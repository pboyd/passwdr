import unittest
import tempfile
from ConfigParser import SafeConfigParser

import sys
import os
sys.path.append(os.path.abspath('%s/../..' % (__file__)))

from passman import persistance
from passman.account import Account

class PersistanceTest(unittest.TestCase):
    def testWritefp(self):
        a = Account('the_key')
        a.setNote('the note')
        a.setUsername('the username')
        a.setPassword('the password')

        f = tempfile.TemporaryFile()
        persistance.writefp(f, [a])
        f.seek(0)

        config = SafeConfigParser()
        config.readfp(f)

        self.assertEqual(config.sections(), ['the_key'])
        self.assertEqual(config.get('the_key', 'note'), 'the note')
        self.assertEqual(config.get('the_key', 'username'), 'the username')
        self.assertEqual(config.get('the_key', 'password'), 'the password')

        f.close

    def testMissingFields(self):
        a = Account('the_key')

        f = tempfile.TemporaryFile()
        persistance.writefp(f, [a])
        f.seek(0)

        accounts = persistance.readfp(f)
        self.assertEqual(len(accounts), 1)

        found = accounts[0]

        self.assertEqual(found.key(), 'the_key')
        self.assertEqual(found.note(), None)
        self.assertEqual(found.username(), None)
        self.assertEqual(found.password(), None)

        f.close

    def testReadfp(self):
        f = tempfile.TemporaryFile()

        for i in range(3):
            f.write("[key%i]\n" % (i))
            f.write("note=note%i\n" % (i))
            f.write("username=username%i\n" % (i))
            f.write("password=password%i\n" % (i))
            f.write("\n")

        f.seek(0)

        accounts = persistance.readfp(f)
        self.assertEqual(len(accounts), 3)

        i = 0
        for a in accounts:
            self.assertEqual(a.username(), 'username%i' % (i))
            self.assertEqual(a.password(), 'password%i' % (i))
            self.assertEqual(a.note(), 'note%i' % (i))
            i += 1

    def testWriteRead(self):
        a = Account('the_key')
        a.setNote('the note')
        a.setUsername('the username')
        a.setPassword('the password')

        path = os.path.join(tempfile.tempdir, 'write_test')

        persistance.write(path, [a])
        self.assertTrue(os.path.isfile(path))

        accounts = persistance.read(path)
        self.assertEqual(len(accounts), 1)

        os.unlink(path)

    def testEncryption(self):
        a = Account('the_key')
        a.setUsername('user')
        a.setPassword('pass')

        f = tempfile.TemporaryFile()

        # write it with an encryption key
        persistance.writefp(f, [a], 'encryption key')
        f.seek(0)

        # read it un-encrypted
        accounts = persistance.readfp(f)

        self.assertNotEqual(accounts[0].password(), 'pass')

    def testDecryption(self):
        a = Account('the_key')
        a.setUsername('user')
        a.setPassword('pass')

        f = tempfile.TemporaryFile()

        key = 'encryption key'
        persistance.writefp(f, [a], key)
        f.seek(0)
        accounts = persistance.readfp(f, key)

        self.assertEqual(accounts[0].password(), 'pass')


if __name__ == "__main__":
    unittest.main()
