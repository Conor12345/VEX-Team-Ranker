import sqlite3
import api_query

def check_team_presence(TeamNum): # returns true if present
    db = sqlite3.connect("database.db")
    c = db.cursor()

    results = c.execute('SELECT * FROM tblTeams WHERE TeamNum=(?)', (TeamNum,))
    db.commit()
    return len(results.fetchall()) == 1

def import_team(TeamNum, skillRating = 0): #import team into tbl Team
    data = api_query.get_team_data(TeamNum)
    if not data:
        return False
    else:
        db = sqlite3.connect("database.db")
        c = db.cursor()
        c.execute('INSERT INTO tblTeams VALUES (?,?,?,?,?)', (TeamNum, data[0], data[1], data[2], skillRating))
        db.commit()

def refresh_team(TeamNum):
    if not check_team_presence(TeamNum):
        return False
    db = sqlite3.connect("database.db")
    c = db.cursor()
    skill = c.execute('SELECT * FROM tblTeams where TeamNum = (?)', (TeamNum,)).fetchall()[0][4]
    print(skill)
    c.execute('DELETE FROM tblTeams WHERE TeamNum = (?)', (TeamNum,))
    db.commit()
    import_team(TeamNum, skill)