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

    def receive_event(self, event):
        if isinstance(event, events.AccountList):
            self._show_accounts(event.accounts)

    def _show_accounts(self, accounts):
        print "Account List"
        for account in accounts:
            print "%-15s %s" % (account.key(), account.note())

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

if __name__ == "__main__":
    PassmanUI().run()
