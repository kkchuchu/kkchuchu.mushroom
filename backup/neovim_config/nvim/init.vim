call plug#begin('~/.config/nvim/plugged')
" Make sure you use single quotes
function! DoRemote(arg)
  UpdateRemotePlugins
endfunction

" Git wrapper. Example: Git status.
Plug 'tpope/vim-fugitive'

" Auto generate tags: [required]ctags
Plug 'szw/vim-tags'

" Show tags
Plug 'kkchuchu/tagbar', { 'branch': 'less_command'}

" On-demand loading
Plug 'scrooloose/nerdtree'
Plug 'jistr/vim-nerdtree-tabs'

" REPL
Plug 'tpope/vim-fireplace'

" Fuzzy autcomplete.
" Example: :FZF. :Tags tagyousearch. :Ag regex
" brew install the_silver_search
Plug 'junegunn/fzf', { 'dir': '~/.config/nvim/fzf', 'do': './install --all' }
Plug 'junegunn/fzf.vim'

" Complete
Plug 'Shougo/deoplete.nvim', { 'do': function('DoRemote') }

" Python Complete
Plug 'zchee/deoplete-jedi'

" python indent
Plug 'hynek/vim-python-pep8-indent'

" vim airline (status-line)
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'

" gui colorscheme
Plug 'thinca/vim-guicolorscheme'

" http://vimcasts.org/episodes/aligning-text-with-tabular-vim/. 
" Example: :Tab /=
Plug 'godlygeek/tabular'

" Add plugins to &runtimepath
call plug#end()

filetype plugin on

if $COLORTERM == 'gnome-terminal'
  set t_Co=256
endif

set tabstop=4
set shiftwidth=4
set expandtab

set nu
set hlsearch
syntax enable
set clipboard=unnamed
autocmd! VimEnter * :GuiColorScheme wombat
autocmd! VimEnter * :AirlineTheme molokai
set background=dark
" set colorcolumn=79

" Enable folding
" set foldmethod=indent
" set foldlevel=99
nnoremap <space> za

set ignorecase
set smartcase 

" python auto-complete
let g:deoplete#enable_at_startup = 1
set completeopt-=preview
let g:deoplete#sources#jedi#statement_length = 0 
let g:python_host_prog = 'python3'
" let g:python3_host_prog = '/Users/albert_chen/.virtualenvs/|_____|/bin/python'

" tmhedberg/SimpylFold
let g:SimpylFold_docstring_preview = 1

" tagbar
let g:tagbar_left = 0
autocmd VimEnter *.py :Tagbar

" NERDTree
let NERDTreeShowHidden=1
let g:nerdtree_tabs_open_on_gui_startup = 1
let g:nerdtree_tabs_open_on_console_startup = 1

" airline
let g:airline#extensions#tabline#enabled = 1
let g:airline#extensions#tabline#left_sep = ' '
let g:airline#extensions#tabline#left_alt_sep = '|'
let g:airline#extensions#tabline#show_buffers = 0
let g:airline#extensions#tabline#show_splits = 0
let g:airline#extensions#tabline#show_tabs = 1
let g:airline#extensions#tabline#show_tab_nr = 0
let g:airline#extensions#tabline#show_tab_type = 0
let g:airline#extensions#tabline#buffer_nr_show = 1
let g:airline_section_c = 0
let g:airline_section_y = 0
let g:airline_section_warning = 0
let g:airline_theme = 'molokai'

" autocmd VimEnter * :hi Directory guifg=#FF0000 ctermfg=red

let g:vim_tags_auto_generate = 1

" Customize shortcut
map <C-U> :redo<CR>

" autocmd BufWritePost * @:

command Wmyut execute "!rsync -ravz --exclude .git --no-o -e ssh ~/workspace/WFBSS_SERVER/ myut:~/WFBS_Hosted"
" $(echo -ne '\r')

imap <C-d> <C-[>diwie
