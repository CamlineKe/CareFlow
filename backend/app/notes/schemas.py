"""Notes request/response models."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated

from pydantic import AnyUrl, BaseModel, ConfigDict, Field, UrlConstraints


HttpsUrl = Annotated[
    AnyUrl,
    UrlConstraints(
        max_length=2_083,
        allowed_schemes=["https"],
        host_required=True,
    ),
]


class NoteImageInput(BaseModel):
    image_url: HttpsUrl
    ocr_text: str | None = Field(default=None, max_length=20_000)
    sort_order: int = Field(default=0, ge=0, le=32_767)


class CreateNoteRequest(BaseModel):
    body_text: str | None = Field(default=None, max_length=10_000)
    audio_transcript: str | None = Field(default=None, max_length=20_000)
    ocr_text: str | None = Field(default=None, max_length=20_000)
    images: list[NoteImageInput] = Field(default_factory=list, max_length=10)


class NoteImageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    image_url: str
    ocr_text: str | None
    sort_order: int


class NoteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    booking_id: int
    author_user_id: int
    body_text: str | None
    audio_transcript: str | None
    ocr_text: str | None
    created_at: datetime
    images: list[NoteImageResponse]


class NoteListResponse(BaseModel):
    notes: list[NoteResponse]
