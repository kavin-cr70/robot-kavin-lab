from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

NPOINT_URL = "https://api.npoint.io/e96acb369bbc02c72723"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/leaderboard", methods=["GET"])
def get_leaderboard():
    try:
        res = requests.get(NPOINT_URL)
        if res.status_code == 200:
            scores = res.json()
            scores.sort(key=lambda x: (int(x["score"]), -int(x["time"])), reverse=True)
            return jsonify(scores)
    except Exception:
        pass
    return jsonify([])

@app.route("/api/leaderboard", methods=["POST"])
def add_score():
    data = request.get_json()
    if data and "name" in data and "score" in data:
        try:
            res = requests.get(NPOINT_URL)
            scores = res.json() if res.status_code == 200 else []
            
            new_entry = {
                "name": data["name"],
                "classVal": data.get("classVal", "8th"),
                "score": data["score"],
                "time": data.get("time", 0),
                "date": data.get("date", "")
            }
            scores.append(new_entry)
            scores.sort(key=lambda x: (int(x["score"]), -int(x["time"])), reverse=True)
            
            requests.put(NPOINT_URL, json=scores)
            return jsonify({"status": "success", "leaderboard": scores}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
                
    return jsonify({"status": "error", "message": "Invalid data"}), 400

if __name__ == "__main__":
    app.run(debug=True)
