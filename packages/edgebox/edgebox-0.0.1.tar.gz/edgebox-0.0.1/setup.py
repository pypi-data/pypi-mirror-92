from setuptools import setup
import edgebox

setup(name='edgebox',
      version="0.0.1",
      description='Edgebox for MobiledgeX',
      url='http://github.com/mobiledgex/edgebox',
      author='Venky Tumkur',
      author_email='venky.tumkur@mobiledgex.com',
      license='MIT',
      packages=['edgebox'],
      python_requires='>=3.6, <4',
      install_requires=[
          'requests>=2.23.0'
      ],
      zip_safe=False)
