import requests


def test_numerology_flow(auth_context, base_url):
    token = auth_context["token"]
    dob = "1990-01-12"

    res = requests.post(
        f"{base_url}/api/numerology",
        json={"dob": dob},
        headers={"Authorization": f"Bearer {token}"},
        timeout=15,
    )
    assert res.status_code == 200, f"Numerology failed: {res.status_code} {res.text}"

    data = res.json()
    assert data.get("success") is True
    assert isinstance(data.get("moolank"), int)
    assert isinstance(data.get("bhagyank"), int)
    assert data.get("prediction"), "Prediction missing"

    debug_res = requests.get(
        f"{base_url}/_debug/numerology",
        params={"user_id": auth_context["user_id"], "dob": dob},
        timeout=15,
    )
    assert debug_res.status_code == 200, f"Debug numerology check failed: {debug_res.status_code} {debug_res.text}"
    assert debug_res.json().get("exists") is True
