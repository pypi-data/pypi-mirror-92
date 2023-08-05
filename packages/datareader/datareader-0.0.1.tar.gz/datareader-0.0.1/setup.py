# -------------------------------------------------------------
# code developed by Michael Hartmann during his Ph.D.
# Reachability Analysis
#
# (C) 2020 Michael Hartmann, Graz, Austria
# Released under GNU GENERAL PUBLIC LICENSE
# email michael.hartmann@v2c2.at
# -------------------------------------------------------------

import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='datareader',
      version='0.0.1',
      description='Data reader',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/ga74kud/datareader',
      author='Michael Hartmann',
      author_email='michael.hartmann@v2c2.at',
      license='GNU GENERAL PUBLIC LICENSE',
      packages=setuptools.find_packages(),
      package_data={'': ['*.txt', 'datareader/annotations.txt']},
      include_package_data=True,
      install_requires=[
          "numpy",
          "pandas",
          "argparse",
          "scipy",
          "matplotlib",
        ],
      zip_safe=False)
