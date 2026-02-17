import os
from urllib.parse import urlparse

from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "vedicnumeroai")

parsed = urlparse(MONGO_URI)
if parsed.scheme == "mongomock":
    import mongomock

    client = mongomock.MongoClient()
elif parsed.scheme == "mongita":
    from mongita import MongitaClientDisk

    storage_path = (parsed.netloc + parsed.path).lstrip("/") or "."
    client = MongitaClientDisk(storage_path)
else:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

db = client[MONGO_DB]

users_collection = db["users"]
numerology_collection = db["numerology_results"]
face_collection = db["face_results"]
