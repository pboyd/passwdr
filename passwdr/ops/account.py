import kernel, events
import os
import persistance

from receiver import Receiver

class Account(Receiver):
    def __init__(self):
        self._path = os.path.expanduser("~/.passwdr")

    def events(self):
        return [ events.GetAccountList,
                 events.FindAccountByKey,
                 events.NewAccount,
                 events.DeleteAccount,
                 events.UpdateAccountField ]

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
            a.setEncryptionKey(event.encryption_key)
            kernel.queue(events.AccountFound(a))

    def _handle_NewAccount(self, event):
        accounts = self._load()
        accounts.append(event.account)

        if self._has_duplicate_keys(accounts):
            return

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

    def _handle_UpdateAccountField(self, event):
        accounts = self._load()
        a = self._find_by_key(accounts, event.key)

        if a == None:
            kernel.queue(events.NotFound())
            return

        if event.field == "password":
            a.setEncryptionKey(event.encryption_key)
            a.setPassword(event.value)
        else:
            setter = "set%s" % (event.field.title())
            if hasattr(a, setter):
                method = getattr(a, setter)
                method(event.value)

        if self._has_duplicate_keys(accounts):
            return

        persistance.write(self._path, accounts)

        kernel.queue(events.Success("Account updated"))

    def _find_by_key(self, accounts, key):
        for acct in accounts:
            if acct.key() == key:
                return acct

        return None

    def _has_duplicate_keys(self, accounts):
        keys = {}
        for acct in accounts:
            if acct.key() in keys:
                kernel.queue(events.DuplicateKeyError(acct.key()))
                return True

            keys[acct.key()] = 1

        return False
