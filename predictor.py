def make_prediction(data):
    stats = data["event"]["homeTeamStatistics"]

    home = data["event"]["homeTeam"]["name"]
    away = data["event"]["awayTeam"]["name"]
    score = data["event"].get("homeScore", {}).get("current", 0), data["event"].get("awayScore", {}).get("current", 0)

    # Basic logic (I will upgrade later)
    prediction = "Over 160.5" if stats["points"]["avg"] > 80 else "Under 160.5"

    return {
        "home": home,
        "away": away,
        "score": score,
        "prediction": prediction
    }
