#
# A simple Evernote API demo script that lists all notebooks in the user's
# account and creates a simple test note in the default notebook.
#
# Before running this sample, you must fill in your Evernote developer token.
#
# To run (Unix):
#   export PYTHONPATH=../lib; python EDAMTest.py
#

import os
import sys
from optparse import OptionParser
#import getopt
sys.path.append("../lib")
import hashlib
import binascii
import time
import json
import thrift.protocol.TBinaryProtocol as TBinaryProtocol
import thrift.transport.THttpClient as THttpClient
import evernote.edam.userstore.UserStore as UserStore
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.notestore.NoteStore as NoteStore
import evernote.edam.type.ttypes as Types
import evernote.edam.error.ttypes as Errors

class Vnote():
    '''
    Vnote Python
    '''
    def __init__(self, config):
        self.config = config
        self.authToken = config["access_token"]
        '''
        Initial development is performed on our sandbox server. 
        To use the production service, 
        change "sandbox.evernote.com" to "www.evernote.com" and replace your
        developer token above with a token from 
        https://www.evernote.com/api/DeveloperToken.action
        '''
        self.evernoteHost = "sandbox.evernote.com"
        userStoreUri = "https://" + self.evernoteHost + "/edam/user"
        userStoreHttpClient = THttpClient.THttpClient(userStoreUri)
        userStoreProtocol = TBinaryProtocol.TBinaryProtocol(userStoreHttpClient)
        self.userStore = UserStore.Client(userStoreProtocol)  
        '''
        Get the URL used to interact with the contents of the user's account
        When your application authenticates using OAuth, the NoteStore URL will
        be returned along with the auth token in the final OAuth request.
        In that case, you don't need to make this call.
        '''
        noteStoreUrl = self.userStore.getNoteStoreUrl(self.authToken)
        #print noteStoreUrl 
        noteStoreHttpClient = THttpClient.THttpClient(noteStoreUrl)
        noteStoreProtocol = TBinaryProtocol.TBinaryProtocol(noteStoreHttpClient)
        self.noteStore = NoteStore.Client(noteStoreProtocol)

    def check_version(self):
        versionOK = self.userStore.checkVersion("Evernote EDAMTest (Python)",
                UserStoreConstants.EDAM_VERSION_MAJOR,
                UserStoreConstants.EDAM_VERSION_MINOR)
        print "Is my Evernote API version up to date? ", str(versionOK)
        print "Your API version is ", str(UserStoreConstants.EDAM_VERSION_MAJOR), ".", str(UserStoreConstants.EDAM_VERSION_MINOR)
        print ""
        if not versionOK:
            return 1
        return 0

    def _get_resource(self, attach):
        '''
        To display the Resource as part of the note's content, 
        include an <en-media> tag in the note's ENML content. 
        The en-media tag identifies the corresponding
        Resource using the MD5 hash.
        '''             
        md5 = hashlib.md5()
        md5.update(attach)
        hash = md5.digest()
        hashHex = binascii.hexlify(hash)

        '''
        To include an attachment such as an image in a note, 
        first create a Resource for the attachment. 
        At a minimum, the Resource contains the binary attachment data, 
        an MD5 hash of the binary data, and the attachment MIME type. 
        It can also include attributes such as filename and location.
        '''
        data = Types.Data()
        data.size = len(attach)
        data.bodyHash = hash
        data.body = attach

        resource = Types.Resource()
        resource.mime = 'image/png'
        resource.data = data
        return resource, hashHex 
    
    def add(self, anote):
        '''
        To create a new note, simply create a new Note object and fill in 
        attributes such as the note's title.
        '''
        note = Types.Note()
        note.title = anote["title"]
        if (anote.has_key("attachment")) and (len(anote["attachment"]) > 0):
            (resource, hashHex) = _get_resource(anote["attachment"])
            note.resources = [ resource ]
        '''
        The content of an Evernote note is represented 
        using Evernote Markup Language (ENML). 
        The full ENML specification can be found in the Evernote API Overview
        at http://dev.evernote.com/documentation/cloud/chapters/ENML.php
        '''
        anote_content = open(anote["content"], "r").readlines()
        note.content = '<?xml version="1.0" encoding="UTF-8"?>'
        note.content += '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
        # TODO: change content from plain text to html
        note.content += '<en-note>' + anote_content + '<br/>'
        if anote.has_key("attachment"):
            note.content += '<en-media type="image/png" hash="' + hashHex + '"/>'
        note.content += '</en-note>'
        print note.content

        # Finally, send the new note to Evernote using the createNote method
        # The new Note object that is returned will contain server-generated
        # attributes such as the new note's unique GUID.
        createdNote = self.noteStore.createNote(self.authToken, note)
        print "Successfully created a new note with GUID: ", createdNote.guid                           
    def list_note(self):
        # List all of the notebooks in the user's account        
        notebooks = self.noteStore.listNotebooks(self.authToken)
        print "Found ", len(notebooks), " notebooks:"
        for notebook in notebooks:
            print "  * ", notebook.name
        print                                            

if __name__ == "__main__":
   
    parser = OptionParser()
    parser.add_option("-c", "--check", action="store_true", dest="check_flag",
            help="check version of evernote")     
    parser.add_option("-l", "--list", action="store_true", dest="list_flag",
            help="list all notes in notebook")    
    parser.add_option("-a", "--add", action="store_true", dest="add_flag",
            help="create a new note")  
    parser.add_option("-d", "--delete", action="store", dest="dnoteid",
            help="delete a exist note")                       
    parser.add_option("-r", "--read", action="store", dest="rnoteid",
            help="read a exist note")                       
    parser.add_option("-u", "--update", action="store", dest="upnoteid",
            help="update a exist note")
         
    (options, args) = parser.parse_args()

    vnote_config = {}
    vnote_config = eval(open(os.path.expanduser("~/.vnoterc"), 'r').read())  
    vnote = Vnote(vnote_config)
     
    if options.check_flag:
        vnote.check_version()
     
    if options.list_flag:
        vnote.list_note()

    if options.add_flag:
        # Get file need to upload
        anote = {}
        anote = eval(open(os.path.expanduser("~/.vnote/index"), 'r').read())  
        vnote.add(anote)
    """
    if options.dnoteid != 0:
        vnote.delete(options.dnoteid)
                  
    if options.rnoteid != 0:
        vnote.display(options.rnoteid)
                  
    if options.upnoteid != 0:
        vnote.update(options.upnoteid)
    """    
