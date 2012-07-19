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

    def testEncryption(self):
        a1 = Account('key', 'crypto')
        a1.setPassword('pass')

        # Check that the password is encrypted (or at least obscured)
        encrypted = a1.encryptedPassword()
        self.assertNotEqual(encrypted, None)
        self.assertNotEqual(encrypted, 'pass')

        # Make sure the password can be decrypted
        a2 = Account('key', 'crypto')
        a2.setEncryptedPassword(encrypted)
        self.assertEqual(a2.password(), 'pass')

        # Make sure the password can't be decrypted with the wrong key
        a3 = Account('key', 'wrong key')
        a3.setEncryptedPassword(encrypted)
        self.assertNotEqual(a3.password(), 'pass')

if __name__ == "__main__":
    unittest.main()
