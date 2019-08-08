ln -s ~/workspace/kkchuchu.mushroom/backup/.basrc.backup ~/.bashrc
chmod +x bin/*


# Using a virtualenv in an IPython notebook
# ref: https://help.pythonanywhere.com/pages/IPythonNotebookVirtualenvs/
python -m ipykernel install --user --name=mushroom
