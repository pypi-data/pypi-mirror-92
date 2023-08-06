# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""

import re
from setuptools import setup

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('Py2SQL/py2sql.py').read(),
    re.M
).group(1)

with open("README.rst", "rb") as f:
    long_descr = f.read().decode("utf-8")

setup(
    name="cmd-Py2SQL",
    packages=["Py2SQL"],
    entry_points={
        "console_scripts": ['Py2SQL = Py2SQL.py2sql:main']
    },
    version=version,
    description="Python command line application bare bones template.",
    long_description=long_descr,
    author="Makhanko_Mospan_Syzko",
    author_email="",
    url="",
)