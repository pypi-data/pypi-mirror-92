#!/usr/bin/env python3

import os
from setuptools import setup, find_packages


def read(fname):
  return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
  name = "doppler-client",
  version = "1.0.12",
  author = "Doppler Team",
  author_email = "support@doppler.com",
  description = "This package is deprecated and is no longer functional. Learn how to migrate to the new CLI at https://docs.doppler.com/docs/removal-deprecated-packages-scripts",
  license = "Apache License 2.0",
  long_description=read('README.md'),
  long_description_content_type='text/markdown',
  keywords = "doppler environment management api key keys secrets",
  url = "https://github.com/DopplerHQ/python-client",
  packages=find_packages(exclude=["tests", "templates", "experiments"]),
  install_requires=[
    "requests",
    "requests-futures",
    "enum34"
  ],
  classifiers=[
    "Development Status :: 7 - Inactive",
    "Topic :: Utilities",
    "License :: OSI Approved :: Apache Software License"
  ],
  project_urls={
    'Bug Reports': 'https://github.com/DopplerHQ/python-client/issues',
    'Source': 'https://github.com/DopplerHQ/python-client',
  },
)