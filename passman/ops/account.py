import kernel, events
import os
import persistance

from receiver import Receiver

class Account(Receiver):
    def __init__(self):
        self._path = os.path.expanduser("~/.passman")

    def events(self):
        return [ events.GetAccountList,
                 events.FindAccountByKey ]

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
        for a in accounts:
            if a.key() == event.key:
                kernel.queue(events.AccountFound(a))

        kernel.queue(events.NotFound())

