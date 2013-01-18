## Description

Vnote —— Facility for Vim & Evernote User

This application is a vim-plugin based on evernote python api. 

It use oauth to get access to a user's account. 

With this, you can:

- list your notebook in your account;
- create new notes;
- editor then update your exist notes;

if you like, you can use it like snippet collector, or a personal wiki.

## Setup
Clone the vim-evernote files to your vim path

or run command: 

cp -r vim-evernote/ ~/.vim

ps: recommand Vundle to manage this vim plugin.
 
## Usage
 
- Post current buffer to gist, using default privacy option.

        :Gist

- Post selected text to gist, using default privacy option.
  This applies to all permutations listed below (except multi).

        :'<,'>Gist
 
- Edit the gist with name 'foo.js' (you need to have opened the gist buffer
  first).

        :Gist -e foo.js
 
- Delete the gist (you need to have opened the gist buffer first).
  Password authentication is needed.

        :Gist -d
 
- List your public gists.

        :Gist -l

## Tips 

If you want to open browser after the post:

    let g:gist_open_browser_after_post = 1
 
If you want to change the browser:

    let g:gist_browser_command = 'w3m %URL%'

or:

    let g:gist_browser_command = 'opera %URL% &'
 
## Changelist

2012.12.27 重构Eernote Python API

2012.12.01 完成基础VIML的开发

## Contact 

author: Huangjian

email: hj1986@gmail.com

website: huangjian.info

## License:

    Copyright 2012 by Huang jian
    modification, are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice,
       this list of conditions and the following disclaimer.
    2. Redistributions in binary form must reproduce the above copyright notice,
       this list of conditions and the following disclaimer in the documentation
       and/or other materials provided with the distribution.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
    ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
    FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
    REGENTS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
    INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
    HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
    STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
    ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
    OF THE POSSIBILITY OF SUCH DAMAGE.


## Install:

Copy it to your plugin directory.

- rtp:
  - autoload/vnote.vim
  - evernote-sdk-python
  - plugin/vnote.vim

If you want to uninstall vnote.vim, remember to also remove `~/.vnote`.

## Setup:

This plugin uses Evernote API v1.22. Configure is stored in `~/.vnoterc`.

When first time to use vnote, you need to approve vnote to access your Evernote account through oauth:

    :Vnote
    authencating...

Then, vnote.vim will ask for your password to create an authorization when you
first use it. The password is not stored and only the OAuth access token will
be kept for later use. 


