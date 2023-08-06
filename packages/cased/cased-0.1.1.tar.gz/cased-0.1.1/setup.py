import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


setup(
    name="cased",
    version="0.1.1",
    description="",
    long_description="",
    author="Cased",
    author_email="support@cased.com",
    url="https://github.com/cased/guard-client",
    license="MIT",
    keywords="cased api",
    packages=find_packages(exclude=["tests", "tests.*"]),
    zip_safe=False,
    scripts=["cased-init", "cguard/cased"],
    python_requires=">3.5",
    install_requires=[
        "cased >= 0.3.8",
        "requests",
        "responses",
        "mock",
        "pytest >= 4.0c0",
        "pytest-mock",
        "pytest-xdist",
        "flask",
        "yaspin",
    ],
    project_urls={
        "Bug Tracker": "https://github.com/cased/guard/issues",
        "Documentation": "https://docs.cased.com/guard",
        "Source Code": "https://github.com/cased/guard",
    },
)
