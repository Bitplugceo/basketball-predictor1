from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return {"status": "Basketball Predictor Running"}

@app.route("/predict", methods=["GET"])
def predict():
    team1 = request.args.get("team1")
    team2 = request.args.get("team2")

    if not team1 or not team2:
        return jsonify({"error": "Missing team1 or team2"}), 400

    return jsonify({
        "team1": team1,
        "team2": team2,
        "prediction": "System active"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)