import os
from setuptools import setup 
import setuptools

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "ktool",
    version = "0.0.1",
    author = "albert chen",
    author_email = "kkchuchualbert@gmail.com",
    description = (""),
    license = "BSD",
    packages=setuptools.find_packages(),
    long_description=read('README.md'),
)

