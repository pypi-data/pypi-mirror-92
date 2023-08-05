#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from setuptools import setup
from crosspm import config

build_number = os.getenv("TRAVIS_BUILD_NUMBER", "")
branch = os.getenv("TRAVIS_BRANCH", "")
travis = any((build_number, branch,))
version = config.__version__.split(".")
develop_status = "4 - Beta"
url = "https://devopshq.github.io/crosspm2/"

if travis:
    version = version[0:3]
    if branch == "master":
        develop_status = "5 - Production/Stable"
        version.append(build_number)
    else:
        version.append("{}{}".format("dev" if branch == "develop" else branch, build_number))
else:
    if len(version) < 4:
        version.append("dev0")

version = ".".join(version)
if travis:
    with open("crosspm/config.py", "w", encoding="utf-8") as f:
        f.write("__version__ = '{}'".format(version))

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="crosspm2",
    version=version,
    description="Cross Package Manager 2",
    license="MIT",
    author="Timut Gilmullin",
    author_email="tim55667757@gmail.com",
    url=url,
    long_description=long_description,
    download_url="https://github.com/devopshq/crosspm2.git",
    entry_points={"console_scripts": ["crosspm2=crosspm.__main__:main"]},
    classifiers=[
        "Development Status :: {}".format(develop_status),
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
    ],
    keywords=[
        "development",
        "dependency",
        "requirements",
        "manager",
        "versioning",
        "packet",
    ],
    packages=[
        "crosspm",
        "crosspm.helpers",
        "crosspm.adapters",
        "crosspm.template",
        "crosspm.contracts"
    ],
    setup_requires=[
        "wheel==0.34.2",
        "pypandoc==1.5",
    ],
    tests_require=[
        "flake8==3.7.9",
        "pytest<=4.6.9; python_version < '3.5'",
        "pytest>=5.2; python_version >= '3.5'",
        "pytest-flask<1.0.0; python_version < '3.5'",
        "pytest-flask>=1.0.0; python_version >= '3.5'",
        "PyYAML<5.2; python_version < '3.5'",
        "PyYAML>=5.2; python_version >= '3.5'",
    ],
    install_requires=[
        "requests<2.22; python_version < '3.5'",
        "requests>=2.22; python_version >= '3.5'",
        "urllib3==1.24.3",
        "docopt==0.6.2",
        "PyYAML==5.1.2; python_version < '3.5'",
        "PyYAML>=5.2; python_version >= '3.5'",
        "dohq-artifactory==0.4.112; python_version < '3.5'",
        "dohq-artifactory>=0.7.377; python_version >= '3.5'",
        "dohq-common",
        "Jinja2<2.11; python_version < '3.5'",
        "Jinja2>=2.11; python_version >= '3.5'",
        "patool==1.12",  # need for pyunpack
        "pyunpack==0.1.2",
        "addict==2.2.1",  # need for crosspm2 contract scheme
        "packaging>=20.4",  # need for crosspm2 contract scheme
        "parse>=1.15.0",  # need for crosspm2 contract scheme
        "tabulate>=0.8.7",  # need for crosspm2 contract scheme
        "ordered-set>=4.0.2",
        "wcmatch",

    ],
    package_data={
        "": [
            "./template/*.j2",
            "*.cmake",
            "../LICENSE",
            "../README.*",
        ],
    },
)
