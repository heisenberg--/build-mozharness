import subprocess
import sys
import unittest

try:
    import json
except:
    import simplejson as json

import config

class TestConfig(unittest.TestCase):
    def _getJsonConfig(self, filename="configs/test/test.json",
                       output='dict'):
        fh = open(filename)
        contents = json.load(fh)
        fh.close()
        if 'output' == 'dict':
            return dict(contents)
        else:
            return contents
    
    def testConfig(self):
        c = config.BaseConfig(initial_config_file='test/test.json')
        content_dict = self._getJsonConfig()
        for key in content_dict.keys():
            self.assertEqual(content_dict[key], c._config[key])
    
    def testDumpConfig(self):
        c = config.BaseConfig(initial_config_file='test/test.json')
        dump_config_output = c.dumpConfig()
        dump_config_dict = json.loads(dump_config_output)
        content_dict = self._getJsonConfig()
        for key in content_dict.keys():
            self.assertEqual(content_dict[key], dump_config_dict[key])

    def testReadOnlyDict(self):
        control_dict = {
         'b':'2',
         'c':{'d': '4'},
         'e':['f', 'g'],
        }
        r = config.ReadOnlyDict(control_dict)
        self.assertEqual(r, control_dict,
                             msg="can't transfer dict to ReadOnlyDict")
        r.popitem()
        self.assertEqual(len(r), len(control_dict) - 1,
                         msg="can't popitem() ReadOnlyDict when unlocked")
        r = config.ReadOnlyDict(control_dict)
        r.pop('e')
        self.assertEqual(len(r), len(control_dict) - 1,
                         msg="can't pop() ReadOnlyDict when unlocked")
        r = config.ReadOnlyDict(control_dict)
        r['e'] = 'yarrr'
        self.assertEqual(r['e'], 'yarrr',
                         msg="can't set var in ReadOnlyDict when unlocked")
        del r['e']
        self.assertEqual(len(r), len(control_dict) - 1,
                         msg="can't del in ReadOnlyDict when unlocked")
        r.clear()
        self.assertEqual(r, {},
                             msg="can't clear() ReadOnlyDict when unlocked")
        for key in control_dict.keys():
            r.setdefault(key, control_dict[key])
        self.assertEqual(r, control_dict,
                             msg="can't setdefault() ReadOnlyDict when unlocked")
        r = config.ReadOnlyDict(control_dict)
        r.lock()
        # TODO use |with self.assertRaises(AssertionError):| if/when we're
        # all on 2.7.
        try:
            r['e'] = 2
        except:
            pass
        else:
            self.assertIsNotNone(None, msg="can set r['e'] when locked")
        try:
            del r['e']
        except:
            pass
        else:
            self.assertIsNotNone(None, "can del r['e'] when locked")
        self.assertRaises(AssertionError, r.popitem)
        self.assertRaises(AssertionError, r.update, {})
        self.assertRaises(AssertionError, r.setdefault, {})
        self.assertRaises(AssertionError, r.pop)
        self.assertRaises(AssertionError, r.clear)
