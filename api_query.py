import json
import requests


def get_team_data(TeamNum):
    try:
        response = requests.get("https://api.vexdb.io/v1/get_teams?program=VRC&team=" + TeamNum)
        data = json.loads(response.text)
    except:
        return False
    if data["size"] == 0:
        return False
    else:
        temp = data["result"][0]
        return [temp["team_name"], temp["city"], temp["country"]]

def get_match_data(EventID):
    try:
        response = requests.get("https://api.vexdb.io/v1/get_matches?sku=" + EventID)
        data = json.loads(response.text)
    except:
        return False
    if data["size"] == 0:
        return False
    else:
        return  data["result"]

def get_event_data(query):
    try:
        response = requests.get("https://api.vexdb.io/v1/get_events?program=VRC&" + query)
        data = json.loads(response.text)
    except:
        return False
    if data["size"] == 0:
        return False
    else:
        return  data["result"]

def get_awards(TeamNum):
    try:
        response = requests.get("https://api.vexdb.io/v1/get_awards?team=" + TeamNum)
        data = json.loads(response.text)
    except:
        return False
    return data["result"]

def get_num_awards(TeamNum, Season):
    return len(get_awards(TeamNum, Season))

def get_alt_skill(TeamNum, Season):
    try:
        response = requests.get("https://api.vexdb.io/v1/get_season_rankings?team=" + TeamNum + "&season=" + Season)
        data = json.loads(response.text)
    except:
        return False
    return data["result"][0]["vrating"]

def get_event_results(EventID, TeamNum):
    try:
        response = requests.get("https://api.vexdb.io/v1/get_rankings?team=" + TeamNum + "&sku=" + EventID)
        data = json.loads(response.text)
        return data["result"][0]
    except:
        return False