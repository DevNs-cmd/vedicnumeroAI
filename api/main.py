import os
import sys
from pathlib import Path

# Add the current directory and its parent to sys.path to ensure modules can be found
# regardless of where the script is executed from (e.g., Vercel)
current_file_path = Path(__file__).resolve()
current_dir = current_file_path.parent
root_dir = current_dir.parent

if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.database import users_collection
from api.routes.auth import router as auth_router
from api.routes.numerology import router as numerology_router
from api.routes.face import router as face_router
from api.routes.chat import router as chat_router


app = FastAPI()

cors_origins = os.getenv("CORS_ORIGINS", "*")
origins = [origin.strip() for origin in cors_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(numerology_router)
app.include_router(face_router)
app.include_router(chat_router)

if os.getenv("ENABLE_TEST_ROUTES") == "1":
    from routes.debug import router as debug_router

    app.include_router(debug_router)


@app.get("/health")
def health():
    return {"status": "ok"}
