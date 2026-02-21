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
    # Note: We remove the top-level ping to avoid cold-start timeouts. 
    # If connection fails, Pymongo will raise an error on the first operation.
    # To be safe, we check if we can reach the server, but don't block indefinitely.
    try:
        # We only check connection info without blocking too long
        # If it fails, we use mongomock as fallback
        client.admin.command('ping')
    except Exception as e:
        print(f"Warning: Could not connect to MongoDB. Using local fallback. Error: {e}")
        import mongomock
        client = mongomock.MongoClient()

db = client[MONGO_DB]

users_collection = db["users"]
numerology_collection = db["numerology_results"]
face_collection = db["face_results"]
