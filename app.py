from flask import Flask, render_template, request, jsonify
import os
import json

app = Flask(__name__)

DATA_FILE = 'leaderboard.json'

# Helper function to load scores from file
def load_scores():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return []

# Helper function to save scores to file
def save_scores(scores):
    with open(DATA_FILE, 'w') as f:
        json.dump(scores, f)

@app.route("/")
def home():
    return render_template("index.html")

# Endpoint to get current leaderboard
@app.route("/api/leaderboard", methods=["GET"])
def get_leaderboard():
    scores = load_scores()
    return jsonify(scores)

# Endpoint to submit a new score
@app.route("/api/leaderboard", methods=["POST"])
def add_score():
    data = request.get_json()
    if data and "name" in data and "score" in data:
        scores = load_scores()
        
        # Add new entry
        new_entry = {
            "name": data["name"],
            "class": data.get("class", "8th"),
            "score": data["score"],
            "time": data.get("time", "")
        }
        scores.append(new_entry)
        
        # Save back to file
        save_scores(scores)
        return jsonify({"status": "success", "leaderboard": scores}), 200
        
    return jsonify({"status": "error", "message": "Invalid data"}), 400

if __name__ == "__main__":
    app.run(debug=True)
