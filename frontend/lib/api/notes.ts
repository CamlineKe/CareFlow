/** Notes API client (P5). Authentication is handled by the shared client. */
import { apiFetch } from "./client";

export type NoteImageInput = {
  image_url: string;
  ocr_text?: string | null;
  sort_order?: number;
};

export type CreateNotePayload = {
  body_text?: string | null;
  audio_transcript?: string | null;
  ocr_text?: string | null;
  images?: NoteImageInput[];
};

export type NoteImage = {
  id: number;
  image_url: string;
  ocr_text: string | null;
  sort_order: number;
};

export type Note = {
  id: number;
  booking_id: number;
  author_user_id: number;
  body_text: string | null;
  audio_transcript: string | null;
  ocr_text: string | null;
  created_at: string;
  images: NoteImage[];
};

export async function createBookingNote(
  bookingId: number,
  payload: CreateNotePayload,
): Promise<Note> {
  return apiFetch<Note>(`/hospital/bookings/${bookingId}/notes`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function listBookingNotes(
  bookingId: number,
): Promise<{ notes: Note[] }> {
  return apiFetch<{ notes: Note[] }>(
    `/hospital/bookings/${bookingId}/notes`,
  );
}
