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
    # Use a short timeout to prevent hang on Vercel initialization
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
    try:
        # Check connection on startup
        client.admin.command('ping')
    except Exception as e:
        print(f"Warning: Could not connect to MongoDB. Using local fallback if possible. Error: {e}")
        # If real DB fails, fallback to mongomock for the serverless instance to at least start
        import mongomock
        client = mongomock.MongoClient()

db = client[MONGO_DB]

users_collection = db["users"]
numerology_collection = db["numerology_results"]
face_collection = db["face_results"]
