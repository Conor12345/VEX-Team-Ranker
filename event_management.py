import sqlite3
import api_query, match_management

def check_event_presence(EventID):
    db = sqlite3.connect("database.db")
    c = db.cursor()

    results = c.execute('SELECT * FROM tblEvents WHERE EventID=(?)', (EventID,))
    db.commit()
    return len(results.fetchall()) == 1

def import_event(query):
    data = api_query.get_event_data(query)
    if not data:
        return False
    else:
        db = sqlite3.connect("database.db")
        c = db.cursor()
        for event in data:
            if not check_event_presence(event["sku"]):
                c.execute("INSERT INTO tblEvents VALUES (?, ?, ?, ?, ?, ?)", (event["sku"], event["name"], event["loc_city"], event["loc_postcode"], event["season"], event["start"][0:10]))
                db.commit()
                match_management.import_match(event["sku"])
            else:
                refresh_event(event["sku"])

def refresh_event(EventID):
    db = sqlite3.connect("database.db")
    c = db.cursor()
    c.execute('DELETE FROM tblEvents WHERE EventID = (?)', (EventID,))
    db.commit()
    import_event("sku=" + EventID)
