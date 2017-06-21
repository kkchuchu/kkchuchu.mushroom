call plug#begin('~/.config/nvim/plugged')
" Make sure you use single quotes
function! DoRemote(arg)
  UpdateRemotePlugins
endfunction

" Git wrapper. Example: Git status.
Plug 'tpope/vim-fugitive'

" On-demand loading
Plug 'scrooloose/nerdtree'
Plug 'jistr/vim-nerdtree-tabs'

" Fuzzy autcomplete.
" Example: :FZF.
" brew install fzf
set rtp+=/usr/local/opt/fzf

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
set foldnestmax=2
set foldmethod=indent
" set foldlevel=99
nnoremap <space> za

set ignorecase
set smartcase 

" python auto-complete
let g:deoplete#enable_at_startup = 1
set completeopt-=preview
let g:deoplete#sources#jedi#statement_length = 0 
let g:python_host_prog = 'python3'
" let g:python3_host_prog = '/usr/bin/python3'

" tmhedberg/SimpylFold
let g:SimpylFold_docstring_preview = 1

" tagbar
let g:tagbar_left = 0
" autocmd VimEnter *.py :Tagbar

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
set switchbuf+=usetab,newtab

" autocmd BufWritePost * @:

command Wmyut execute "!rsync -ravz --exclude .git --no-o -e ssh ~/workspace/WFBSS_SERVER/ myut:~/WFBS_Hosted"
" $(echo -ne '\r')

nmap <F7> :ToggleNERDTreeAndTagbar<CR>

command ChangeCtrl execute "!echo \"keycode 58 = Caps_Lock\" >> ~/keymap; echo \"keycode 58 = Escape\" >> ~/keymap; loadkeys ~/keymap; rm ~/keymap"

autocmd FileType qf nnoremap <buffer> <c-t> <C-W><Enter><C-W>T
