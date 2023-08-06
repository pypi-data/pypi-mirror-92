#!/usr/bin/env python

from distutils.core import setup

from setuptools import find_packages

from settings import settings


with open("requirements.txt") as requirements_file:
    text = requirements_file.read()

    install_requires = text.split("\n")

packages = find_packages()

setup(
    name=settings.NAME,
    version=settings.VERSION,

    long_description=settings.LONG_DESCRIPTION,
    long_description_content_type="text/markdown",

    author=settings.AUTHOR,
    author_email=settings.AUTHOR_EMAIL,

    url=settings.URL,

    install_requires=install_requires,
    packages=packages,

    license=settings.LICENSE,
)
