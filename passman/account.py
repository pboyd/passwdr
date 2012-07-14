class Account:
    def __init__(self, key):
        self.setKey(key)
        self.setNote(None)
        self.setUsername(None)
        self.setPassword(None)

    def key(self):
        return self._key

    def setKey(self, value):
        self._key = value

    def note(self):
        return self._note

    def setNote(self, value):
        self._note = value

    def username(self):
        return self._username

    def setUsername(self, value):
        self._username = value

    def password(self):
        return self._password

    def setPassword(self, value):
        self._password = value
