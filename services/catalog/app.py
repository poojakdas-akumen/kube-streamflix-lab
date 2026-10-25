from flask import Flask, jsonify

app = Flask(__name__)

MOVIES = [
    {"id": 1, "title": "Neon Skies", "genre": "Sci-Fi", "year": 2025,
     "rating": 4.8, "description": "A pilot discovers a city above the clouds.", "color": "violet"},
    {"id": 2, "title": "The Last Signal", "genre": "Thriller", "year": 2024,
     "rating": 4.6, "description": "A radio operator receives a message from tomorrow.", "color": "blue"},
    {"id": 3, "title": "Paper Moons", "genre": "Drama", "year": 2023,
     "rating": 4.4, "description": "Two strangers rebuild a forgotten cinema.", "color": "pink"},
    {"id": 4, "title": "Wild Circuit", "genre": "Action", "year": 2025,
     "rating": 4.7, "description": "A courier races through a smart city.", "color": "orange"},
    {"id": 5, "title": "Ocean of Stars", "genre": "Adventure", "year": 2022,
     "rating": 4.5, "description": "A deep-sea crew finds an impossible signal.", "color": "teal"},
    {"id": 6, "title": "Midnight Library", "genre": "Mystery", "year": 2024,
     "rating": 4.3, "description": "A library predicts the future.", "color": "indigo"},
    {"id": 7, "title": "Small Wonders", "genre": "Comedy", "year": 2023,
     "rating": 4.2, "description": "An inventors club takes on a giant problem.", "color": "yellow"},
    {"id": 8, "title": "Red Planet Cafe", "genre": "Sci-Fi", "year": 2025,
     "rating": 4.6, "description": "A cafe on Mars becomes a galactic hotspot.", "color": "red"}
]

@app.get("/health")
def health():
    return {"status": "ok", "service": "catalog"}

@app.get("/api/catalog")
def catalog():
    return jsonify(MOVIES)

@app.get("/")
def root():
    return {"service": "catalog", "status": "running"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)