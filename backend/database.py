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
elif not MONGO_URI or "localhost" in MONGO_URI:
    print("Warning: MONGO_URI not set or pointing to localhost. Using local fallback (mongomock).")
    try:
        import mongomock
        client = mongomock.MongoClient()
    except ImportError:
        print("Error: mongomock not installed.")
        client = None
else:
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
        client.admin.command('ping')
    except Exception as e:
        print(f"Warning: Could not connect to MongoDB. Error: {e}")
        try:
            import mongomock
            client = mongomock.MongoClient()
        except ImportError:
            client = None

db = client[MONGO_DB]

users_collection = db["users"]
numerology_collection = db["numerology_results"]
face_collection = db["face_results"]
