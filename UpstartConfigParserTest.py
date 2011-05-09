'''
Created on Aug 26, 2010

@author: gyp
'''
import unittest
import os
from UpstartConfigParser import *


class UpstartConfigParserTest(unittest.TestCase):

    def setUp(self):
        # NOTE: we only check a tiny part of the config files, but we let it through all the confs the
        # make sure it can handle them
        self.checks = {
                       'ssh.conf': {
                                        'description' : 'OpenSSH server',
                                        'oom': 'never',
                                        'FAKE_STANZA': None
                                    },
                        'rc.conf': {
                                        'author': 'Scott James Remnant <scott@netsplit.com>',
                                        'export': 'PREVLEVEL',
                                        'env': 'INIT_VERBOSE'
                                    },
                        'kdm.conf': {
                                        'emits': 'starting-dm',
                                        'script': '__IS_LIST__'
                                     },
                        'ureadahead.conf': {
                                            'normal': 'exit 0',
                                            'pre-stop exec': 'sleep 45',
                                            'exec': '/sbin/ureadahead --daemon',
                                            'kill': 'timeout 180',
                                            'expect': 'fork'
                                            }
                       }
        pass


    def testParseFiles(self):
        for filename in os.listdir('test_configs/'):

            parser = UpstartConfigParser()
            parser.read("test_configs/%s" % filename)

            if filename in self.checks.keys():
                for (checkkey, checkvalue) in self.checks[filename].iteritems():
                    if checkvalue == '__IS_LIST__':
                        self.assertTrue(isinstance(parser.get(checkkey), (list)))
                    else:
                        self.assertEqual(checkvalue, parser.get(checkkey))



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()