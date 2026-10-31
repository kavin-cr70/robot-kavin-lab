from flask import Flask, render_template, request, jsonify
import os
import json

app = Flask(__name__)

DATA_FILE = "leaderboard.json"

def load_scores():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    # Default initial scores if file doesn't exist
    return [
        {"name": "kavin", "classVal": "8th", "score": 15, "time": 41, "date": "1st Place"},
        {"name": "Jerrold", "classVal": "7th", "score": 15, "time": 37, "date": "1st Place"}
    ]

def save_scores(scores):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(scores, f)
    except Exception:
        pass

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/leaderboard", methods=["GET"])
def get_leaderboard():
    scores = load_scores()
    # Sort scores: highest score first, then lowest time
    scores.sort(key=lambda x: (int(x["score"]), -int(x["time"])), reverse=True)
    return jsonify(scores)

@app.route("/api/leaderboard", methods=["POST"])
def add_score():
    data = request.get_json()
    if data and "name" in data and "score" in data:
        scores = load_scores()
        new_entry = {
            "name": data["name"],
            "classVal": data.get("classVal", "8th"),
            "score": data["score"],
            "time": data.get("time", 0),
            "date": data.get("date", "")
        }
        scores.append(new_entry)
        scores.sort(key=lambda x: (int(x["score"]), -int(x["time"])), reverse=True)
        save_scores(scores)
        return jsonify({"status": "success", "leaderboard": scores}), 200
        
    return jsonify({"status": "error", "message": "Invalid data"}), 400

if __name__ == "__main__":
    app.run(debug=True)
