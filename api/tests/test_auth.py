import uuid

import requests


def test_signup_returns_token(base_url):
    email = f"auth_{uuid.uuid4().hex}@example.com"
    payload = {
        "full_name": "Auth Test",
        "email": email,
        "password": "AuthPass123!",
        "dob": "1991-02-03",
        "birth_place": "Auth City",
    }

    res = requests.post(f"{base_url}/auth/signup", json=payload, timeout=15)
    assert res.status_code == 200, f"Signup failed: {res.status_code} {res.text}"

    data = res.json()
    assert data.get("success") is True
    assert data.get("token"), "Token missing on signup"

    debug_res = requests.get(f"{base_url}/_debug/user", params={"email": email}, timeout=15)
    assert debug_res.status_code == 200, f"Debug user check failed: {debug_res.status_code} {debug_res.text}"
    assert debug_res.json().get("exists") is True


def test_login_returns_token(auth_context, base_url):
    res = requests.post(
        f"{base_url}/auth/login",
        json={"email": auth_context["email"], "password": auth_context["password"]},
        timeout=15,
    )
    assert res.status_code == 200, f"Login failed: {res.status_code} {res.text}"

    data = res.json()
    assert data.get("success") is True
    assert data.get("token"), "Token missing on login"


def test_protected_rejects_without_token(base_url):
    res = requests.post(f"{base_url}/api/numerology", json={"dob": "1990-01-12"}, timeout=15)
    assert res.status_code in (401, 403), f"Expected auth error, got {res.status_code}: {res.text}"
