import unittest

import sys
import os
sys.path.append(os.path.abspath('%s/../../..' % (__file__)))
sys.path.append(os.path.abspath('%s/../../../passwdr' % (__file__)))

import kernel, events
from ops.account import Account

class TestReceiver:
    def __init__(self):
        self.events = {}
        types = [ events.AccountList,
                  events.AccountFound,
                  events.Success,
                  events.NotFound,
                  events.DuplicateKeyError ]

        for et in types:
            kernel.subscribe(et, self)

    def receive_event(self, event):
        self.events[event.__class__.__name__] = event

class AccountTest(unittest.TestCase):
    def setUp(self):
        self.tr = TestReceiver()

    def test_list(self):
        e = events.GetAccountList({})

        a = Account()
        a.receive_event(e)

        kernel.run()
        kernel.join()

        self.assertTrue('AccountList' in self.tr.events)

if __name__ == "__main__":
    unittest.main()
