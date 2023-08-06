#! /usr/bin/env python
from codecs import open

from setuptools import find_packages, setup

with open("README.md", "r", "utf-8") as f:
    readme = f.read()

setup(
    name="amqp_client_cli",
    packages=find_packages(),
    version="0.4.1",
    description="A command line interface for interacting with amqp exchanges.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Dillon Dixon",
    url="https://github.com/ownaginatious/amqp-client-cli",
    license="MIT",
    keywords=["amqp", "cli", "client", "rabbitmq", "amq"],
    classifiers=[
        "Environment :: Console",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=[
        line.strip() for line in open("requirements.txt", "r", "utf-8").readlines()
    ],
    entry_points={
        "console_scripts": [
            "amqpcli = amqp_client_cli.main:main",
        ],
    },
)
