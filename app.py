from flask import Flask, render_template, request, jsonify
import urllib.request
import json

app = Flask(__name__)

# Free Public Cloud Storage (JSONBin public endpoint)
CLOUD_URL = "https://api.jsonbin.io/v3/b/66f8d098acd3cb34a88d44e5"

# Helper function to load scores from cloud
def load_scores():
    try:
        req = urllib.request.Request(CLOUD_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return data.get("record", [])
    except Exception as e:
        print("Error reading cloud storage:", e)
        return []

# Helper function to save scores to cloud
def save_scores(scores):
    try:
        req = urllib.request.Request(
            CLOUD_URL,
            data=json.dumps(scores).encode('utf-8'),
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0"
            },
            method="PUT"
        )
        with urllib.request.urlopen(req) as response:
            return True
    except Exception as e:
        print("Error saving cloud storage:", e)
        return False

@app.route("/")
def home():
    return render_template("index.html")

# Get leaderboard endpoint
@app.route("/api/leaderboard", methods=["GET"])
def get_leaderboard():
    scores = load_scores()
    return jsonify(scores)

# Add score endpoint
@app.route("/api/leaderboard", methods=["POST"])
def add_score():
    data = request.get_json()
    if data and "name" in data and "score" in data:
        scores = load_scores()
        
        # Format entry
        new_entry = {
            "name": data["name"],
            "class": data.get("class", "8th"),
            "score": data["score"],
            "time": data.get("time", "")
        }
        scores.append(new_entry)
        
        # Sort scores highest to lowest
        scores.sort(key=lambda x: int(x["score"]), reverse=True)
        
        save_scores(scores)
        return jsonify({"status": "success", "leaderboard": scores}), 200
        
    return jsonify({"status": "error", "message": "Invalid data"}), 400

if __name__ == "__main__":
    app.run(debug=True)
