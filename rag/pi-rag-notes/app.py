from __future__ import annotations

from flask import Flask, jsonify, render_template, request

from rag_engine import RagEngine


app = Flask(__name__)
engine = RagEngine()


@app.get("/")
def index():
    return render_template("index.html", chunk_count=len(engine.chunks))


@app.get("/api/status")
def status():
    return jsonify({"chunk_count": len(engine.chunks)})


@app.post("/api/add")
def add_notes():
    payload = request.get_json(silent=True) or {}
    text = str(payload.get("text", ""))
    chunks = engine.add_document(text)
    return jsonify({"added": len(chunks), "chunk_count": len(engine.chunks)})


@app.post("/api/ask")
def ask():
    payload = request.get_json(silent=True) or {}
    question = str(payload.get("question", ""))
    return jsonify(engine.answer(question))


@app.post("/api/sample")
def sample():
    added = engine.load_sample_dataset()
    return jsonify({"added": added, "chunk_count": len(engine.chunks)})


@app.post("/api/ship-systems")
def ship_systems():
    added = engine.load_ship_systems_dataset()
    return jsonify({"added": added, "chunk_count": len(engine.chunks)})


@app.post("/api/reset")
def reset():
    engine.reset()
    return jsonify({"chunk_count": len(engine.chunks)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=False)
