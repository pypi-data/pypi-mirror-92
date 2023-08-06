#!/usr/bin/env python

import os

HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = "1.0.0"

setup(
    name="gcloud-auth-headers",
    version=version,
    description="Token generator for cloud endpoints with Oauth2",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Bruno Tomas S Buzzo",
    author_email="bbuzzo_engineering@timbrasil.com.br",
    url="https://github.com/btbuzzo/gcloud-oauth-headers",
    packages=['gcloud_oauth_headers'],
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    include_package_data=True,
    install_requires=[
        "google-auth",
    ],
    entry_points={"console_scripts": ["generate_headers=gcloud_oauth_headers.__main__:main"]},
)
