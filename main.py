from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Basketball Predictor is running!"

if __name__ == "__main__":
    app.run()
