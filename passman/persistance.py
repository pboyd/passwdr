from account import Account
from ConfigParser import SafeConfigParser

from Crypto import Random
from Crypto.Cipher import AES

def write(path, accounts):
    with open(path, 'wb') as fp:
        return writefp(fp, accounts)

def writefp(fp, accounts, encryption_key=None):
    config = SafeConfigParser()
    for a in accounts:
        config.add_section(a.key())

        if a.username():
            config.set(a.key(), 'username', a.username())

        if a.password():
            password = a.password()
            if encryption_key:
                password = _encrypt(encryption_key, password)

            config.set(a.key(), 'password', password)

        if a.note():
            config.set(a.key(), 'note', a.note())

    config.write(fp)

def read(path):
    with open(path, 'rb') as fp:
        return readfp(fp)

def readfp(fp, encryption_key=None):
    config = SafeConfigParser()
    config.readfp(fp)

    accounts = []

    for key in config.sections():
        acct = Account(key)

        if config.has_option(key, 'username'):
            acct.setUsername(config.get(key, 'username'))

        if config.has_option(key, 'password'):
            password = config.get(key, 'password')
            if encryption_key:
                password = _decrypt(encryption_key, password)
            acct.setPassword(password)

        if config.has_option(key, 'note'):
            acct.setNote(config.get(key, 'note'))

        accounts.append(acct)

    return accounts

def _pad_key(key):
    # The encryption key needs to be 16, 24 or 32 bytes. Padding it to make the
    # length. Or if it's more than 32 bytes, truncating it.

    def pad(key, length):
        return key + ('0' * (length-len(key)))

    length = len(key)
    if length < 16:
        return pad(key, 16)
    elif length > 16 and length < 24:
        return pad(key, 24)
    elif length > 24 and length < 32:
        return pad(key, 32)
    elif length > 32:
        return key[0:32]

    return length

def _encrypt(key, plaintext):
    key = _pad_key(key)

    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    return iv + cipher.encrypt(plaintext)

def _decrypt(key, cryptotext):
    key = _pad_key(key)
    iv = cryptotext[0:AES.block_size]
    cryptotext = cryptotext[AES.block_size:len(cryptotext)]

    cipher = AES.new(key, AES.MODE_CFB, iv)
    return cipher.decrypt(cryptotext)
