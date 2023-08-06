#!/usr/bin/env python

import argparse
import getpass
import hashlib
import logging
import os
import requests
import shutil
import subprocess
import sys

import edgebox
from edgebox.master_controller import MC, prompt

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.DEBUG if os.environ.get("DEBUG") else logging.INFO)

# Handle incompatibility between Pythons 2 and 3
try:
    input = raw_input
except NameError:
    pass

DEF_CONF_DIR = os.path.expanduser("~/.edgebox")
ARTF_BASE = "https://artifactory.mobiledgex.net/artifactory/edgebox-public"
RELEASE = "r2.4"
CONF_NAME = "config.json"
OS_DEPS = {
    "helm": "https://helm.sh/docs/intro/install/",
    "sha1sum": {
        "darwin": "brew install md5sha1sum",
    },
    "wget": {
        "darwin": "brew install wget",
    },
}
BIN_DEPS = {
    "crmserver": 0o555,
    "dind-cluster-v1.14.sh": 0o555,
    "mcctl": 0o555,
    "plugins/platforms.so": 0o444,
}

def init(args):
    confdir = os.path.join(args.confdir, args.name)
    if not os.path.exists(confdir):
        os.makedirs(confdir)
    config = os.path.join(confdir, CONF_NAME)
    access_key_file = os.path.join(confdir, "accesskey.pem")

    os.environ["PATH"] = "/usr/local/bin:/usr/sbin:/sbin:/usr/bin:/bin"

    return config, access_key_file

def sha256sum(file):
    sha256 = hashlib.sha256()
    with open(file, "rb") as f:
        while True:
            data = f.read(65536)    # 64k buffer
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()

def download_artf(mc, path, deps_dir):
    artf_url = os.path.join(ARTF_BASE, RELEASE, path)
    username = mc.artf_username or mc.username
    password = mc.artf_password or mc.password
    r = requests.head(artf_url,
                      auth=(username, password))
    if r.status_code in (401, 403) and not mc.artf_username:
        username = prompt("Artifactory username")
        password = getpass.getpass(prompt="Artifactory password: ")
        r = requests.head(artf_url,
                          auth=(username, password))

    if r.status_code != requests.codes.ok:
        sys.exit("Error loading dependencies: {}".format(r.status_code))

    need_chksum = r.headers["X-Checksum-Sha256"]

    outfile = os.path.join(deps_dir, path)
    outdir = os.path.dirname(outfile)
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    if os.path.exists(outfile):
        # Verify checksum
        file_chksum = sha256sum(outfile)
        if file_chksum != need_chksum:
            logging.debug("Checksum mismatch: {0} (not \"{1}\")".format(
                outfile, need_chksum))
            os.remove(outfile)

    if not os.path.exists(outfile):
        print("Downloading {}...".format(path))
        with requests.get(artf_url, auth=(username, password), stream=True) as r:
            r.raise_for_status()
            with open(outfile, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

    assert sha256sum(outfile) == need_chksum, \
        "Checksum mismatch: {0}: not \"{1}\"".format( outfile, need_chksum)

    if not mc.artf_username:
        mc.artf_username = username
        mc.artf_password = password

def load_deps(mc, args, version):
    deps_dir = os.path.join(args.confdir, "bin")
    if not os.path.exists(deps_dir):
        os.makedirs(deps_dir)
    deps_loaded = os.path.join(deps_dir, ".{}.done".format(edgebox.__version__))
    if not os.path.exists(deps_loaded):
        logging.debug("Loading dependencies")
        for file in sorted(BIN_DEPS.keys()):
            download_artf(mc, file, deps_dir)
            os.chmod(os.path.join(deps_dir, file), BIN_DEPS[file])

    deps_missing = False
    for binary in sorted(OS_DEPS.keys()):
        exe = shutil.which(binary)
        if not exe:
            deps_missing = True
            msg = "Missing dependency: \"{}\".".format(binary)
            if OS_DEPS[binary]:
                if isinstance(OS_DEPS[binary], dict):
                    if sys.platform in OS_DEPS[binary]:
                        msg += ' ("{}")'.format(OS_DEPS[binary][sys.platform])
                else:
                    msg += ' ("{}")'.format(OS_DEPS[binary])
            print(msg)

    if deps_missing:
        sys.exit()

    with open(deps_loaded, "a"):
        pass

    # Add deps path to system PATH
    os.environ["PATH"] = "{0}:{1}".format(deps_dir, os.environ["PATH"])
    os.environ["GOPATH"] = deps_dir

def create_cloudlet(mc):
    mc.banner("Create cloudlet")
    mc.create_cloudlet()

def generate_access_key(mc, access_key_file):
    mc.banner("Generating access key")
    accesskey = mc.get_access_key()
    with open(access_key_file, "w+") as f:
        f.write(accesskey)
    return access_key_file

def start_crm(mc, access_key_file):
    mc.banner("Starting CRM")

    logdir = mc.logdir
    if not os.path.exists(logdir):
        os.makedirs(logdir)
    outlog = os.path.join(logdir, "crm.out")
    errlog = os.path.join(logdir, "crm.log")

    if mc.deploy_env == "main":
        jaeger = "https://jaeger.mobiledgex.net:14268/api/traces"
    else:
        jaeger = "https://jaeger-{0}.mobiledgex.net:14268/api/traces".format(
            mc.deploy_env)
    os.environ["JAEGER_ENDPOINT"] = jaeger

    cmd = [ "crmserver",
	    "--notifyAddrs", mc.controller + ":37001",
	    "--cloudletKey",
            '{{"organization": "{0}","name":"{1}"}}'.format(mc.cloudlet_org, mc.cloudlet),
	    "--hostname", "crm1",
	    "--region", mc.region,
	    "--platform", "PLATFORM_TYPE_EDGEBOX",
	    "--useVaultCAs",
	    "--useVaultCerts",
	    "--deploymentTag", mc.deploy_env,
	    "--accessKeyFile", access_key_file,
	    "--accessApiAddr", mc.controller + ":41001",
	    "-d", "notify,infra,api,events" ]

    out = open(outlog, "w+")
    err = open(errlog, "w+")
    subprocess.Popen(cmd, stdout=out, stderr=err, stdin=subprocess.DEVNULL,
                     cwd=mc.logdir, start_new_session=True)

def cleanup_cloudlet(mc):
    # Load user credentials
    mc.username
    mc.password

    for c in mc.get_cluster_instances():
        cluster = c["key"]["cluster_key"]["name"]
        cluster_org = c["key"]["organization"]

        for a in mc.get_app_instances(cluster, cluster_org):
            app_name = a["key"]["app_key"]["name"]
            app_vers = a["key"]["app_key"]["version"]
            app_org = a["key"]["app_key"]["organization"]

            mc.banner("Deleting app {0}@{1}".format(app_name, app_vers))
            mc.delete_app_instance(cluster, cluster_org, app_name, app_org, app_vers)

        mc.banner("Deleting cluster {0}".format(cluster))
        mc.delete_cluster_instance(cluster, cluster_org)

    mc.banner("Deleting cloudlet {0}".format(mc.cloudlet))
    try:
        mc.delete_cloudlet()
    except Exception as e:
        if "not found" in str(e):
            # Cloudlet has already been deleted
            print("Cloudlet does not exist")
        else:
            raise e

def cleanup_crm(mc, access_key_file):
    mc.banner("Killing CRM process")
    p = subprocess.Popen(["ps", "-eo", "pid,args"], stdout=subprocess.PIPE,
                         universal_newlines=True)
    out, err = p.communicate()
    for line in out.splitlines():
        (pid, args) = line.split(None, 1)
        if not args.startswith("crmserver "):
            continue
        if access_key_file not in args:
            continue
        print(args)
        subprocess.call(["kill", "-9", pid])
        break

def cleanup_docker(mc):
    mc.banner("Cleaning up docker containers")
    p = subprocess.Popen(["docker", "ps", "-a", "-q"], stdout=subprocess.PIPE,
                         universal_newlines=True)
    out, err = p.communicate()
    for container in out.splitlines():
        print("Deleting docker container " + container)
        subprocess.call(["docker", "stop", container])
        subprocess.call(["docker", "rm", container])

    mc.banner("Cleaning up docker networks")
    p = subprocess.Popen(["docker", "network", "list", "--format", "{{.Name}}"],
                         stdout=subprocess.PIPE, universal_newlines=True)
    out, err = p.communicate()
    for network in out.splitlines():
        if "kubeadm" in network:
            print("Deleting docker network " + network)

def edgebox_create(args):
    config, access_key_file = init(args)

    mc = MC(args.name, config)
    mc.validate()
    mc.save()

    load_deps(mc, args, edgebox.__version__)

    print("\nCreating edgebox cloudlet:")
    print(mc)
    if not mc.confirm_continue():
        os.remove(config)
        sys.exit("Not creating edgebox")

    create_cloudlet(mc)
    generate_access_key(mc, access_key_file)
    start_crm(mc, access_key_file)

def edgebox_delete(args):
    config, access_key_file = init(args)
    if not os.path.exists(config):
        sys.exit("Edgebox not found: {}".format(config))

    mc = MC(args.name, config)

    print("\nDeleting edgebox cloudlet:")
    print(mc)
    if not mc.confirm_continue():
        sys.exit("Not deleting cloudlet")

    cleanup_cloudlet(mc)
    cleanup_docker(mc)
    cleanup_crm(mc, access_key_file)

def edgebox_list(args):
    _, dirnames, _ = next(os.walk(args.confdir))
    for dirname in sorted(dirnames):
        if os.path.exists(os.path.join(args.confdir, dirname, CONF_NAME)):
            print(dirname)
   
def edgebox_show(args):
    config, _ = init(args)
    if not os.path.exists(config):
        sys.exit("Edgebox not found: {}".format(config))

    mc = MC(args.name, config)
    print("\nEdgebox {}:".format(args.name))
    print(mc)

def edgebox_version(args):
    print("{} ({})".format(edgebox.__version__, RELEASE))

def main():
    parser = argparse.ArgumentParser(prog='edgebox',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--debug", action="store_true",
                        help="Enable debug logging")
    parser.add_argument("--confdir", help="configuration directory",
                        default=DEF_CONF_DIR)
    subparsers = parser.add_subparsers(help="sub-command help", dest="cmd")
    subparsers.required = True

    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument("name", help="edgebox name")
    common_parser.add_argument("--region", help="region")
    common_parser.add_argument("--cloudlet", help="cloudlet name")
    common_parser.add_argument("--cloudlet-org", help="cloudlet org")

    parser_create = subparsers.add_parser("create", help="create edgeboxes",
                                          parents=[common_parser])
    parser_create.set_defaults(func=edgebox_create)

    parser_delete = subparsers.add_parser("delete", help="delete edgeboxes",
                                          parents=[common_parser])
    parser_delete.set_defaults(func=edgebox_delete)

    parser_list = subparsers.add_parser("list", help="list edgeboxes")
    parser_list.set_defaults(func=edgebox_list)

    parser_list = subparsers.add_parser("show", help="show edgebox details")
    parser_list.add_argument("name", help="edgebox name")
    parser_list.set_defaults(func=edgebox_show)

    parser_version = subparsers.add_parser("version", help="display version")
    parser_version.set_defaults(func=edgebox_version)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
