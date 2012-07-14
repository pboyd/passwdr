class Event():
    def __init__(self):
        pass

class GetAccountList(Event):
    pass

class AccountList(Event):
    def __init__(self, accounts):
        self.accounts = accounts
        Event.__init__(self)

class FindAccountByKey(Event):
    def __init__(self, key):
        self.key = key
        Event.__init__(self)

class AccountFound(Event):
    def __init__(self, account):
        self.account = account
        Event.__init__(self)

class NewAccount(Event):
    def __init__(self, account):
        self.account = account
        Event.__init__(self)

class DeleteAccount(Event):
    def __init__(self, key):
        self.key = key
        Event.__init__(self)

class UpdateAccountField(Event):
    def __init__(self, key, field, value):
        self.key = key
        self.field = field
        self.value = value
        Event.__init__(self)

class Success(Event):
    def __init__(self, message):
        self.message = message
        Event.__init__(self)

class NotFound(Event):
    pass
