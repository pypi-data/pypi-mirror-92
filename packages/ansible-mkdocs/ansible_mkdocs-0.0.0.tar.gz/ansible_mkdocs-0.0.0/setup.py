"""Packaging file for ansible_mkdocs."""
from distutils.core import setup


__version__ = "0.0.0"
URL = "https://github.com/tbobm/ansible_mkdocs/archive/{}.tar.gz".format(__version__)

setup(
    name="ansible_mkdocs",
    packages=["ansible_mkdocs"],
    install_requires=[
    ],
    version=__version__,
    description="Broker payload spooler",
    author="Theo 'Bob' Massard",
    author_email="tbobm@protonmail.com",
    url="https://github.com/tbobm/ansible_mkdocs",
    download_url=URL,
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
)
