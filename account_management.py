import sqlite3, hashlib, binascii, os
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

def create_user(UserName: str, Password: str, TeamNum: str, Admin: bool):
    PassW = hash_password(Password)

    if Admin: # converts true,false to 1,0
        Adm = 1
    else:
        Adm = 0

    if not team_management.check_team_presence(TeamNum): # Checks to see if the team is already in tblTeams
        team_management.import_team(TeamNum) # IF not in table, add team to table

    db = sqlite3.connect("database.db")
    c = db.cursor()
    c.execute('INSERT INTO tblUsers (UserName, Password, TeamNum, Admin) VALUES (?, ?, ?, ?)'   ,(UserName, PassW, TeamNum, Adm))
    db.commit()

def get_user_data(UserName):
    db = sqlite3.connect("database.db")
    c = db.cursor()

    result = c.execute("SElECT * FROM tblUsers WHERE UserName = (?)", (UserName,)).fetchall()
    db.commit()
    if len(result) == 0:
        return False
    else:
        return list(result[0])