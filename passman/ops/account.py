import kernel, events
import os
import persistance

from receiver import Receiver

class Account(Receiver):
    def __init__(self):
        self._path = os.path.expanduser("~/.passman")

    def events(self):
        return [ events.GetAccountList,
                 events.FindAccountByKey,
                 events.NewAccount,
                 events.DeleteAccount ]

    def _load(self):
        if not os.path.isfile(self._path):
            with file(self._path, 'w'):
                pass

        return persistance.read(self._path)

    def _handle_GetAccountList(self, event):
        accounts = self._load()
        kernel.queue(events.AccountList(accounts))

    def _handle_FindAccountByKey(self, event):
        accounts = self._load()

        a = self._find_by_key(accounts, event.key)
        if a == None:
            kernel.queue(events.NotFound())
        else:
            kernel.queue(events.AccountFound(a))

    def _handle_NewAccount(self, event):
        accounts = self._load()
        accounts.append(event.account)
        persistance.write(self._path, accounts)

        kernel.queue(events.Success("Account created"))

    def _handle_DeleteAccount(self, event):
        accounts = self._load()
        a = self._find_by_key(accounts, event.key)

        if a == None:
            kernel.queue(events.NotFound())
            return

        accounts.remove(a)
        persistance.write(self._path, accounts)

        kernel.queue(events.Success("Account removed"))

    def _find_by_key(self, accounts, key):
        for acct in accounts:
            if acct.key() == key:
                return acct

        return None

