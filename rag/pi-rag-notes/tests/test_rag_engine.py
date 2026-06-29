from rag_engine import RagEngine
from storage import JsonChunkStorage


def make_engine(tmp_path):
    return RagEngine(JsonChunkStorage(tmp_path / "kb.json"))


def test_chunking_splits_long_text(tmp_path):
    engine = make_engine(tmp_path)
    chunks = engine.split_text("word " * 240, chunk_size=500)

    assert len(chunks) >= 3
    assert all(len(chunk) <= 500 for chunk in chunks)


def test_add_document_persists_chunks(tmp_path):
    storage = JsonChunkStorage(tmp_path / "kb.json")
    engine = RagEngine(storage)

    added = engine.add_document("Raspberry Pi uses Python and Flask for this local demo.")
    restarted = RagEngine(storage)

    assert len(added) == 1
    assert len(restarted.chunks) == 1
    assert "Raspberry Pi" in restarted.chunks[0]["text"]


def test_retrieves_relevant_chunk(tmp_path):
    engine = make_engine(tmp_path)
    engine.add_document("Pump maintenance includes vibration checks and seal inspection.")
    engine.add_document("Calendar troubleshooting includes timezone and browser session checks.")

    results = engine.search("How do I check pump vibration?")

    assert results
    assert "Pump maintenance" in results[0].text
    assert results[0].score > 0


def test_empty_knowledge_base_returns_no_results(tmp_path):
    engine = make_engine(tmp_path)

    assert engine.search("What is stored?") == []
    answer = engine.answer("What is stored?")
    assert answer["results"] == []
    assert answer["chunk_count"] == 0


def test_ship_systems_dataset_retrieves_ballast_notes(tmp_path):
    engine = make_engine(tmp_path)

    added = engine.load_ship_systems_dataset()
    results = engine.search("What does ballast water do for ship stability?")

    assert added >= 10
    assert results
    assert "Ballast water" in results[0].text
    assert "imo.org" in results[0].source
