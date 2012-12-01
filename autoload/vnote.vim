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

" Avoid side-effects from cpoptions setting.
let s:save_cpo = &cpo
set cpo&vim

let s:configfile = expand('~/.vnoterc')
let s:note = expand('~/.vnote')

let g:vnote_config = {}
let g:vnote_config.consumer_key = "chiyantian"
let g:vnote_config.consumer_secret = "943df63e8e294b48"
let g:vnote_config.callback = "http://huangjian.info"

" set rtp+=.

if !exists('g:Vnote_exec_dir')
    let g:Vnote_exec_dir = simplify(expand('<sfile>:p:h') .'/..') .
                \ "/evernote-sdk-python/sample"
    echo g:Vnote_exec_dir
endif

function! s:AuthVNote()
    redraw
    echo "Authencating..."
   
    let request_token_url = "https://sandbox.evernote.com/oauth"
    let auth_url = "https://sandbox.evernote.com/OAuth.action"
    let access_token_url = "https://sandbox.evernote.com/oauth"

    " third is additional params 
    let g:vnote_config = oauth#request_token(request_token_url, g:vnote_config, {"oauth_callback": g:vnote_config.callback})
    if has("win32") || has("win64")
        exe "!start rundll32 url.dll,FileProtocolHandler ".auth_url."?oauth_token=".g:vnote_config.request_token
    else
        call system("xdg-open '".auth_url."?oauth_token=".g:vnote_config.request_token. "'")
    endif
    " after grant access 
    " return to callback url
    " then callback url display the oauth_verifier
    let verifier = input("VERIFIER:")
    let g:vnote_config = oauth#access_token(access_token_url, g:vnote_config, {"oauth_verifier": verifier})
    call writefile([string(g:vnote_config)], s:configfile)
    redraw!
endfunction

function! vnote#VNote(count, line1, line2, ...)
    if !exists("g:vnote_config.access_token")
        if filereadable(s:configfile)
            let g:vnote_config = {}
            let g:vnote_config = eval(join(readfile(s:configfile), ""))
        else  
            call s:AuthVNote()
        endif
    endif
    if !exists("g:vnote_config.access_token")
        return
    endif     
    let notefile = {}
    let notefile.title = s:get_current_filename()
    if a:count < 1
        let notefile.content = join(getline(a:line1, a:line2), "\n")
    else
        " reselect & past in register
        let save_regcont = @"
        let save_regtype = getregtype('"')
        silent! normal! gvy
        let notefile.content = @"
        call setreg('"', save_regcont, save_regtype)
    endif
    " in case Newline will be strtrans() to ^@ (nr2char(10))
    let notefile = map(notefile, 'substitute(v:val, "\n", "<br/>", "g")')
    call writefile([string(notefile)], s:note)

    exec "cd ".g:Vnote_exec_dir
    exec "!python EDAMTest.py ".g:vnote_config.access_token
    exec "cd -"
endfunction

function! s:get_current_filename()
    let filename = '[vnote] '.expand('%:t')
    let nowtime = strftime("%b-%d-%Y")
    if len(filename) == 0 || filename == ''
        let filename = printf('[vnote] %s', nowtime)
    endif
    return filename
endfunction

" List cnt notes from your evernote account
" use silent noautocmd split bufname
function! s:VnoteList(cnt)
    return
endfunction

function! s:shellwords(str)
    let words = split(a:str, '\%(\([^ \t\''"]\+\)\|''\([^\'']*\)''\|"\(\%([^\"\\]\|\\.\)*\)"\)\zs\s*\ze')
    let words = map(words, 'substitute(v:val, ''\\\([\\ ]\)'', ''\1'', "g")')
    let words = map(words, 'matchstr(v:val, ''^\%\("\zs\(.*\)\ze"\|''''\zs\(.*\)\ze''''\|.*\)$'')')
    return words
endfunction

let &cpo = s:save_cpo
unlet s:save_cpo
