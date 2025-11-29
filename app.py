from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

SOFA_HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

@app.route("/")
def home():
    return jsonify({"status": "API running", "usage": "/predict?team1=Arsenal&team2=Chelsea"})

def get_team(team_name):
    url = f"https://api.sofascore.com/api/v1/search/all?q={team_name}"
    r = requests.get(url, headers=SOFA_HEADERS)
    data = r.json()

    for item in data.get("results", []):
        if item.get("entityType") == "team":
            return item["entity"]

    return None


def get_last_5_matches(team_id):
    url = f"https://api.sofascore.com/api/v1/team/{team_id}/events/last/0"
    r = requests.get(url, headers=SOFA_HEADERS)
    data = r.json().get("events", [])
    return data[:5]


@app.route("/predict", methods=["GET"])
def predict():
    team1 = request.args.get("team1")
    team2 = request.args.get("team2")

    if not team1 or not team2:
        return jsonify({"error": "team1 and team2 are required"}), 400

    t1 = get_team(team1)
    t2 = get_team(team2)

    if not t1:
        return jsonify({"error": f"Team 1 '{team1}' not found"}), 404

    if not t2:
        return jsonify({"error": f"Team 2 '{team2}' not found"}), 404

    t1_last5 = get_last_5_matches(t1["id"])
    t2_last5 = get_last_5_matches(t2["id"])

    return jsonify({
        "team1": t1,
        "team2": t2,
        "team1_last_5": t1_last5,
        "team2_last_5": t2_last5
    })
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)