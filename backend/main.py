import os
import sys
from pathlib import Path

# Add the current directory to sys.path to ensure modules can be found
# regardless of where the script is executed from (e.g., Vercel)
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.append(str(current_dir))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import users_collection
from routes.auth import router as auth_router
from routes.numerology import router as numerology_router
from routes.face import router as face_router
from routes.chat import router as chat_router

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
