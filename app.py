# app.py
import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

SPORTMONKS_KEY = os.environ.get("SPORTMONKS_KEY")

# -------------------------
# Fetch team ID by name
# -------------------------
def get_team_id(team_name):
    try:
        url = f"https://api.sportmonks.com/v3/basketball/teams/search/{team_name}"
        params = {"api_token": SPORTMONKS_KEY}
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()

        if "data" in data and len(data["data"]) > 0:
            return data["data"][0]["id"], None
        return None, "Team not found"
    except Exception as e:
        return None, str(e)


# -------------------------
# Fetch last 5 matches
# -------------------------
def get_team_last5(team_id):
    try:
        url = f"https://api.sportmonks.com/v3/basketball/teams/{team_id}?include=latest.events"
        params = {"api_token": SPORTMONKS_KEY}
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()

        results = []

        if "data" in data and "latest" in data["data"]:
            events = data["data"]["latest"]["events"]
            for ev in events[:5]:
                results.append(ev.get("result_info", "N/A"))

        return results, None
    except Exception as e:
        return None, str(e)


# -------------------------
# Simple Prediction Logic
# -------------------------
def make_prediction(team1_results, team2_results):
    t1_wins = team1_results.count("win")
    t2_wins = team2_results.count("win")

    if t1_wins > t2_wins:
        return "Team 1 likely wins"
    elif t2_wins > t1_wins:
        return "Team 2 likely wins"
    else:
        return "Tight game — no clear favorite"


@app.route("/")
def home():
    return {"status": "Basketball Predictor Running"}


@app.route("/predict", methods=["GET"])
def predict():
    team1 = request.args.get("team1")
    team2 = request.args.get("team2")

    if not team1 or not team2:
        return jsonify({"error": "Missing team1 or team2"}), 400

    # Get team IDs
    t1_id, err = get_team_id(team1)
    if err:
        return jsonify({"error": f"Team1 error: {err}"}), 400

    t2_id, err = get_team_id(team2)
    if err:
        return jsonify({"error": f"Team2 error: {err}"}), 400

    # Get last 5 results
    t1_last5, err = get_team_last5(t1_id)
    if err:
        return jsonify({"error": f"Team1 last5 error: {err}"}), 400

    t2_last5, err = get_team_last5(t2_id)
    if err:
        return jsonify({"error": f"Team2 last5 error: {err}"}), 400

    # Prediction
    prediction = make_prediction(t1_last5, t2_last5)

    return jsonify({
        "team1": team1,
        "team2": team2,
        "team1_last5": t1_last5,
        "team2_last5": t2_last5,
        "prediction": prediction
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)