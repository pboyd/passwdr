class Event():
    def __init__(self):
        pass

class GetAccountList(Event):
    def __init__(self):
        Event.__init__(self)

class AccountList(Event):
    def __init__(self, accounts):
        self.accounts = accounts
        Event.__init__(self)
