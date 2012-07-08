import kernel, events
import os
import persistance

class Account:
    def __init__(self):
        self._path = os.path.expanduser("~/.passman")

    def register(self):
        kernel.subscribe(events.GetAccountList, self)
        kernel.subscribe(events.FindAccountByKey, self)

    def receive_event(self, event):
        if isinstance(event, events.GetAccountList):
            self._get_account_list()
        elif isinstance(event, events.FindAccountByKey):
            self._find_account_by_key(event.key)

    def _load(self):
        if not os.path.isfile(self._path):
            with file(self._path, 'w'):
                pass

        return persistance.read(self._path)

    def _get_account_list(self):
        accounts = self._load()
        kernel.queue(events.AccountList(accounts))

    def _find_account_by_key(self, key):
        accounts = self._load()
        for a in accounts:
            if a.key() == key:
                kernel.queue(events.AccountFound(a))

        kernel.queue(events.NotFound())

