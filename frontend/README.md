# Frontend (`frontend/`)

Installable Next.js 15 PWA for CareFlow: role picker, care-seeker shell, and hospital desk shell. Talks to the FastAPI on port 8000 (`GET /health`, `/me`, `/facilities/recommend` — no `/v1` prefix).

## Key files

| File | Role |
|------|------|
| `app/page.tsx` | Role picker (`/`): care-seeker or hospital staff, no mic |
| `app/patient/page.tsx` | Care-seeker shell (`/patient`): pretriage disclaimer + 999 / go now |
| `app/hospital/page.tsx` | Hospital desk shell (`/hospital`): this facility only |
| `app/manifest.ts` | Web app manifest (`start_url` `/`, shortcuts `/patient` and `/hospital`) |
| `public/sw.js` | Online-only service worker (does not cache API / recommend) |
| `next.config.ts` | `output: 'standalone'` |

Dev: `cd frontend && npm install && npm run dev` (port 3000). Optional `NEXT_PUBLIC_API_URL` (default `http://localhost:8000`). Probe the API with `curl localhost:8000/health` → `{"status":"ok"}`. No vendor keys in the PWA. Full run order: [ONBOARDING.md](../ONBOARDING.md).

## Related

- [Repository root](../README.md)
- [ONBOARDING.md](../ONBOARDING.md)
- [docs/api/](../docs/api/) — HTTP chapters
