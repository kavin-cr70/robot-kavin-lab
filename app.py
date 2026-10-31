from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Temporary leaderboard storage (stores name and score)
leaderboard_data = [
    {"name": "Kavin", "score": 100},
    {"name": "Player 1", "score": 85}
]

@app.route("/")
def home():
    return render_template("index.html")

# Endpoint to get current leaderboard
@app.route("/api/leaderboard", methods=["GET"])
def get_leaderboard():
    return jsonify(leaderboard_data)

# Endpoint to submit a new score
@app.route("/api/leaderboard", methods=["POST"])
def add_score():
    data = request.get_json()
    if data and "name" in data and "score" in data:
        leaderboard_data.append({"name": data["name"], "score": int(data["score"])})
        # Sort leaderboard highest to lowest
        leaderboard_data.sort(key=lambda x: x["score"], reverse=True)
        return jsonify({"status": "success", "leaderboard": leaderboard_data}), 200
    return jsonify({"status": "error", "message": "Invalid data"}), 400

if __name__ == "__main__":
    app.run(debug=True)
