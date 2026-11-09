import os
import sqlite3
from flask import Flask, jsonify, request, send_from_directory

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "leaderboard.db")

app = Flask(__name__)


def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con


with db() as con:
    con.execute(
        """CREATE TABLE IF NOT EXISTS scores (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL,
               classVal TEXT NOT NULL,
               score INTEGER NOT NULL,
               time INTEGER NOT NULL
           )"""
    )


@app.route("/")
def home():
    return send_from_directory(BASE, "index.html")


@app.route("/api/leaderboard", methods=["GET"])
def get_scores():
    with db() as con:
        rows = con.execute(
            "SELECT name, classVal, score, time FROM scores "
            "ORDER BY score DESC, time ASC LIMIT 100"
        ).fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/api/leaderboard", methods=["POST"])
def add_score():
    data = request.get_json(silent=True) or {}
    try:
        score = int(data.get("score"))
        secs = int(data.get("time"))
    except (TypeError, ValueError):
        return jsonify({"error": "bad score or time"}), 400
    name = str(data.get("name", "")).strip()[:30]
    cls = str(data.get("classVal", "")).strip()[:30]
    if not name or not 0 <= score <= 15 or not 0 <= secs <= 86400:
        return jsonify({"error": "invalid entry"}), 400
    with db() as con:
        con.execute(
            "INSERT INTO scores (name, classVal, score, time) VALUES (?,?,?,?)",
            (name, cls or "-", score, secs),
        )
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
