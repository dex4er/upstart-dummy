'''
Created on Aug 26, 2010

@author: gyp
'''

import re

class UpstartConfigParser(object):
    '''
    This class loads and parses Upstart config files. It can be used similarily to Python's builtin ConfigParser:
    you create an instance, read() the configfile and get() the various entries. Saving and other miscellanneous 
    things are not supported. It only cares about known "stanzas" and simply skips over the unknown ones. Note
    that it doesn't parse "start on" and "stop on" entries currently.
    '''


    def __init__(self):
        # NOTE: start and stop can actually be multiline, but it'd hard to parse properly and we don't use it anyway, so
        # we just don't parse it...
        self.simple_stanzas = ["instance", "description", "author", "version", "env", "export", # "start on", "stop on", 
                               "emits", "exec", "expect", "task", "kill", "respawn", "normal", "console", "umask",
                               "nice", "oom", "limit" ,"chroot", "chdir", "pre-start exec", "post-start exec", "pre-stop exec",
                               "post-stop exec"]

        # these all end with "end script"
        self.multiline_stanzas = ["script", "pre-start script", "post-start script", "pre-stop script", "post-stop script"]


        self.reset()
        
    def reset(self):
        self.values = {}
    
    def read(self, filename):
        '''
        Opens and parses the configuration file
        '''
        f = open(filename, 'r')
        
        line = f.readline()
        while line != '':
            # cut out the ending whitespace and comments, skip empty lines
            if '#' in line:
                [content, comment] = line.split('#', 1)
            else:
                content = line
            content = content.strip()
            if len(content) == 0:
                line = f.readline()
                continue
            
            stanza = False
            args = ''
            for stanza_to_check in self.simple_stanzas:
                if content.startswith(stanza_to_check):
                    stanza = stanza_to_check
                    args = content[len(stanza_to_check)+1:].strip(' \t"')
                    break
                
            for stanza_to_check in self.multiline_stanzas:
                if content.startswith(stanza_to_check):
                    stanza = stanza_to_check
                    args = []
                    
                    while True:
                        argline = f.readline()
                        if argline == '' or argline.strip() == 'end script':
                            break
                        else:
                            if len(argline.strip()) > 0:
                                args.append(argline.strip())
                    
                    break                

            if stanza:
                self.values[stanza] = args
                
            line = f.readline()
            
        f.close()

    def get(self, stanza):
        try:
            ret = self.values[stanza]
        except KeyError:
            ret = None
        return ret

    def stanzas(self):
        return self.values.keys()
    
    def dump(self):
        print self.values