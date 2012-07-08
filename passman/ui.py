import sys
import argparse

import kernel
import events
import ops

class PassmanUI:
    def __init__(self):
        ops.account.Account().register()
        self.register()

    def register(self):
        kernel.subscribe(events.AccountList, self)
        kernel.subscribe(events.AccountFound, self)

    def receive_event(self, event):
        if isinstance(event, events.AccountList):
            self._show_accounts(event.accounts)
        elif isinstance(event, events.AccountFound):
            self._show_account(event.account)

    def _show_accounts(self, accounts):
        print "Account List"
        for account in accounts:
            print "%-15s %s" % (account.key(), account.note())

    def _show_account(self, account):
        print account.key()
        if account.note():
            print account.note()

        print ""
        print "Username: %s" % (account.username())
        print "Password: %s" % (account.password())

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
