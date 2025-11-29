# app.py
import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

SPORTMONKS_KEY = os.environ.get("SPORTMONKS_KEY")        # your SportMonks token
SOFASCORE_API_URL = os.environ.get("SOFASCORE_API_URL")  # if you want to call a SofaScore-ish URL
# e.g. "https://api.sofascore.com/api/v1/" (or blank if not using)

@app.route("/")
def home():
    return {"status": "Basketball Predictor Running"}

def get_from_sportmonks(team_name):
    """
    Example generic fetch - SportMonks endpoints vary by sport/version.
    This is a template: replace endpoint path with the correct SportMonks basketball endpoint
    if/when you confirm it from their docs.
    """
    if not SPORTMONKS_KEY:
        return None, "no sportmonks key"
    # example endpoint template (you may need to change the path to the correct basketball one)
    url = "https://api.sportmonks.com/v3/basketball/teams/search"  # <-- verify in docs
    params = {"api_token": SPORTMONKS_KEY, "search": team_name}
    try:
        r = requests.get(url, params=params, timeout=8)
        r.raise_for_status()
        return r.json(), None
    except Exception as e:
        return None, str(e)

def get_from_sofascore(team_name):
    """If you insist on SofaScore, call whatever URL you stored in SOFASCORE_API_URL."""
    if not SOFASCORE_API_URL:
        return None, "no sofascore url configured"
    params = {"q": team_name}
    try:
        r = requests.get(SOFASCORE_API_URL, params=params, timeout=8, headers={
            "User-Agent": "Mozilla/5.0 (compatible)"
        })
        r.raise_for_status()
        return r.json(), None
    except Exception as e:
        return None, str(e)

@app.route("/predict", methods=["GET"])
def predict():
    team1 = request.args.get("team1")
    team2 = request.args.get("team2")

    if not team1 or not team2:
        return jsonify({"error": "Missing team1 or team2"}), 400

    # Try SportMonks first
    sm1, err1 = get_from_sportmonks(team1)
    sm2, err2 = get_from_sportmonks(team2)

    # fallback: SofaScore if SportMonks failed
    if sm1 is None or sm2 is None:
        sofa1, e1 = get_from_sofascore(team1)
        sofa2, e2 = get_from_sofascore(team2)
    else:
        sofa1 = sofa2 = None

    # For now we just return what we got (you will parse & use actual fields)
    return jsonify({
        "team1": team1,
        "team2": team2,
        "sportmonks_team1": sm1 if sm1 else None,
        "sportmonks_err_team1": err1,
        "sportmonks_team2": sm2 if sm2 else None,
        "sportmonks_err_team2": err2,
        "sofascore_team1": sofa1,
        "sofascore_err_team1": e1 if 'e1' in locals() else None,
        "sofascore_team2": sofa2,
        "sofascore_err_team2": e2 if 'e2' in locals() else None,
        "prediction": "System active"
    })