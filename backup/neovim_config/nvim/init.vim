call plug#begin('~/.config/nvim/plugged')
" Make sure you use single quotes
function! DoRemote(arg)
  UpdateRemotePlugins
endfunction

" Git wrapper. Example: Gstatus.
Plug 'tpope/vim-fugitive'

" On-demand loading
Plug 'scrooloose/nerdtree'
Plug 'jistr/vim-nerdtree-tabs'

" Fuzzy autcomplete.
" Example: :FZF.
set rtp+=~/.fzf

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
" :Tab/:\zs 
Plug 'godlygeek/tabular'
Plug 'terryma/vim-multiple-cursors'

" :Autoformat
Plug 'Chiel92/vim-autoformat'

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
set background=dark
" set colorcolumn=79
set ignorecase
set smartcase
" Enable folding
set foldmethod=indent
set foldlevel=99
nnoremap <space> za
map <C-U> :redo<CR>
autocmd! VimEnter * :GuiColorScheme wombat
autocmd! VimEnter * :AirlineTheme molokai


" python auto-complete
let g:deoplete#enable_at_startup = 1
set completeopt-=preview
let g:deoplete#sources#jedi#statement_length = 0 
let g:python_host_prog = 'python3'
" let g:python3_host_prog = '/usr/bin/python3'


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

" autocmd BufWritePost * @:

" map capslock to ctrl
command Ctrl2Capslock execute "!echo \"keycode 58 = Caps_Lock\" >> ~/keymap; echo \"keycode 58 = Escape\" >> ~/keymap; loadkeys ~/keymap; rm ~/keymap"
" sample
command -nargs=1 Echo echo <q-args>

" Ggrep -> tab copen -> ctrl t open file in new tab
autocmd FileType qf nnoremap <buffer> <c-t> <C-W><Enter><C-W>T
autocmd QuickFixCmdPost *grep* tab cwindow
command -nargs=+ Send :!send_command "<q-args>"
command Gg :FZF
set switchbuf=usetab

command Whereis :echo @%
