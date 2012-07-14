import sys
import argparse

import kernel
import events
import ops
from account import Account

from receiver import Receiver

class PassmanUI(Receiver):
    def __init__(self):
        ops.account.Account().register()
        self.register()

    def events(self):
        return [ events.AccountList,
                 events.AccountFound,
                 events.Success,
                 events.NotFound ]

    def _handle_AccountList(self, event):
        for account in event.accounts:
            if account.note():
                print "%-15s %s" % (account.key(), account.note())
            else:
                print "%-15s" % (account.key())

    def _handle_AccountFound(self, event):
        acct = event.account
        print acct.key()
        print "Username: %s" % (acct.username())
        print "Password: %s" % (acct.password())
        print ""

        if acct.note():
            print "Note: %s" % (acct.note())
            print ""

    def _handle_Success(self, event):
        print event.message

    def _handle_NotFound(self, event):
        print "Account not found"

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

    def _command_add(self, args):
        if len(args) < 3:
            print "usage: add account_key username password [note]"
            return

        account = Account(args[0])
        account.setUsername(args[1])
        account.setPassword(args[2])
        if len(args) > 3:
            account.setNote(args[3])

        kernel.queue(events.NewAccount(account))

    def _command_rm(self, args):
        if len(args) == 0:
            print "usage: rm account_key"
            return

        kernel.queue(events.DeleteAccount(args[0]))

    def _command_show(self, args):
        if len(args) == 0:
            print "usage: show account_key"
            return

        kernel.queue(events.FindAccountByKey(args[0]))

    def _command_set(self, args):
        if len(args) != 3:
            print "usage: set account_key field new_value"
            return

        kernel.queue(events.UpdateAccountField(args[0], args[1], args[2]))

if __name__ == "__main__":
    PassmanUI().run()
