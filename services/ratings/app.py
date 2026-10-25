from flask import Flask, jsonify, request

app = Flask(__name__)

REVIEWS = [
    {"id": 1, "movie_id": 1, "user": "Maya",
     "score": 5, "comment": "Beautiful world-building."},
    {"id": 2, "movie_id": 2, "user": "Arun",
     "score": 5, "comment": "A clever, tense story."},
    {"id": 3, "movie_id": 4, "user": "Sam",
     "score": 4, "comment": "Fast and fun."}
]

@app.get("/health")
def health():
    return {"status": "ok", "service": "ratings"}

@app.get("/api/ratings")
def ratings():
    movie_id = request.args.get("movie_id", type=int)
    result = REVIEWS if movie_id is None else [
        review for review in REVIEWS if review["movie_id"] == movie_id
    ]
    return jsonify(result)

@app.post("/api/ratings")
def add_rating():
    data = request.get_json(silent=True) or {}
    try:
        movie_id = int(data["movie_id"])
        score = int(data["score"])
        user = str(data.get("user", "Guest"))[:40]
        comment = str(data.get("comment", ""))[:300]
        if score < 1 or score > 5:
            raise ValueError()
    except (KeyError, ValueError, TypeError):
        return {"error": "movie_id and score (1-5) are required"}, 400

    item = {
        "id": max([r["id"] for r in REVIEWS], default=0) + 1,
        "movie_id": movie_id,
        "user": user,
        "score": score,
        "comment": comment
    }
    REVIEWS.append(item)
    return item, 201

@app.get("/")
def root():
    return {"service": "ratings", "status": "running"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)