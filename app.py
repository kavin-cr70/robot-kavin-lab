from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Global shared storage list for all devices
shared_leaderboard = [
    {"name": "kavin", "class": "8th", "score": "15/15", "time": "41s"},
    {"name": "Jerrold", "class": "7th", "score": "15/15", "time": "37s"}
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/leaderboard", methods=["GET"])
def get_leaderboard():
    # Return sorted scores
    return jsonify(shared_leaderboard)

@app.route("/api/leaderboard", methods=["POST"])
def add_score():
    data = request.get_json()
    if data and "name" in data and "score" in data:
        new_entry = {
            "name": data["name"],
            "class": data.get("class", "8th"),
            "score": data["score"],
            "time": data.get("time", "")
        }
        # Add to the beginning of the list
        shared_leaderboard.insert(0, new_entry)
        return jsonify({"status": "success", "leaderboard": shared_leaderboard}), 200
        
    return jsonify({"status": "error", "message": "Invalid data"}), 400

if __name__ == "__main__":
    app.run(debug=True)
