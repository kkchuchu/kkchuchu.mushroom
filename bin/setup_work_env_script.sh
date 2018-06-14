# neovim plug in manager
curl -fLo ~/.local/share/nvim/site/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim

mkdir ~/.config
ln -s ~/workspace/kkchuchu.mushroom/backup/neovim_config/vimwiki ~/vimwiki
ln -s ~/workspace/kkchuchu.mushroom/backup/neovim_config/nvim ~/.config
ln -s ~/workspace/kkchuchu.mushroom/backup/.gitconfig ~/.gitconfig
ln -s ~../backup/.bashrc.backup ~/.bashrc


pip install virtualenv

virtualenv -p python3 --no-site-packages ~/.virtualenvs/mushroom/
. ~/.virtualenvs/mushroom/bin/activate
# reguire pip3
pip3 install neovim jedi

# install plugins
# :PluginInstall
# update python interpreter for vim
# :UpdateRemotePlugin in vim

# let python autocomplete in shell
export PYTHONSTARTUP="$(python -m jedi.__main__ repl)"


# Reference
# vim-plug
# https://github.com/junegunn/vim-plug
# fzf
# https://github.com/junegunn/fzf


