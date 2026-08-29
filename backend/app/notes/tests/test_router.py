"""Notes routes: validation, role denial, and facility isolation."""

from __future__ import annotations

import pytest
from sqlalchemy import text

_AUTH = {"Authorization": "Bearer test-token"}
_IMAGE_URL_PREFIX = "https://example.com/"
_MAX_IMAGE_URL = _IMAGE_URL_PREFIX + "x" * (2_083 - len(_IMAGE_URL_PREFIX))
_OVERSIZED_IMAGE_URL = _MAX_IMAGE_URL + "x"


@pytest.mark.parametrize("method", ["post", "get"])
def test_patient_cannot_access_notes(
    method, notes_client, mock_firebase_uid, notes_test_data
):
    mock_firebase_uid(notes_test_data.patient_uid)
    request = getattr(notes_client, method)
    kwargs = {"json": {"body_text": "Should fail"}} if method == "post" else {}
    response = request(
        f"/hospital/bookings/{notes_test_data.same_facility_booking_id}/notes",
        headers=_AUTH,
        **kwargs,
    )

    assert response.status_code == 403
    assert response.json()["error"]["code"] == "forbidden"


def test_same_facility_staff_can_create_and_list_notes(
    notes_client, mock_firebase_uid, notes_test_data
):
    mock_firebase_uid(notes_test_data.same_facility_staff_uid)
    path = (
        f"/hospital/bookings/"
        f"{notes_test_data.same_facility_booking_id}/notes"
    )

    created = notes_client.post(
        path,
        headers=_AUTH,
        json={
            "body_text": "Patient stable.",
            "audio_transcript": "Stable vitals.",
            "images": [
                {
                    "image_url": "https://example.com/rx.jpg",
                    "ocr_text": "Paracetamol",
                    "sort_order": 1,
                }
            ],
        },
    )
    listed = notes_client.get(path, headers=_AUTH)

    assert created.status_code == 200
    assert created.json()["booking_id"] == notes_test_data.same_facility_booking_id
    assert created.json()["images"][0]["image_url"] == "https://example.com/rx.jpg"
    assert listed.status_code == 200
    assert [note["body_text"] for note in listed.json()["notes"]] == [
        "Patient stable."
    ]


@pytest.mark.parametrize("method", ["post", "get"])
def test_cross_facility_staff_receives_not_found(
    method, notes_client, mock_firebase_uid, notes_test_data
):
    mock_firebase_uid(notes_test_data.same_facility_staff_uid)
    request = getattr(notes_client, method)
    kwargs = {"json": {"body_text": "Must remain isolated"}} if method == "post" else {}
    response = request(
        f"/hospital/bookings/{notes_test_data.other_facility_booking_id}/notes",
        headers=_AUTH,
        **kwargs,
    )

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "booking_not_found"


@pytest.mark.parametrize(
    "image_url",
    [
        "http://example.com/rx.jpg",
        "javascript:alert(1)",
        "data:image/png;base64,AAAA",
        "ftp://example.com/rx.jpg",
        "/relative/rx.jpg",
        "https://",
    ],
)
def test_image_url_requires_valid_https(
    image_url, notes_client, mock_firebase_uid, notes_test_data
):
    mock_firebase_uid(notes_test_data.same_facility_staff_uid)
    response = notes_client.post(
        f"/hospital/bookings/{notes_test_data.same_facility_booking_id}/notes",
        headers=_AUTH,
        json={"images": [{"image_url": image_url}]},
    )

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"


def test_image_url_is_persisted_as_string(
    notes_client,
    mock_firebase_uid,
    notes_test_data,
    owner_session_factory,
):
    mock_firebase_uid(notes_test_data.same_facility_staff_uid)
    image_url = "https://example.com/evidence/rx.jpg"
    response = notes_client.post(
        f"/hospital/bookings/{notes_test_data.same_facility_booking_id}/notes",
        headers=_AUTH,
        json={"images": [{"image_url": image_url}]},
    )

    assert response.status_code == 200
    with owner_session_factory() as session:
        stored_url = session.execute(
            text(
                """
                SELECT ni.image_url
                FROM note_images ni
                JOIN notes n ON n.id = ni.note_id
                WHERE n.booking_id = :booking_id
                """
            ),
            {"booking_id": notes_test_data.same_facility_booking_id},
        ).scalar_one()
    assert isinstance(stored_url, str)
    assert stored_url == image_url


@pytest.mark.parametrize(
    "payload",
    [
        {"body_text": "x" * 10_001},
        {"audio_transcript": "x" * 20_001},
        {"ocr_text": "x" * 20_001},
        {
            "images": [
                {
                    "image_url": "https://example.com/rx.jpg",
                    "ocr_text": "x" * 20_001,
                }
            ]
        },
        {
            "images": [
                {
                    "image_url": _OVERSIZED_IMAGE_URL,
                }
            ]
        },
        {
            "images": [
                {"image_url": f"https://example.com/{index}.jpg"}
                for index in range(11)
            ]
        },
        {
            "images": [
                {
                    "image_url": "https://example.com/rx.jpg",
                    "sort_order": -1,
                }
            ]
        },
        {
            "images": [
                {
                    "image_url": "https://example.com/rx.jpg",
                    "sort_order": 32_768,
                }
            ]
        },
    ],
)
def test_note_and_image_bounds_reject_values_over_limits(
    payload, notes_client, mock_firebase_uid, notes_test_data
):
    mock_firebase_uid(notes_test_data.same_facility_staff_uid)
    response = notes_client.post(
        f"/hospital/bookings/{notes_test_data.same_facility_booking_id}/notes",
        headers=_AUTH,
        json=payload,
    )

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"


def test_note_and_image_bounds_accept_exact_limits(
    notes_client, mock_firebase_uid, notes_test_data
):
    mock_firebase_uid(notes_test_data.same_facility_staff_uid)
    response = notes_client.post(
        f"/hospital/bookings/{notes_test_data.same_facility_booking_id}/notes",
        headers=_AUTH,
        json={
            "body_text": "b" * 10_000,
            "audio_transcript": "a" * 20_000,
            "ocr_text": "o" * 20_000,
            "images": [
                {
                    "image_url": f"https://example.com/{index}.jpg",
                    "ocr_text": "i" * 20_000,
                    "sort_order": 32_767,
                }
                for index in range(10)
            ],
        },
    )

    assert response.status_code == 200
    assert len(response.json()["images"]) == 10


def test_image_url_accepts_exact_maximum_length(
    notes_client, mock_firebase_uid, notes_test_data
):
    mock_firebase_uid(notes_test_data.same_facility_staff_uid)
    response = notes_client.post(
        f"/hospital/bookings/{notes_test_data.same_facility_booking_id}/notes",
        headers=_AUTH,
        json={"images": [{"image_url": _MAX_IMAGE_URL}]},
    )

    assert len(_MAX_IMAGE_URL) == 2_083
    assert response.status_code == 200


@pytest.mark.parametrize("booking_id", [0, -1])
def test_booking_id_must_be_positive(
    booking_id, notes_client, mock_firebase_uid, notes_test_data
):
    mock_firebase_uid(notes_test_data.same_facility_staff_uid)
    response = notes_client.get(
        f"/hospital/bookings/{booking_id}/notes",
        headers=_AUTH,
    )

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"


@pytest.mark.parametrize(
    "payload",
    [{}, {"body_text": "   ", "audio_transcript": "\n"}],
)
def test_empty_note_returns_validation_error(
    payload, notes_client, mock_firebase_uid, notes_test_data
):
    mock_firebase_uid(notes_test_data.same_facility_staff_uid)
    response = notes_client.post(
        f"/hospital/bookings/{notes_test_data.same_facility_booking_id}/notes",
        headers=_AUTH,
        json=payload,
    )

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"
