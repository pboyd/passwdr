from Crypto import Random
from Crypto.Cipher import AES

class Account:
    def __init__(self, key, enc_key=None):
        self.setKey(key)
        self.setEncryptionKey(enc_key)
        self.setNote(None)
        self.setUsername(None)
        self.setPassword(None)
        self.setEncryptedPassword(None)

    def key(self):
        return self._key

    def setKey(self, value):
        self._key = value

    def setEncryptionKey(self, key):
        if key == None:
            self._encryption_key = None
            return

        # The encryption key needs to be 16, 24 or 32 bytes. Padding it to make the
        # length. Or if it's more than 32 bytes, truncating it.

        def pad(key, length):
            return key + ('0' * (length-len(key)))

        length = len(key)
        if length < 16:
            key = pad(key, 16)
        elif length > 16 and length < 24:
            key = pad(key, 24)
        elif length > 24 and length < 32:
            key = pad(key, 32)
        elif length > 32:
            key = key[0:32]

        self._encryption_key = key

    def note(self):
        return self._note

    def setNote(self, value):
        self._note = value

    def username(self):
        return self._username

    def setUsername(self, value):
        self._username = value

    def password(self):
        if self._password:
            return self._password
        elif self._encrypted_password and self._encryption_key:
            return self._decrypt(self._encryption_key, self._encrypted_password)
        else:
            # If neither of the above are set, then this is probably an un-encrypted file
            return self._encrypted_password

    def setPassword(self, value):
        self._password = value
        # Setting a new password invalidates the previous encrypted password
        self._encrypted_password = None

    def encryptedPassword(self):
        if self._encrypted_password:
            return self._encrypted_password
        elif self._password and self._encryption_key:
            return self._encrypt(self._encryption_key, self._password)
        else:
            return None

    def setEncryptedPassword(self, value):
        self._encrypted_password = value

    def _encrypt(self, key, plaintext):
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CFB, iv)
        return iv + cipher.encrypt(plaintext)

    def _decrypt(self, key, cryptotext):
        iv = cryptotext[0:AES.block_size]
        if len(iv) < AES.block_size:
            # Value wasn't encrypted
            return cryptotext

        cryptotext = cryptotext[AES.block_size:len(cryptotext)]

        cipher = AES.new(key, AES.MODE_CFB, iv)
        return cipher.decrypt(cryptotext)
