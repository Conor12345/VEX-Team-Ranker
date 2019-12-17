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
    eventID = event_management.get_eventID(EventName)
    matchData = match_management.import_match(eventID, True)
    if matchData != False:
        teams = []
        for match in matchData:
            if match["round"] == 1:
                for team in ["red1", "red2", "red3", "blue1", "blue2", "blue3"]:
                    if match[team] != "" and match[team] not in teams:
                        teams.append(match[team])
        if len(teams) != 0:
            return sorted(teams)
        else:
            teams = []
            for match in matchData:
                for team in ["red1", "red2", "red3", "blue1", "blue2", "blue3"]:
                    if match[team] != "" and match[team] not in teams:
                        teams.append(match[team])
            return sorted(teams)
    else:
        return []

def get_team_skill(TeamNum):
    if not check_team_presence(TeamNum):
        return False
    db = sqlite3.connect("database.db")
    c = db.cursor()
    return c.execute('SELECT * FROM tblTeams where TeamNum = (?)', (TeamNum,)).fetchall()[0][4]