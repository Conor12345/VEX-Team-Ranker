import binascii
import hashlib
import os
import sqlite3

import team_management


def hash_password(password):
    # source https://www.vitoshacademy.com/hashing-passwords-in-python/
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password):
    # source https://www.vitoshacademy.com/hashing-passwords-in-python/
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

def create_user(UserName: str, Password: str, TeamNum: str, Admin: int):
    PassW = hash_password(Password)

    if not team_management.check_team_presence(TeamNum): # Checks to see if the team is already in tblTeams
        if not team_management.import_team(TeamNum): # IF not in table, add team to tabl
            return False

    db = sqlite3.connect("database.db")
    c = db.cursor()
    c.execute('INSERT INTO tblUsers (UserName, Password, TeamNum, Admin) VALUES (?, ?, ?, ?)'   ,(UserName, PassW, TeamNum, Admin))
    db.commit()
    return True

def get_user_data(UserName):
    db = sqlite3.connect("database.db")
    c = db.cursor()

    result = c.execute("SElECT * FROM tblUsers WHERE UserName = (?)", (UserName,)).fetchall()
    db.commit()
    if len(result) == 0:
        return False
    else:
        return list(result[0])

def is_admin(UserName):
    return get_user_data(UserName)[4] == 1

def verify_user_login(UserName, Password):
    user = get_user_data(UserName)
    if not user:
        return False
    else:
        return verify_password(user[2], Password)

def update_user_password(UserName, NewPassword):
    db = sqlite3.connect("database.db")
    c = db.cursor()
    c.execute('UPDATE tblUsers set Password=? where UserName=?', (hash_password(NewPassword), UserName))
    db.commit()

def update_user_data(CurrentUserName, NewUserName=None, NewTeamNum=None, NewAdmin=None):
    if NewTeamNum is not None:
        db = sqlite3.connect("database.db")
        c = db.cursor()
        c.execute('UPDATE tblUsers set TeamNum=? where UserName=?', (NewTeamNum, CurrentUserName))
        db.commit()

    if NewAdmin is not None:
        db = sqlite3.connect("database.db")
        c = db.cursor()
        c.execute('UPDATE tblUsers set Admin=? where UserName=?', (NewAdmin, CurrentUserName))
        db.commit()

    if NewUserName is not None:
        db = sqlite3.connect("database.db")
        c = db.cursor()
        c.execute('UPDATE tblUsers set UserName=? where UserName=?', (NewUserName, CurrentUserName))
        db.commit()

def delete_user(UserName):
    db = sqlite3.connect("database.db")
    c = db.cursor()
    c.execute("DELETE FROM tblUsers WHERE UserName = ?", (UserName,))
    db.commit()