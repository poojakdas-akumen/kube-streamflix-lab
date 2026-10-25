import os
import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)
DB_PATH = os.getenv("DB_PATH", "/data/watchlist.db")

def connect():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS watchlist (
            movie_id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            genre TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn

@app.get("/health")
def health():
    try:
        conn = connect()
        conn.close()
        return {"status": "ok", "service": "watchlist"}
    except Exception as exc:
        return {"status": "error", "detail": str(exc)}, 500

@app.get("/api/watchlist")
def get_watchlist():
    conn = connect()
    rows = conn.execute("""
        SELECT movie_id AS id, title, genre
        FROM watchlist ORDER BY title
    """).fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.post("/api/watchlist")
def add_item():
    data = request.get_json(silent=True) or {}
    try:
        movie_id = int(data["id"])
        title = str(data["title"])[:120]
        genre = str(data.get("genre", "Unknown"))[:60]
        if not title:
            raise ValueError()
    except (KeyError, ValueError, TypeError):
        return {"error": "Provide a numeric id and title"}, 400

    conn = connect()
    try:
        conn.execute("""
            INSERT OR REPLACE INTO watchlist(movie_id, title, genre)
            VALUES (?, ?, ?)
        """, (movie_id, title, genre))
        conn.commit()
    finally:
        conn.close()

    return {"status": "added", "id": movie_id}, 201

@app.delete("/api/watchlist/<int:movie_id>")
def remove_item(movie_id):
    conn = connect()
    conn.execute("DELETE FROM watchlist WHERE movie_id = ?", (movie_id,))
    conn.commit()
    conn.close()
    return {"status": "removed", "id": movie_id}

@app.get("/")
def root():
    return {"service": "watchlist", "status": "running"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)