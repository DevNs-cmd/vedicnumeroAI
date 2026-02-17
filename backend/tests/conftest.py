import os
import sys
import time
import uuid
from pathlib import Path
import subprocess

import pytest
import requests
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[2]


def _load_env():
    env_path = BASE_DIR / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    storage_dir = BASE_DIR / "backend" / "tests" / "mongita_db"
    os.environ["MONGO_URI"] = f"mongita:///{storage_dir.as_posix()}"


@pytest.fixture(scope="session")
def base_url():
    _load_env()
    return os.getenv("BASE_URL", "http://127.0.0.1:8000")




@pytest.fixture(scope="session", autouse=True)
def ensure_server_running(base_url):
    health_url = f"{base_url}/health"
    try:
        res = requests.get(health_url, timeout=3)
        if res.status_code == 200:
            yield
            return
    except requests.RequestException:
        pass

    backend_dir = BASE_DIR / "backend"
    env = os.environ.copy()
    env.setdefault("PYTHONPATH", str(backend_dir))
    env["MONGO_URI"] = os.environ["MONGO_URI"]
    env["ENABLE_TEST_ROUTES"] = "1"

    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"],
        cwd=str(backend_dir),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    ready = False
    for _ in range(20):
        try:
            res = requests.get(health_url, timeout=3)
            if res.status_code == 200:
                ready = True
                break
        except requests.RequestException:
            pass
        time.sleep(0.5)

    if not ready:
        process.terminate()
        raise RuntimeError("Backend server did not start in time")

    try:
        yield
    finally:
        process.terminate()


def _signup_user(base_url: str, email: str, password: str):
    payload = {
        "full_name": "Test User",
        "email": email,
        "password": password,
        "dob": "1990-01-12",
        "birth_place": "Test City",
    }
    return requests.post(f"{base_url}/auth/signup", json=payload, timeout=15)


@pytest.fixture()
def auth_context(base_url):
    password = "TestPass123!"
    email = f"test_{uuid.uuid4().hex}@example.com"

    response = _signup_user(base_url, email, password)
    if response.status_code != 200:
        email = f"test_{uuid.uuid4().hex}@example.com"
        response = _signup_user(base_url, email, password)

    assert response.status_code == 200, f"Signup failed: {response.status_code} {response.text}"
    token = response.json().get("token")
    assert token, "Signup did not return token"

    debug_res = requests.get(f"{base_url}/_debug/user", params={"email": email}, timeout=15)
    assert debug_res.status_code == 200, f"Debug user check failed: {debug_res.status_code} {debug_res.text}"
    debug_data = debug_res.json()
    assert debug_data.get("exists") is True, "User not found in DB after signup"

    context = {
        "email": email,
        "password": password,
        "token": token,
        "user_id": debug_data.get("user_id"),
    }

    try:
        yield context
    finally:
        pass
