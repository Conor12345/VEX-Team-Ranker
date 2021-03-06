import sqlite3
from datetime import date

from dateutil.relativedelta import relativedelta

import api_query
import match_management


def check_event_presence(EventID):
    db = sqlite3.connect("database.db")
    c = db.cursor()

    results = c.execute('SELECT * FROM tblEvents WHERE EventID=(?)', (EventID,))
    db.commit()
    return len(results.fetchall()) == 1


def import_event(query):  # Loads event data base upon a query such as "Country=United Kingdom&season=Turning Point"
    data = api_query.get_event_data(query)  # Query the API using a function
    if not data:  # Ensures the API has returned some data
        return False
    else:
        db = sqlite3.connect("database.db")  # Loading database
        c = db.cursor()
        for event in data:  # Checks each event return by database query
            if not check_event_presence(event["sku"]):  # Checks if the event is already present in the event database
                c.execute("INSERT INTO tblEvents VALUES (?, ?, ?, ?, ?, ?, ?)",
                          (event["sku"], event["name"], event["loc_city"], event["loc_postcode"], event["season"], event["start"][0:10], event["loc_country"]))
                db.commit()
                match_management.import_match(event["sku"])  # Passes the EventID to the match import function to import all matches which took place at the event
            elif not match_management.check_event_has_matches(event["sku"]):
                refresh_event(event["sku"])  # Updates the data if it is already in the database


def refresh_event(EventID):  # Updates the data for the specified event
    db = sqlite3.connect("database.db")
    c = db.cursor()
    c.execute('DELETE FROM tblEvents WHERE EventID = (?)', (EventID,))  # Removes the event from the database
    c.execute('DELETE FROM tblMatches WHERE EventID = (?)', (EventID,))
    db.commit()
    import_event("sku=" + EventID)  # Imports the event as if it was never present


def refresh_recent_events():
    dateCheck = date.today() + relativedelta(months=-6) # Gets the date six months ago
    db = sqlite3.connect("database.db")
    c = db.cursor()
    results = c.execute("SELECT EventID FROM tblEvents where Date > (?)", (dateCheck,)) # Collects EventID for recent events
    for event in results.fetchall(): # Iterates through recent events
        if not match_management.check_event_has_matches(event[0]): # Checks if the event has any matches
            refresh_event(event[0]) # Attempts to import matches if none exist
    import_event("season=current&country=United Kingdom") # Import any new events from this season


def get_event_list(country, season, sku=False):
    if sku:
        column = "EventID"
    else:
        column = "EventName"
    db = sqlite3.connect("database.db")
    c = db.cursor()
    results = c.execute("SELECT " + column + " FROM tblEvents WHERE Country=(?) and Season=(?)", (country, season)).fetchall()
    data = []
    for event in results:
        data.append(event[0])
    return data


def get_eventID(eventName):
    db = sqlite3.connect("database.db")
    c = db.cursor()
    results = c.execute("SELECT EventID FROM tblEvents WHERE EventName = (?)", (eventName,)).fetchall()
    if len(results) == 0:
        return False
    else:
        return results[0][0]


def get_eventName(eventID):
    db = sqlite3.connect("database.db")
    c = db.cursor()
    results = c.execute("SELECT EventName FROM tblEvents WHERE EventID = (?)", (eventID,)).fetchall()
    if len(results) == 0:
        return False
    else:
        return results[0][0]

def get_event_data(eventID):
    db = sqlite3.connect("database.db")
    c = db.cursor()
    results = c.execute("SELECT * FROM tblEvents WHERE EventID = (?)", (eventID,)).fetchall()
    if len(results) == 0:
        return False
    else:
        return results[0]

def get_average_contribution_to_win(TeamNum, Season):
    data = []
    for eventID in get_event_list("United Kingdom", Season, True):
        temp = api_query.get_event_results(eventID, TeamNum)
        if temp != False:
            data.append(temp["ccwm"])
    if len(data) > 0:
        return round(sum(data) / len(data), 2)
    else:
        return 0