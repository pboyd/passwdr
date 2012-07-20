class Event():
    def __init__(self, session):
        self.session = session

class GetAccountList(Event):
    pass

class AccountList(Event):
    def __init__(self, accounts, session):
        self.accounts = accounts
        Event.__init__(self, session)

class FindAccountByKey(Event):
    def __init__(self, key, session):
        self.key = key
        Event.__init__(self, session)

class AccountFound(Event):
    def __init__(self, account, session):
        self.account = account
        Event.__init__(self, session)

class NewAccount(Event):
    def __init__(self, account, session):
        self.account = account
        Event.__init__(self, session)

class DeleteAccount(Event):
    def __init__(self, key, session):
        self.key = key
        Event.__init__(self, session)

class UpdateAccountField(Event):
    def __init__(self, key, field, value, session):
        self.key = key
        self.field = field
        self.value = value
        Event.__init__(self, session)

class DuplicateKeyError(Event):
    def __init__(self, key, session):
        self.key = key
        Event.__init__(self, session)

class Success(Event):
    def __init__(self, message, session):
        self.message = message
        Event.__init__(self, session)

class NotFound(Event):
    pass
