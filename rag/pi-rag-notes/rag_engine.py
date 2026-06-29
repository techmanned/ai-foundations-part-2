"""Beginner-friendly local RAG/vector search engine.

This intentionally uses TF-IDF instead of neural embeddings so it can run
locally on a Raspberry Pi without API keys or external services.
"""

from __future__ import annotations

import re
import uuid
from dataclasses import dataclass
from typing import Any

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from storage import JsonChunkStorage


SAMPLE_NOTES = [
    {
        "title": "Pump maintenance notes",
        "text": (
            "Pump P-204 should be inspected every Friday. Check vibration, "
            "bearing temperature, seal leakage, and suction pressure. If the "
            "pump sounds rough, clean the inlet strainer and confirm that the "
            "coupling guard is secure before restarting."
        ),
    },
    {
        "title": "Raspberry Pi setup notes",
        "text": (
            "The Raspberry Pi demo runs best with Raspberry Pi OS Lite, Python "
            "3, and a local virtual environment. Enable SSH with raspi-config, "
            "connect to Wi-Fi, update packages, and run Flask on port 5050 so "
            "students can open the app from another computer on the same LAN."
        ),
    },
    {
        "title": "Ship system interface notes",
        "text": (
            "The navigation interface sends heading, speed, and GPS position "
            "to the monitoring display every two seconds. If messages stop, "
            "check the serial adapter, confirm the baud rate is 38400, and "
            "review the interface status page for timeout warnings."
        ),
    },
    {
        "title": "Calendar troubleshooting notes",
        "text": (
            "Calendar sync issues are usually caused by stale browser sessions "
            "or disabled permissions. Sign out, clear site data, sign back in, "
            "and confirm that the calendar integration is allowed to read and "
            "write events. Check timezone settings if meetings appear offset."
        ),
    },
]

SHIP_SYSTEM_NOTES = [
    {
        "title": "SOLAS ship construction, stability, machinery and electrical systems",
        "url": "https://www.imo.org/en/about/conventions/pages/international-convention-for-the-safety-of-life-at-sea-(solas),-1974.aspx",
        "text": (
            "SOLAS Chapter II-1 covers ship construction, subdivision, stability, "
            "machinery, and electrical installations. Passenger ships use watertight "
            "compartments so that, after assumed hull damage, the vessel can remain "
            "afloat and stable. The same safety logic applies to watertight integrity, "
            "bilge pumping arrangements, and emergency conditions. Machinery and "
            "electrical installations should keep essential services available for "
            "the safety of the ship, passengers, and crew."
        ),
    },
    {
        "title": "SOLAS fire protection, detection and extinction systems",
        "url": "https://www.imo.org/en/about/conventions/pages/international-convention-for-the-safety-of-life-at-sea-(solas),-1974.aspx",
        "text": (
            "SOLAS Chapter II-2 covers ship fire protection, fire detection, and fire "
            "extinction. Important design ideas include dividing the ship with thermal "
            "and structural boundaries, separating accommodation spaces from other "
            "areas, limiting combustible materials, detecting a fire in its zone of "
            "origin, containing and extinguishing the fire where it starts, protecting "
            "escape routes, and keeping fire-extinguishing appliances ready for use."
        ),
    },
    {
        "title": "SOLAS radio communication and distress systems",
        "url": "https://www.imo.org/en/about/conventions/pages/international-convention-for-the-safety-of-life-at-sea-(solas),-1974.aspx",
        "text": (
            "SOLAS Chapter IV incorporates the Global Maritime Distress and Safety "
            "System, often called GMDSS. Passenger ships and cargo ships of 300 gross "
            "tonnage and above on international voyages carry radio equipment intended "
            "to improve rescue chances after an accident. Examples include emergency "
            "position-indicating radio beacons, or EPIRBs, and search and rescue "
            "transponders, or SARTs, used to help locate the ship or survival craft."
        ),
    },
    {
        "title": "SOLAS navigation systems, AIS and voyage data recorders",
        "url": "https://www.imo.org/en/about/conventions/pages/international-convention-for-the-safety-of-life-at-sea-(solas),-1974.aspx",
        "text": (
            "SOLAS Chapter V deals with safety of navigation. It covers operational "
            "subjects such as meteorological services for ships, ice patrol, routeing "
            "of ships, search and rescue services, and the master's obligation to "
            "assist persons in distress. It also makes carriage of voyage data "
            "recorders and automatic identification systems, known as VDR and AIS, "
            "mandatory for relevant ships."
        ),
    },
    {
        "title": "Ballast water system purpose and operating value",
        "url": "https://www.imo.org/en/ourwork/environment/pages/ballastwatermanagement.aspx",
        "text": (
            "Ballast water is pumped into ballast tanks to help stabilize a ship at "
            "sea and maintain safe operating conditions during a voyage. Ballast can "
            "reduce stress on the hull, provide transverse stability, improve "
            "propulsion and manoeuvrability, and compensate for changing weight as "
            "cargo, fuel, and fresh water are loaded, consumed, or discharged."
        ),
    },
    {
        "title": "Ballast water environmental risk and invasive species",
        "url": "https://www.imo.org/en/ourwork/environment/pages/ballastwatermanagement.aspx",
        "text": (
            "Ballast water can also move marine species between ports. Organisms such "
            "as bacteria, microbes, larvae, eggs, cysts, and small invertebrates may "
            "survive inside ballast tanks and establish populations after discharge. "
            "This can create ecological, economic, and health problems by introducing "
            "invasive species that compete with local species and damage fisheries, "
            "aquaculture, tourism, infrastructure, and biodiversity."
        ),
    },
    {
        "title": "MARPOL oily bilge water and oily water separator",
        "url": "https://www.imo.org/en/ourwork/environment/pages/oilpollution-default.aspx",
        "text": (
            "MARPOL Annex I addresses oil pollution from ships. For machinery-space "
            "bilges, operational oily water is controlled through equipment such as "
            "the oily water separator. The familiar 15 ppm standard is associated "
            "with allowable discharge of processed bilge water. A shipboard bilge "
            "system therefore matters for both safety, by removing water from spaces, "
            "and environmental compliance, by controlling oily discharge."
        ),
    },
    {
        "title": "MARPOL oil tanker ballast, segregated ballast tanks and double hulls",
        "url": "https://www.imo.org/en/ourwork/environment/pages/oilpollution-default.aspx",
        "text": (
            "MARPOL introduced important tanker design and operating changes to reduce "
            "oil pollution. New oil tankers were required to use segregated ballast "
            "tanks so ballast water did not need to be carried in cargo oil tanks. "
            "Later requirements for double hulls on newer tankers further improved "
            "marine environmental protection by adding separation between cargo oil "
            "and the sea after damage."
        ),
    },
    {
        "title": "Ship cargo and dangerous goods systems",
        "url": "https://www.imo.org/en/about/conventions/pages/international-convention-for-the-safety-of-life-at-sea-(solas),-1974.aspx",
        "text": (
            "SOLAS cargo chapters cover hazards created by cargo type and cargo "
            "handling. Cargo systems need correct stowage and securing so cargo units "
            "do not shift and endanger the ship. Dangerous goods require classification, "
            "packing, marking, labelling, placarding, documentation, stowage, and "
            "segregation. Chemical tankers and gas carriers have additional construction "
            "and equipment requirements under specialized IMO codes."
        ),
    },
    {
        "title": "Ship safety management and operational responsibility",
        "url": "https://www.imo.org/en/about/conventions/pages/international-convention-for-the-safety-of-life-at-sea-(solas),-1974.aspx",
        "text": (
            "SOLAS Chapter IX makes the International Safety Management Code mandatory. "
            "The ISM Code requires a safety management system for the company or "
            "shipowner responsible for operating the ship. In practice, ship systems "
            "are not only machinery and electronics; they also include procedures, "
            "maintenance records, drills, defined responsibilities, and checks that "
            "help the crew operate safely."
        ),
    },
]


@dataclass
class SearchResult:
    id: str
    text: str
    source: str
    score: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "text": self.text,
            "source": self.source,
            "score": round(self.score, 4),
        }


class RagEngine:
    def __init__(self, storage: JsonChunkStorage | None = None) -> None:
        self.storage = storage or JsonChunkStorage()
        self.chunks = self.storage.load_chunks()
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.matrix = None
        self._rebuild_vectors()

    def split_text(self, text: str, chunk_size: int = 500) -> list[str]:
        cleaned = re.sub(r"\s+", " ", text).strip()
        if not cleaned:
            return []

        chunks: list[str] = []
        remaining = cleaned
        while len(remaining) > chunk_size:
            split_at = remaining.rfind(" ", 0, chunk_size)
            if split_at < int(chunk_size * 0.6):
                split_at = chunk_size
            chunks.append(remaining[:split_at].strip())
            remaining = remaining[split_at:].strip()

        if remaining:
            chunks.append(remaining)
        return chunks

    def add_document(self, text: str, source: str = "Pasted notes") -> list[dict[str, Any]]:
        new_chunks = [
            {"id": str(uuid.uuid4()), "text": chunk, "source": source}
            for chunk in self.split_text(text)
        ]
        if not new_chunks:
            return []

        self.chunks.extend(new_chunks)
        self.storage.save_chunks(self.chunks)
        self._rebuild_vectors()
        return new_chunks

    def load_sample_dataset(self) -> int:
        added = 0
        for note in SAMPLE_NOTES:
            added += len(self.add_document(note["text"], source=note["title"]))
        return added


    def load_ship_systems_dataset(self) -> int:
        added = 0
        for note in SHIP_SYSTEM_NOTES:
            source = f"{note['title']} ({note['url']})"
            added += len(self.add_document(note["text"], source=source))
        return added

    def reset(self) -> None:
        self.chunks = []
        self.matrix = None
        self.storage.reset()

    def search(self, question: str, top_k: int = 3) -> list[SearchResult]:
        if not question.strip() or not self.chunks or self.matrix is None:
            return []

        query_vector = self.vectorizer.transform([question])
        scores = cosine_similarity(query_vector, self.matrix).flatten()
        ranked_indexes = scores.argsort()[::-1][:top_k]

        results: list[SearchResult] = []
        for index in ranked_indexes:
            score = float(scores[index])
            if score <= 0:
                continue
            chunk = self.chunks[int(index)]
            results.append(
                SearchResult(
                    id=str(chunk.get("id", "")),
                    text=str(chunk.get("text", "")),
                    source=str(chunk.get("source", "Unknown")),
                    score=score,
                )
            )
        return results

    def answer(self, question: str) -> dict[str, Any]:
        results = self.search(question)
        if not results:
            return {
                "answer": (
                    "No relevant chunks were found. Add notes to the knowledge "
                    "base or try a question using words from the stored notes."
                ),
                "results": [],
                "chunk_count": len(self.chunks),
            }

        combined = " ".join(result.text for result in results)
        answer = self._shorten_answer(combined)
        return {
            "answer": answer,
            "results": [result.to_dict() for result in results],
            "chunk_count": len(self.chunks),
        }

    def _shorten_answer(self, text: str, max_sentences: int = 3) -> str:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        summary = " ".join(sentence for sentence in sentences[:max_sentences] if sentence)
        return summary or text[:500]

    def _rebuild_vectors(self) -> None:
        texts = [str(chunk.get("text", "")) for chunk in self.chunks if chunk.get("text")]
        if not texts:
            self.matrix = None
            return
        self.matrix = self.vectorizer.fit_transform(texts)
