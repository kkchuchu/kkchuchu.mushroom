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

" Complete
Plug 'Shougo/deoplete.nvim', { 'do': function('DoRemote') }
Plug 'davidhalter/jedi-vim'
Plug 'Shougo/unite.vim'

" python indent
Plug 'hynek/vim-python-pep8-indent'

" gui colorscheme
Plug 'thinca/vim-guicolorscheme'

" http://vimcasts.org/episodes/aligning-text-with-tabular-vim/.
" Example: :Tab /=
" :Tab/:\zs
Plug 'godlygeek/tabular'

" :Autoformat
Plug 'Chiel92/vim-autoformat'

Plug 'junegunn/fzf', { 'dir': '~/.fzf', 'do': './install --all' }

Plug 'hzchirs/vim-material'

Plug 'tell-k/vim-autopep8'

Plug 'ludovicchabant/vim-gutentags'


" Add plugins to &runtimepath
call plug#end()

filetype plugin on

" if $COLORTERM == 'gnome-terminal'
"   set t_Co=256
" endif

set termguicolors
set nocompatible
filetype plugin on
syntax on

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
set list
nnoremap <space> za
map <C-U> :redo<CR>
colorscheme wombat


" python auto-complete
let g:deoplete#enable_at_startup = 1
set completeopt+=preview

let g:deoplete#sources#jedi#statement_length = 0
highlight Pmenu guibg=#606060
let g:jedi#force_py_version = '3'
" jedi-python
let g:jedi#completions_enabled = 1
let g:python3_host_prog = expand('~/.virtualenvs/mushroom/bin/python3')


" NERDTree
let NERDTreeShowHidden=1
" let g:nerdtree_tabs_open_on_gui_startup = 1
" let g:nerdtree_tabs_open_on_console_startup = 1


" sample
command -nargs=1 Echo echo <q-args>

" Ggrep -> tab copen -> ctrl t open file in new tab
autocmd FileType qf nnoremap <buffer> <c-t> <C-W><Enter><C-W>T
autocmd QuickFixCmdPost *grep* tab cwindow
":Send args
command -nargs=+ Send :!send_command "<q-args>"
set switchbuf=usetab

command Whereis :echo @%
:map <c-f> <s-k>
:setlocal display=uhex
command -nargs=+ Ggreppy :Ggrep -I "<q-args>" -- '*.py'

let g:ctrlp_map = '<c-p>'
let g:ctrlp_cmd = 'CtrlP'

let g:jedi#goto_command = ""
let g:jedi#goto_assignments_command = "<leader>g"
let g:jedi#goto_definitions_command = "<leader>d"
let g:jedi#documentation_command = "K"
let g:jedi#usages_command = "<leader>n"
let g:jedi#completions_command = "<C-Space>"
let g:jedi#rename_command = "<leader>r"

let g:fzf_buffers_jump = 1


function! s:tags_sink(line)
  let parts = split(a:line, '\t\zs')
  let excmd = matchstr(parts[2:], '^.*\ze;"\t')
  execute 'silent e' parts[1][:-2]
  let [magic, &magic] = [&magic, 0]
  execute excmd
  let &magic = magic
endfunction

function! s:tags()
  if empty(tagfiles())
    echohl WarningMsg
    echom 'Preparing tags'
    echohl None
    call system('ctags -R')
  endif

  call fzf#run({
  \ 'source':  'cat '.join(map(tagfiles(), 'fnamemodify(v:val, ":S")')).
  \            '| grep -v -a ^!',
  \ 'options': '+m -d "\t" --with-nth 1,4.. -n 1 --tiebreak=index',
  \ 'down':    '40%',
  \ 'sink':    function('s:tags_sink')})
endfunction

command! Tags call s:tags()
