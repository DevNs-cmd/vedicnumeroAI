from pathlib import Path

import requests


BASE_DIR = Path(__file__).resolve().parents[2]
IMAGE_PATH = BASE_DIR / ".vscode" / "developer img-1.jpeg"


def test_face_read_flow(auth_context, base_url):
    assert IMAGE_PATH.exists(), f"Sample face image not found at {IMAGE_PATH}"

    with IMAGE_PATH.open("rb") as image_file:
        res = requests.post(
            f"{base_url}/api/face-read",
            files={"file": image_file},
            headers={"Authorization": f"Bearer {auth_context['token']}"},
            timeout=30,
        )

    assert res.status_code == 200, f"Face read failed: {res.status_code} {res.text}"

    data = res.json()
    assert data.get("success") is True
    assert data.get("face_shape"), "Face shape missing"
    assert data.get("numerology_prediction"), "Prediction missing"

    debug_res = requests.get(
        f"{base_url}/_debug/face",
        params={"user_id": auth_context["user_id"], "filename": "developer img-1.jpeg"},
        timeout=15,
    )
    assert debug_res.status_code == 200, f"Debug face check failed: {debug_res.status_code} {debug_res.text}"
    assert debug_res.json().get("exists") is True
