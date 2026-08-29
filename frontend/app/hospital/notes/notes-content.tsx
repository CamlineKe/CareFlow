"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useCallback, useEffect, useRef, useState } from "react";
import type { FormEvent } from "react";

import { AppShell, BackToRolePicker } from "@/components/app-shell";
import {
  createBookingNote,
  listBookingNotes,
  type Note,
} from "@/lib/api/notes";
import { subscribeAuth } from "@/lib/auth";

const BODY_MAX_LENGTH = 10_000;
const TRANSCRIPT_MAX_LENGTH = 20_000;
const IMAGE_URL_MAX_LENGTH = 2_083;

function parseBookingId(value: string | null): number | null {
  if (!value || !/^[1-9]\d*$/.test(value)) {
    return null;
  }
  const bookingId = Number(value);
  return Number.isSafeInteger(bookingId) ? bookingId : null;
}

function getSafeHttpsUrl(value: string): string | null {
  try {
    const url = new URL(value);
    return url.protocol === "https:" ? url.href : null;
  } catch {
    return null;
  }
}

export function HospitalNotesContent() {
  const searchParams = useSearchParams();
  const bookingId = parseBookingId(searchParams.get("booking_id"));

  const [notes, setNotes] = useState<Note[]>([]);
  const [bodyText, setBodyText] = useState("");
  const [audioTranscript, setAudioTranscript] = useState("");
  const [imageUrl, setImageUrl] = useState("");
  const [status, setStatus] = useState<string | null>(null);
  const [isLoadingNotes, setIsLoadingNotes] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [authUid, setAuthUid] = useState<string | null | undefined>(undefined);
  const submissionInFlight = useRef(false);
  const loadRequestId = useRef(0);
  const activeBookingId = useRef<number | null>(bookingId);
  const activeAuthUid = useRef<string | null | undefined>(authUid);
  activeBookingId.current = bookingId;
  activeAuthUid.current = authUid;

  const loadNotes = useCallback(async (successMessage: string | null = null) => {
    const requestId = ++loadRequestId.current;
    setNotes([]);
    if (bookingId === null) {
      setIsLoadingNotes(false);
      return;
    }
    if (authUid === undefined) {
      setIsLoadingNotes(true);
      return;
    }
    if (authUid === null) {
      setIsLoadingNotes(false);
      setStatus("Sign in as hospital staff to view notes.");
      return;
    }

    setIsLoadingNotes(true);
    try {
      const data = await listBookingNotes(bookingId);
      if (
        requestId !== loadRequestId.current ||
        activeBookingId.current !== bookingId
      ) {
        return;
      }
      setNotes(data.notes);
      setStatus(successMessage);
    } catch (err: unknown) {
      if (
        requestId === loadRequestId.current &&
        activeBookingId.current === bookingId
      ) {
        setStatus(err instanceof Error ? err.message : "Could not load notes.");
      }
    } finally {
      if (
        requestId === loadRequestId.current &&
        activeBookingId.current === bookingId
      ) {
        setIsLoadingNotes(false);
      }
    }
  }, [authUid, bookingId]);

  useEffect(() => {
    return subscribeAuth(setAuthUid);
  }, []);

  useEffect(() => {
    void loadNotes();
  }, [loadNotes]);

  useEffect(() => {
    setBodyText("");
    setAudioTranscript("");
    setImageUrl("");
  }, [authUid, bookingId]);

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    if (submissionInFlight.current) return;
    if (bookingId === null) {
      setStatus("Open a valid booking from the hospital desk.");
      return;
    }
    if (!authUid) {
      setStatus("Sign in as hospital staff to add notes.");
      return;
    }
    const trimmedImageUrl = imageUrl.trim();
    if (trimmedImageUrl && !getSafeHttpsUrl(trimmedImageUrl)) {
      setStatus("Photo URL must be a valid HTTPS URL.");
      return;
    }

    submissionInFlight.current = true;
    setIsSubmitting(true);
    setStatus(null);
    const submittedBookingId = bookingId;
    const submittedAuthUid = authUid;
    try {
      await createBookingNote(submittedBookingId, {
        body_text: bodyText || null,
        audio_transcript: audioTranscript || null,
        images: trimmedImageUrl
          ? [{ image_url: trimmedImageUrl, sort_order: 0 }]
          : undefined,
      });
      if (
        activeBookingId.current !== submittedBookingId ||
        activeAuthUid.current !== submittedAuthUid
      ) {
        return;
      }
      setBodyText("");
      setAudioTranscript("");
      setImageUrl("");
      await loadNotes("Note saved.");
    } catch (err: unknown) {
      if (
        activeBookingId.current === submittedBookingId &&
        activeAuthUid.current === submittedAuthUid
      ) {
        setStatus(err instanceof Error ? err.message : "Could not save note.");
      }
    } finally {
      submissionInFlight.current = false;
      setIsSubmitting(false);
    }
  }

  return (
    <AppShell width="desk">
      <BackToRolePicker />

      <header>
        <h1 className="text-2xl font-semibold tracking-tight">
          Clinical notes
        </h1>
        <p className="mt-3 text-base text-cf-muted">
          Staff at this facility only. Patients cannot read these notes.
        </p>
        <p className="mt-2 text-sm">
          <Link href="/hospital" className="text-cf-teal underline-offset-4 hover:underline">
            Back to hospital desk
          </Link>
        </p>
      </header>

      {bookingId === null ? (
        <p className="mt-6 text-sm text-cf-muted" role="status">
          Open this page from a booking on the hospital desk. A positive integer{" "}
          <code>booking_id</code> is required.
        </p>
      ) : (
        <>
          <form className="mt-8 space-y-4" onSubmit={onSubmit}>
            <div>
              <label htmlFor="body-text" className="block text-sm font-medium">
                Text note
              </label>
              <textarea
                id="body-text"
                className="mt-1 w-full rounded-lg border border-cf-line bg-cf-card px-3 py-2 text-sm"
                rows={4}
                maxLength={BODY_MAX_LENGTH}
                disabled={isSubmitting}
                value={bodyText}
                onChange={(e) => setBodyText(e.target.value)}
              />
            </div>

            <div>
              <label htmlFor="audio-transcript" className="block text-sm font-medium">
                Transcript
              </label>
              <textarea
                id="audio-transcript"
                className="mt-1 w-full rounded-lg border border-cf-line bg-cf-card px-3 py-2 text-sm"
                rows={3}
                maxLength={TRANSCRIPT_MAX_LENGTH}
                aria-describedby="transcript-help"
                disabled={isSubmitting}
                value={audioTranscript}
                onChange={(e) => setAudioTranscript(e.target.value)}
                placeholder="Paste or type a transcript"
              />
              <p id="transcript-help" className="mt-1 text-xs text-cf-muted">
                Manual metadata entry only. Browser audio capture and transcription
                are not implemented.
              </p>
            </div>

            <div>
              <label htmlFor="image-url" className="block text-sm font-medium">
                Photo URL
              </label>
              <input
                id="image-url"
                type="url"
                inputMode="url"
                maxLength={IMAGE_URL_MAX_LENGTH}
                pattern="https://.*"
                aria-describedby="image-url-help"
                disabled={isSubmitting}
                className="mt-1 w-full rounded-lg border border-cf-line bg-cf-card px-3 py-2 text-sm"
                value={imageUrl}
                onChange={(e) => setImageUrl(e.target.value)}
                placeholder="https://…"
              />
              <p id="image-url-help" className="mt-1 text-xs text-cf-muted">
                Paste an existing HTTPS image URL. Browser photo capture, upload,
                and OCR are not implemented.
              </p>
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              className="rounded-lg bg-cf-teal px-4 py-2 text-sm font-semibold text-white disabled:opacity-60"
            >
              {isSubmitting ? "Saving…" : "Save note"}
            </button>
          </form>

          <section className="mt-10" aria-labelledby="notes-list-heading">
            <h2 id="notes-list-heading" className="text-base font-semibold">
              Notes for booking #{bookingId}
            </h2>
            {isLoadingNotes ? (
              <p className="mt-2 text-sm text-cf-muted" role="status">
                Loading notes…
              </p>
            ) : notes.length === 0 ? (
              <p className="mt-2 text-sm text-cf-muted">No notes yet.</p>
            ) : (
              <ul className="mt-4 space-y-4">
                {notes.map((note) => (
                  <li
                    key={note.id}
                    className="rounded-xl border border-cf-line bg-cf-card px-4 py-3 text-sm"
                  >
                    {note.body_text && <p>{note.body_text}</p>}
                    {note.audio_transcript && (
                      <p className="mt-2 text-cf-muted">
                        Voice: {note.audio_transcript}
                      </p>
                    )}
                    {note.images.length > 0 && (
                      <ul className="mt-2 list-disc pl-5">
                        {note.images.map((img) => (
                          <li key={img.id}>
                            {getSafeHttpsUrl(img.image_url) ? (
                              <a
                                href={getSafeHttpsUrl(img.image_url) ?? undefined}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-cf-teal underline"
                              >
                                Photo (opens in a new tab)
                              </a>
                            ) : (
                              <span className="text-cf-muted">
                                Photo URL unavailable
                              </span>
                            )}
                            {img.ocr_text ? `: ${img.ocr_text}` : null}
                          </li>
                        ))}
                      </ul>
                    )}
                  </li>
                ))}
              </ul>
            )}
          </section>
        </>
      )}

      {status && (
        <p className="mt-6 text-sm" role="status">
          {status}
        </p>
      )}
    </AppShell>
  );
}
