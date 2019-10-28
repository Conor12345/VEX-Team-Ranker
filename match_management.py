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
                c.execute("INSERT INTO tblMatches VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (EventID, match["matchnum"], match["round"], match["red1"], match["red2"], match["red3"], match["blue1"], match["blue2"], match["blue3"], match["redsit"], match["bluesit"], match["redscore"], match["bluescore"]))
                db.commit()
                for teamNum in ["red1", "red2", "red3", "blue1", "blue2", "blue3"]:
                    if match[teamNum] != "":
                        if not team_management.check_team_presence(match[teamNum]):
                            team_management.import_team(match[teamNum])

