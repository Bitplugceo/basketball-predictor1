import requests

def get_live_match(team1, team2):
    url = f"https://api.sofascore.com/api/v1/search/all?q={team1}%20{team2}"
    r = requests.get(url).json()

    try:
        events = r["events"]
        if not events:
            return None
        
        event_id = events[0]["id"]

        match_url = f"https://api.sofascore.com/api/v1/event/{event_id}"
        match_data = requests.get(match_url).json()

        return match_data
    except:
        return None
