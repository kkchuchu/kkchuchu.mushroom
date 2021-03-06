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

## Installing auto-sklearn 
``` sh
curl https://raw.githubusercontent.com/automl/auto-sklearn/master/requirements.txt | xargs -n 1 -L 1 pip install
pip install auto-sklearn
```
Ref: https://automl.github.io/auto-sklearn/master/installation.html

## Downloading Data From Kaggle

1. Install kaggle command
``` sh
pip install kaggle
```
2. Go to https://www.kaggle.com/kkchuchu/account
3. Click "Create New API Token"
4. Download compressed files
``` sh
kaggle competitions download -c competitive-data-science-predict-future-sales
```
## Reference

- jupyter config: https://ipython.readthedocs.io/en/stable/interactive/magics.html
