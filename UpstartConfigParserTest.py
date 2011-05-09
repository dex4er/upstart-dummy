'''
Created on Aug 26, 2010

@author: gyp
'''
import unittest
import os, sys
sys.path.append('../../../fixups/core/')
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
                                        'env': {'INIT_VERBOSE': True}
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
                                            },
                        'munin-node.conf': {
                                            'expect': 'fork',
                                            'respawn': '',
                                            'pre-start script': 
                                                ['mkdir -p /var/run/munin',
                                                 'chown munin:munin /var/run/munin',
                                                 'chmod 0755 /var/run/munin'],
                                            'script':
                                                ['[ -r /etc/default/munin-node ] && . /etc/default/munin-node',
                                                 'exec $DAEMON $DAEMON_ARGS'
                                                 ],
                                            'env' : {'DAEMON' : '/usr/sbin/munin-node',
                                                     'TESTENV' : '/this/is/a/testenv'
                                                    }
                                            }
                       }
        pass


    def testParseFiles(self):
        for filename in os.listdir('fixups/upstart_test_configs/'):

            parser = UpstartConfigParser()
            parser.read("fixups/upstart_test_configs/%s" % filename)

            if filename in self.checks.keys():
                for (checkkey, checkvalue) in self.checks[filename].iteritems():
                    if checkvalue == '__IS_LIST__':
                        self.assertTrue(isinstance(parser.get(checkkey), (list)))
                    else:
                        self.assertEqual(checkvalue, parser.get(checkkey))



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
