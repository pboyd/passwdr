import kernel, events
import os
import persistance

class Account:
    def __init__(self):
        self._path = os.path.expanduser("~/.passman")

    def register(self):
        kernel.subscribe(events.GetAccountList, self)

    def receive_event(self, event):
        if isinstance(event, events.GetAccountList):
            self._get_account_list()

    def _get_account_list(self):
        accounts = self._load()
        kernel.queue(events.AccountList(accounts))

    def _load(self):
        if not os.path.isfile(self._path):
            with file(self._path, 'w'):
                pass

        return persistance.read(self._path)
