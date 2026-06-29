# pi-rag-notes

`pi-rag-notes` is a beginner-friendly local web app that demonstrates Retrieval-Augmented Generation ideas with vectors. It runs on a Raspberry Pi with Flask, scikit-learn, JSON storage, and plain HTML/CSS/JavaScript.

It uses no OpenAI API, no LangChain, no vector database, no Docker, no cloud service, and no API keys.

## What the app does

- Lets you paste notes or load a fake sample engineering dataset.
- Splits notes into chunks of about 500 characters.
- Converts chunks into TF-IDF vectors with scikit-learn.
- Converts a question into the same vector space.
- Uses cosine similarity to retrieve the top 3 matching chunks.
- Shows similarity scores for each retrieved chunk.
- Creates a clearly labeled simple extractive answer from the retrieved chunks.
- Persists chunks locally in `knowledge_base.json` so the app still works after restart.
- Provides a reset button to clear the knowledge base.

## Why this demonstrates RAG and vectors

RAG systems retrieve relevant context before producing an answer. In a production RAG app, retrieved chunks are often sent to a large language model. This demo keeps everything local and replaces the LLM step with a simple extractive answer so students can see the retrieval process directly.

The vector search uses TF-IDF. TF-IDF is not a neural embedding model, but it still turns text into vectors that can be compared mathematically. That makes it a good classroom-friendly way to explain chunking, vectors, cosine similarity, and retrieval.

## Setup on Raspberry Pi

From the project folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

The app runs on:

```text
http://0.0.0.0:5050
```

On the Raspberry Pi itself, open:

```text
http://localhost:5050
```

From another computer on the same network, open:

```text
http://<raspberry-pi-ip-address>:5050
```

You can find the Pi's IP address with:

```bash
hostname -I
```

## Example questions to try

Load the sample dataset, then ask:

- How do I check pump vibration?
- What port does the Raspberry Pi demo use?
- What should I check if ship interface messages stop?
- How do I fix calendar sync problems?
- Why are meetings showing the wrong time?

## Run tests

```bash
source .venv/bin/activate
pytest
```

## Troubleshooting

- If `flask` or `sklearn` cannot be imported, activate the virtual environment and run `pip install -r requirements.txt`.
- If another service is using port 5050, stop that service or change the port in `app.py`.
- If the browser cannot connect from another computer, confirm both devices are on the same network and that the app is running on `0.0.0.0`.
- If results look weak, add more notes or ask questions using words that appear in the stored notes. TF-IDF is simple and works best when terms overlap.
- To clear all stored data, use the reset button or delete `knowledge_base.json`.
