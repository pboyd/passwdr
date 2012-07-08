import sys
import argparse

import kernel
import events
import ops

from receiver import Receiver

class PassmanUI(Receiver):
    def __init__(self):
        ops.account.Account().register()
        self.register()

    def events(self):
        return [ events.AccountList,
                 events.AccountFound ]

    def _handle_AccountList(self, event):
        print "Account List"
        for account in event.accounts:
            print "%-15s %s" % (account.key(), account.note())

    def _handle_AccountFound(self, event):
        acct = event.account
        print acct.key()
        if acct.note():
            print acct.note()

        print ""
        print "Username: %s" % (acct.username())
        print "Password: %s" % (acct.password())

    def run(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("command")
        parser.add_argument("args", nargs='*')
        args = parser.parse_args()

        method_name = "_command_%s" % args.command
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            method(args.args)
        else:
            sys.stderr.write("error: Unknown command \"%s\"\n" % args.command)

        kernel.run()
        kernel.join()

    def _command_list(self, args):
        kernel.queue(events.GetAccountList())

    def _command_show(self, args):
        if len(args) == 0:
            print "usage: show account_key"
            return

        key = args[0]
        kernel.queue(events.FindAccountByKey(args[0]))

if __name__ == "__main__":
    PassmanUI().run()
