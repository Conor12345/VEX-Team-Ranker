import sqlite3
from importlib import reload

import api_query
import event_management
import match_management

reload(match_management)

def check_team_presence(TeamNum):  # returns true if present
    db = sqlite3.connect("database.db")
    c = db.cursor()

    results = c.execute('SELECT * FROM tblTeams WHERE TeamNum=(?)', (TeamNum,))
    db.commit()
    return len(results.fetchall()) == 1


def import_team(TeamNum, skillRating=0):  # import team into tbl Team
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
    c.execute('DELETE FROM tblTeams WHERE TeamNum = (?)', (TeamNum,))
    db.commit()
    import_team(TeamNum, skill)


def get_team_list(EventName):
    db = sqlite3.connect("database.db")
    c = db.cursor()
    results = c.execute("SELECT RedTeam1, RedTeam2, BlueTeam1, BlueTeam2 FROM tblMatches "
                        "JOIN tblEvents ON tblMatches.EventID = tblEvents.EventID WHERE EventName=(?)", (EventName,)).fetchall()
    teamList = []
    for match in results:
        teamList += match

    return sorted(list(set(teamList)))

def get_team_skill(TeamNum):
    if not check_team_presence(TeamNum):
        return False
    db = sqlite3.connect("database.db")
    c = db.cursor()
    return c.execute('SELECT * FROM tblTeams where TeamNum = (?)', (TeamNum,)).fetchall()[0][4]