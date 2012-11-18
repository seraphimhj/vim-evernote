" ==============================================================
"  Vnote - Post to Evernote from Vim
"  Based on oauth access library by Mattn
" 
"  Version: 0.0.1
"  License: Vim license. See :help license
"  Language: Vim script
"  Maintainer: huangjian <hj1986@gmail.com>
"  Created: Nov 11, 2012
"  Last updated: November 13, 2012
" 
" ==============================================================
 
" check if loaded plugin
if &cp || (exists("g:loaded_vnote") && g:loaded_vnote)
    finish
endif
let g:loaded_vnote = 1

command! -nargs=? -range=% Vnote :call vnote#VNote(<count>, <line1>, <line2>, <f-args>)
