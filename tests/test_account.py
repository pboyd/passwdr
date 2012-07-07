import unittest

import sys
import os
sys.path.append(os.path.abspath('%s/../..' % (__file__)))

from passman.account import Account

class AccountTest(unittest.TestCase):
    def testConstructor(self):
        a = Account('key')
        self.assertEqual(a.key(), 'key')

    def testNote(self):
        a = Account('key')
        self.assertEqual(a.note(), None)

        a.setNote('a note')
        self.assertEqual(a.note(), 'a note')

    def testUsername(self):
        a = Account('key')
        self.assertEqual(a.username(), None)

        a.setUsername('a user')
        self.assertEqual(a.username(), 'a user')

    def testPassword(self):
        a = Account('key')
        self.assertEqual(a.password(), None)

        a.setPassword('a pass')
        self.assertEqual(a.password(), 'a pass')

if __name__ == "__main__":
    unittest.main()
