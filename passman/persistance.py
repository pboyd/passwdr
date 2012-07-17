from account import Account
from ConfigParser import SafeConfigParser

def write(path, accounts):
    with open(path, 'wb') as fp:
        return writefp(fp, accounts)

def writefp(fp, accounts):
    config = SafeConfigParser()
    for a in accounts:
        config.add_section(a.key())

        if a.username():
            config.set(a.key(), 'username', a.username())

        crypted = a.encryptedPassword()
        if crypted:
            config.set(a.key(), 'password', crypted)

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
        acct = Account(key, encryption_key)

        if config.has_option(key, 'username'):
            acct.setUsername(config.get(key, 'username'))

        if config.has_option(key, 'password'):
            acct.setEncryptedPassword(config.get(key, 'password'))

        if config.has_option(key, 'note'):
            acct.setNote(config.get(key, 'note'))

        accounts.append(acct)

    return accounts
