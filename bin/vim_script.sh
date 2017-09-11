# neovim plug in manager
curl -fLo ~/.local/share/nvim/site/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim

# reguire pip3
pip3 install neovim, jedi

# update python interpreter for vim
# :UpdateRemotePlugin in vim

# let python autocomplete in shell
export PYTHONSTARTUP="$(python -m jedi.__main__ repl)"


# Reference
# vim-plug
# https://github.com/junegunn/vim-plug
# fzf
# https://github.com/junegunn/fzf

