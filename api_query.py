import json, requests

def get_team_data(TeamNum):
    response = requests.get("https://api.vexdb.io/v1/get_teams?program=VRC&team=" + TeamNum)
    data = json.loads(response.text)
    if data["size"] == 0:
        return False
    else:
        temp = data["result"][0]
        return [temp["team_name"], temp["city"], temp["country"]]

def get_match_data(EventID):
    response = requests.get("https://api.vexdb.io/v1/get_matches?sku=" + EventID)
    data = json.loads(response.text)
    if data["size"] == 0:
        return False
    else:
        return  data["result"]

def get_event_data(query):
    response = requests.get("https://api.vexdb.io/v1/get_events?program=VRC&" + query)
    data = json.loads(response.text)
    if data["size"] == 0:
        return False
    else:
        return  data["result"]