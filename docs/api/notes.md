# Notes

Clinical notes attached to hospital bookings (J6).

## Domain context

The notes API lets authenticated hospital staff create and list clinical notes
for bookings at their own facility. Patients cannot create or read notes. A
booking outside the staff member's facility is concealed as not found.

Paths have no `/v1` prefix. JSON keys and path parameters use `snake_case`.
There is no pagination in this phase, and response shapes must remain stable.
See [API conventions](conventions.md) for the shared Bearer authentication and
error envelope.

| Method | Path | Capability | OpenAPI tag |
|--------|------|------------|-------------|
| `POST` | `/hospital/bookings/{booking_id}/notes` | Hospital staff at the booking facility | `notes` |
| `GET` | `/hospital/bookings/{booking_id}/notes` | Hospital staff at the booking facility | `notes` |

**Authentication and authorisation**

- Send `Authorization: Bearer <Firebase ID token>`.
- `require_hospital_staff` requires `role = hospital_staff` and a
  `facility_id`.
- Request database sessions use the CareFlow app role. PostgreSQL RLS and the
  service's facility predicate both restrict bookings, notes, and images to
  the authenticated staff facility.
- A valid Firebase identity without a provisioned CareFlow user receives
  `404 user_not_provisioned`.
- A patient or staff user without a facility receives `403 forbidden`.
- A missing booking and a booking at another facility both receive the same
  `404 booking_not_found` response to avoid disclosing cross-facility data.

**Storage and side effects**

- `notes` stores text metadata; `note_images` stores HTTPS URL metadata and
  optional OCR text.
- Image bytes are not stored in PostgreSQL.
- Creating a note writes one note and zero to ten image metadata rows in the
  request transaction. No async jobs, webhooks, or notifications are started.
- Notes are listed oldest first by `created_at`, then `id`. Images are ordered
  by `sort_order`, then `id`.
- No update or delete route is exposed.

## Shared types

### `CreateNoteRequest`

| JSON key | Type | Required | Limits and behaviour |
|----------|------|----------|----------------------|
| `body_text` | string or null | No | Maximum 10,000 characters. Whitespace-only text does not make an otherwise empty note valid. |
| `audio_transcript` | string or null | No | Maximum 20,000 characters. Transcript input is metadata supplied by the client. |
| `ocr_text` | string or null | No | Maximum 20,000 characters. Note-level OCR metadata supplied by the client. |
| `images` | array of `NoteImageInput` | No | Defaults to `[]`; maximum 10 images. |

At least one non-whitespace text field or one image is required. An omitted
field and an explicit `null` have the same meaning.

### `NoteImageInput`

| JSON key | Type | Required | Limits and behaviour |
|----------|------|----------|----------------------|
| `image_url` | string URL | Yes | Maximum 2,083 characters. Must be a valid absolute HTTPS URL with a host. `http`, `javascript`, `data`, other schemes, and relative URLs are rejected. Stored as a string. |
| `ocr_text` | string or null | No | Maximum 20,000 characters. Image-level OCR metadata supplied by the client. |
| `sort_order` | integer | No | Defaults to `0`; inclusive range `0..32767`. |

The URL is metadata only. CareFlow does not fetch, validate the remote object,
or verify its content type in this phase.

### `NoteImageResponse`

| JSON key | Type | Notes |
|----------|------|-------|
| `id` | integer | Server-assigned image metadata ID. |
| `image_url` | string | Persisted HTTPS URL. |
| `ocr_text` | string or null | Client-supplied image OCR metadata. |
| `sort_order` | integer | Client value or server default `0`. |

### `NoteResponse`

| JSON key | Type | Notes |
|----------|------|-------|
| `id` | integer | Server-assigned note ID. |
| `booking_id` | integer | Parent booking ID. |
| `author_user_id` | integer | Authenticated staff user's CareFlow ID. |
| `body_text` | string or null | Note text. |
| `audio_transcript` | string or null | Client-supplied transcript metadata. |
| `ocr_text` | string or null | Client-supplied note-level OCR metadata. |
| `created_at` | RFC 3339 date-time string | Server creation time. |
| `images` | array of `NoteImageResponse` | Always present; ordered by `sort_order`, then `id`. |

### `NoteListResponse`

| JSON key | Type | Notes |
|----------|------|-------|
| `notes` | array of `NoteResponse` | Always present. This unpaginated envelope is unchanged in this phase. |

## `POST /hospital/bookings/{booking_id}/notes`

- **Purpose** — Add one clinical note and optional image metadata to a booking
  at the authenticated staff member's facility.
- **Path parameters** — `booking_id` is an integer greater than or equal to
  `1`.
- **Query parameters** — None. Unknown query keys are ignored by FastAPI.
- **Request body** — Required `application/json` body using
  `CreateNoteRequest`.
- **Success response** — `200` with `NoteResponse`.
- **Errors** — `401 unauthorized` for a missing or invalid Firebase token;
  `403 forbidden` for a non-staff user or staff user without a facility;
  `404 user_not_provisioned` for a valid but unknown Firebase identity;
  `404 booking_not_found` when the booking does not exist at the staff facility;
  `422 validation_error` for an invalid path parameter, empty note, non-HTTPS
  URL, or field/image limit violation.
- **Behaviour notes** — The authenticated staff user becomes
  `author_user_id`. URL and text metadata are persisted in the same
  transaction. This operation has no idempotency key, so retrying a successful
  request can create another note.

## `GET /hospital/bookings/{booking_id}/notes`

- **Purpose** — List clinical notes for one booking at the authenticated staff
  member's facility.
- **Path parameters** — `booking_id` is an integer greater than or equal to
  `1`.
- **Query parameters** — None. Unknown query keys are ignored by FastAPI.
- **Request body** — None.
- **Success response** — `200` with `NoteListResponse`, including
  `{ "notes": [] }` when the booking exists but has no notes.
- **Errors** — `401 unauthorized` for a missing or invalid Firebase token;
  `403 forbidden` for a non-staff user or staff user without a facility;
  `404 user_not_provisioned` for a valid but unknown Firebase identity;
  `404 booking_not_found` when the booking does not exist at the staff facility;
  `422 validation_error` for an invalid path parameter.
- **Behaviour notes** — The list is unpaginated. Notes are ordered by
  `created_at ASC, id ASC`; nested images by `sort_order ASC, id ASC`.

## Stable error codes and messages

All errors use `{ "error": { "code": "...", "message": "..." } }`.

| Code | HTTP | Stable message or source | When |
|------|------|--------------------------|------|
| `unauthorized` | 401 | Shared auth message | Bearer token is missing or invalid. |
| `user_not_provisioned` | 404 | `No CareFlow user is provisioned for this Firebase account.` | Token is valid but its UID is absent from `users`. |
| `forbidden` | 403 | `Hospital staff role required.` | Authenticated user is not hospital staff. |
| `forbidden` | 403 | `Staff user is not scoped to a facility.` | Staff user has no facility. |
| `booking_not_found` | 404 | `Booking not found for this facility.` | Booking is absent or belongs to another facility. |
| `validation_error` | 422 | First FastAPI/Pydantic validation message | Path, URL, text, image-count, OCR, or sort-order validation fails. |
| `validation_error` | 422 | `At least one of body_text, audio_transcript, ocr_text, or images is required.` | Payload has no image and no non-whitespace text. |

## Relationship to bookings

Notes are children of bookings. Facility ownership comes from the parent
booking, not from client-supplied note data. The notes package expects the P1
route hub to include its router; this chapter does not change booking routes
or router mounting.

## Suggested view → API mapping

| Hospital workflow | API call |
|-------------------|----------|
| Open a booking's notes panel | `GET /hospital/bookings/{booking_id}/notes` |
| Submit typed text or client-produced transcript/OCR metadata | `POST /hospital/bookings/{booking_id}/notes` |
| Refresh after a successful create | Reuse the returned note or call `GET` again |

Patients have no notes view or notes API call.

## Frontend notes

- Enforce the documented limits for immediate feedback, but treat backend
  validation as authoritative.
- Only send absolute HTTPS image URLs. Do not send blobs, data URLs, or local
  object URLs.
- Display `403` as role/access denial. Treat `404` uniformly and do not infer
  whether a booking exists at another facility.
- The backend accepts transcript and OCR text already produced by a client or
  another service. Browser capture, audio upload, image upload, transcription,
  and OCR execution are not implemented.
- Do not add pagination parameters or unwrap the `{ "notes": [...] }`
  response.

## Implementation status snapshot (backend)

| Area | Status |
|------|--------|
| Notes request validation and persistence | **Implemented** |
| Same-facility create/list authorisation | **Implemented** |
| Notes router inclusion in the main app | **Handshake P1** |
| Image or audio upload/storage pipeline | **Not implemented** |
| OCR or transcription execution | **Not implemented** |
| Browser media capture | **Not implemented** |
| Pagination | **Not implemented** |

## Reference files

- Router: `backend/app/notes/router.py`
- Schemas: `backend/app/notes/schemas.py`
- Service and SQL: `backend/app/notes/service.py`
- Staff guard: `backend/app/notes/deps.py`
- Package integration tests: `backend/app/notes/tests/`
- Route registration handshake: `backend/app/main.py` (P1-owned)
- Database schema and RLS: `backend/alembic/versions/0001_product_schema.sql`
- OpenAPI: `backend/openapi/openapi.yaml` after P1 mounts the router
