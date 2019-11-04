import sqlite3
import api_query, match_management
from datetime import date
from dateutil.relativedelta import relativedelta

def check_event_presence(EventID):
    db = sqlite3.connect("database.db")
    c = db.cursor()

    results = c.execute('SELECT * FROM tblEvents WHERE EventID=(?)', (EventID,))
    db.commit()
    return len(results.fetchall()) == 1

def import_event(query): # Loads event data base upon a query such as "Country=United Kingdom&season=Turning Point"
    data = api_query.get_event_data(query) # Query the API using a function
    if not data: # Ensures the API has returned some data
        return False
    else:
        db = sqlite3.connect("database.db") # Loading database
        c = db.cursor()
        for event in data: # Checks each event return by database query
            if not check_event_presence(event["sku"]): # Checks if the event is already present in the event database
                c.execute("INSERT INTO tblEvents VALUES (?, ?, ?, ?, ?, ?)", (event["sku"], event["name"], event["loc_city"], event["loc_postcode"], event["season"], event["start"][0:10]))
                db.commit()
                match_management.import_match(event["sku"]) # Passes the EventID to the match import function to import all matches which took place at the event
            else:
                refresh_event(event["sku"]) # Updates the data if it is already in the database

def refresh_event(EventID): # Updates the data for the specified event
    db = sqlite3.connect("database.db")
    c = db.cursor()
    c.execute('DELETE FROM tblEvents WHERE EventID = (?)', (EventID,)) # Removes the event from the database
    c.execute('DELETE FROM tblMatches WHERE EventID = (?)', (EventID,))
    db.commit()
    import_event("sku=" + EventID) # Imports the event as if it was never present

def refresh_recent_events():
    dateCheck = date.today() + relativedelta(months=-6)
    db = sqlite3.connect("database.db")
    c = db.cursor()
    results = c.execute("SELECT EventID FROM tblEvents where Date > (?)", (dateCheck,))
    for event in results.fetchall():
         if not match_management.check_event_has_matches(event[0]):
             refresh_event(event[0])