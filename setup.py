import os
from setuptools import setup
import setuptools


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="ktool",
    version="0.0.1",
    author="albert chen",
    author_email="kkchuchualbert@gmail.com",
    description=(""),
    license="BSD",
    packages=setuptools.find_packages(),
    long_description=read('README.md'),
)
