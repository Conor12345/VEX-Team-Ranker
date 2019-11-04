import sqlite3
import api_query
import team_management

def import_match(EventID):
    data = api_query.get_match_data(EventID)
    if not data:
        return False
    else:
        db = sqlite3.connect("database.db")
        c = db.cursor()
        for match in data:
            if match["round"] != 1:
                if match["red3"] == "":
                    del match["red3"]
                    del match["blue3"]
                    del match["redsit"]
                    del match["bluesit"]
                else:
                    teams = []
                    for colour in ["blue", "red"]:
                        team = []
                        for teamnum in range(1,4):
                            team.append(match[colour + str(teamnum)])
                        teams.append(team)
                    teams[0].remove(match["bluesit"])
                    teams[1].remove(match["redsit"])
                    match["blue1"] = teams[0][0]
                    match["blue2"] = teams[0][1]
                    match["red1"] = teams[1][0]
                    match["red2"] = teams[1][1]
                c.execute("INSERT INTO tblMatches VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (EventID, match["matchnum"], match["round"], match["red1"], match["red2"], match["blue1"], match["blue2"], match["redscore"], match["bluescore"]))
                db.commit()
                for teamNum in ["red1", "red2", "blue1", "blue2"]:
                    if match[teamNum] != "":
                        if not team_management.check_team_presence(match[teamNum]):
                            team_management.import_team(match[teamNum])