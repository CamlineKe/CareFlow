"""GET /me — 401 / 404 user_not_provisioned / 200 patient and staff."""

_AUTH = {"Authorization": "Bearer test-token"}


def test_me_missing_auth_returns_401(client):
    response = client.get("/me")
    assert response.status_code == 401
    error = response.json()["error"]
    assert error["code"] == "unauthorized"
    assert "message" in error


def test_me_garbage_token_returns_401(client):
    response = client.get("/me", headers=_AUTH)
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "unauthorized"


def test_me_unknown_uid_returns_404_not_provisioned(client, db_reset, mock_firebase_uid):
    mock_firebase_uid("not-a-provisioned-user")
    response = client.get("/me", headers=_AUTH)
    assert response.status_code == 404
    error = response.json()["error"]
    assert error["code"] == "user_not_provisioned"
    assert "message" in error


def test_me_patient_200(client, db_reset, mock_firebase_uid):
    mock_firebase_uid("demo-patient")
    response = client.get("/me", headers=_AUTH)
    assert response.status_code == 200
    body = response.json()
    assert body["firebase_uid"] == "demo-patient"
    assert body["role"] == "patient"
    assert body["facility_id"] is None
    assert body["locale"] == "en"
    assert body["phone_e164"] == "+254711111111"


def test_me_staff_200_with_facility_id(client, db_reset, mock_firebase_uid):
    mock_firebase_uid("demo-staff")
    response = client.get("/me", headers=_AUTH)
    assert response.status_code == 200
    body = response.json()
    assert body["firebase_uid"] == "demo-staff"
    assert body["role"] == "hospital_staff"
    assert isinstance(body["facility_id"], int)
    assert body["locale"] == "en"
    assert body["phone_e164"] == "+254722222222"

    ranked = client.get(
        "/facilities/recommend",
        params={"lat": -1.2925, "lng": 36.821},
    )
    assert ranked.status_code == 200
    knh = next(
        row
        for row in ranked.json()["facilities"]
        if row["kmhfr_code"] == "SEED-NBO-KNH"
    )
    assert body["facility_id"] == knh["id"]
