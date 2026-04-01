"""
database.py  —  Pure JSON File Storage (No MongoDB required)
=============================================================
All user accounts, numerology results, and face readings are stored
in a single JSON file:

  • Locally  → api/data/db.json  (relative to this file)
  • Vercel   → /tmp/vedicnumeroai_db.json  (writable in serverless)

The JSON file is created automatically on first use.
No external database service needed.
"""

import json
import os
import uuid
import threading
from datetime import datetime
from pathlib import Path

# ── Determine storage path ─────────────────────────────────────────────────────
# On Vercel /tmp is the only writable dir. Locally we use api/data/db.json
_IS_VERCEL = bool(os.getenv("VERCEL") or os.getenv("VERCEL_ENV"))

if _IS_VERCEL:
    _DB_PATH = Path("/tmp/vedicnumeroai_db.json")
else:
    _DATA_DIR = Path(__file__).parent / "data"
    _DATA_DIR.mkdir(exist_ok=True)
    _DB_PATH = _DATA_DIR / "db.json"

print(f"[DB] JSON storage path: {_DB_PATH}")

# ── Thread-safe lock ───────────────────────────────────────────────────────────
_lock = threading.Lock()


# ── Core read/write helpers ────────────────────────────────────────────────────
def _load() -> dict:
    """Load the entire database from disk."""
    if _DB_PATH.exists():
        try:
            return json.loads(_DB_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"users": [], "numerology_results": [], "face_results": []}


def _save(db: dict):
    """Atomically write the database back to disk."""
    _DB_PATH.write_text(
        json.dumps(db, default=str, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


# ── JSON Collection ────────────────────────────────────────────────────────────
class JsonCollection:
    """
    MongoDB-compatible collection interface backed by a JSON file.
    Supports: find_one, find, insert_one, update_one, delete_one
    """

    def __init__(self, name: str):
        self._name = name

    # ── Read ───────────────────────────────────────────────────────────────────
    def find_one(self, query: dict):
        with _lock:
            db = _load()
        for doc in db.get(self._name, []):
            if self._match(doc, query):
                return doc
        return None

    def find(self, query: dict = None):
        with _lock:
            db = _load()
        docs = db.get(self._name, [])
        if query:
            docs = [d for d in docs if self._match(d, query)]
        return list(docs)

    # ── Write ──────────────────────────────────────────────────────────────────
    def insert_one(self, document: dict):
        with _lock:
            db = _load()
            if "_id" not in document:
                document["_id"] = str(uuid.uuid4())
            # Store timestamps as ISO strings so JSON can serialise them
            for k, v in document.items():
                if isinstance(v, datetime):
                    document[k] = v.isoformat()
            db.setdefault(self._name, []).append(document)
            _save(db)

        class _Result:
            inserted_id = document["_id"]
        return _Result()

    def update_one(self, query: dict, update: dict, upsert: bool = False):
        with _lock:
            db = _load()
            col = db.setdefault(self._name, [])
            for doc in col:
                if self._match(doc, query):
                    if "$set" in update:
                        doc.update(update["$set"])
                    _save(db)
                    return
            if upsert:
                new_doc = {**query}
                if "$set" in update:
                    new_doc.update(update["$set"])
                if "_id" not in new_doc:
                    new_doc["_id"] = str(uuid.uuid4())
                col.append(new_doc)
                _save(db)

    def delete_one(self, query: dict):
        with _lock:
            db = _load()
            col = db.get(self._name, [])
            for i, doc in enumerate(col):
                if self._match(doc, query):
                    col.pop(i)
                    _save(db)
                    return

    # ── Helpers ────────────────────────────────────────────────────────────────
    @staticmethod
    def _match(doc: dict, query: dict) -> bool:
        for k, v in query.items():
            if doc.get(k) != v:
                return False
        return True


# ── Public collections (drop-in MongoDB replacements) ─────────────────────────
users_collection      = JsonCollection("users")
numerology_collection = JsonCollection("numerology_results")
face_collection       = JsonCollection("face_results")
