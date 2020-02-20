# README

## Developing Process
- Install ktool.
- Create Virtualenv.
- Create notebook for the new topic,
- Connection and data parser should be in the ktool with unittests for the sharing purpose.
- Connection String or Sensative Data Should be in another project.

# Installization

Install ktool

``` sh
cd mushroom
pip3 install -e .
```


# How to
## Create wheel File From Source
1. Create Package Folder
2. Create setup.py
3. Run python setup.py sdist bdist_wheel

Ref: https://packaging.python.org/tutorials/packaging-projects/
