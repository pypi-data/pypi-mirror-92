import os
import sys

from setuptools import find_packages, setup

version = "0.3b3"

def readfile(name):
    with open(os.path.join(os.path.dirname(__file__), name)) as f:
        out = f.read()
    return out

desc = '\n'.join([readfile('README.rst'), readfile('CHANGELOG.rst')])

setup(
    name="mfw-template",
    version=version,
    description="Cookiecutter templates for Morp Framework",
    long_description=desc,
    classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords="",
    author="Izhar Firdaus",
    author_email="kagesenshi.87@gmail.com",
    url="http://github.com/morpframework",
    license="MIT",
    packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "cookiecutter>=1.7.2",
        "click>=7.1.2",
        "importscan",
        "pyyaml>=4.2b1",
        "cryptography",
        # -*- Extra requirements: -*-
    ],
    extras_require={
        "docs": [
            'sphinx-click'
        ]
    },
    entry_points={
        "console_scripts": [
            "mfw-template=mfw_template.cli:cli",
        ]
    },
)
