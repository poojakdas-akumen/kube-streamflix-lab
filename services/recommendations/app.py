from flask import Flask, jsonify

app = Flask(__name__)

PICKS = [
    {"id": 8, "title": "Red Planet Cafe",
     "reason": "Because you like futuristic stories"},
    {"id": 5, "title": "Ocean of Stars",
     "reason": "A highly rated adventure"},
    {"id": 6, "title": "Midnight Library",
     "reason": "For your next mystery night"}
]

@app.get("/health")
def health():
    return {"status": "ok", "service": "recommendations"}

@app.get("/api/recommendations")
def recommendations():
    return jsonify(PICKS)

@app.get("/")
def root():
    return {"service": "recommendations", "status": "running"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)