# neovim plug in manager
curl -fLo ~/.local/share/nvim/site/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim

$mushroom_folder = $1

mkdir ~/.config
ln -s $mushroom_folder / '/backup/neovim_config/nvim' ~/.config
ln -s $mushroom_folder / '/backup/.gitconfig' ~/.gitconfig
ln -s $mushroom_folder / '/backup/ctags' ~/.ctags
ln -s $mushroom_folder / '/backup/bash_profile' ~/.profile

chmod +x $mushroom_folder / '/bin'


# create virtualenv for neovim

rm -rf ~/.virtualenvs/mushroom/

pip3 install virtualenv

virtualenv -p python3 --no-site-packages ~/.virtualenvs/mushroom/
. ~/.virtualenvs/mushroom/bin/activate
# reguire pip3
pip3 install -r $mushroom_folder / '/requirements.txt'

deactivate


# jupyter notebook setup

rm -rf ~/.virtualenvs/k_lab/
virtualenv -p python3.7 --no-site-packages ~/.virtualenvs/k_lab/
. ~/.virtualenvs/k_lab/bin/activate
pip3 install -r $mushroom_folder / '/data_project_requirements.txt'

python -m ipykernel install --user --name=k_lab

# install plugins
# :PluginInstall
# update python interpreter for vim
# :UpdateRemotePlugin in vim

# let python autocomplete in shell
export PYTHONSTARTUP="$(python -m jedi.__main__ repl)"
export PYTHONPATH="${PYTHONPATH}:$1"


# Reference
# vim-plug
# https://github.com/junegunn/vim-plug
# fzf
# https://github.com/junegunn/fzf
