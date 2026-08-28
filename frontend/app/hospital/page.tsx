import type { Metadata } from "next";
import { AppShell, BackToRolePicker } from "@/components/app-shell";

export const metadata: Metadata = {
  title: "Hospital desk",
  description: "Hospital desk for this facility only.",
};

export default function HospitalDeskPage() {
  return (
    <AppShell width="desk">
      <BackToRolePicker />

      <header>
        <h1 className="text-2xl font-semibold tracking-tight">
          Hospital desk — this facility only
        </h1>
        <p className="mt-3 text-base text-cf-muted">
          Hospital staff at one facility. Today’s CareFlow bookings and people
          waiting will appear here for this facility — not other facilities.
        </p>
      </header>

      <section
        className="mt-8 rounded-xl border border-dashed border-cf-line bg-cf-card px-4 py-6"
        aria-labelledby="desk-placeholder-heading"
      >
        <h2 id="desk-placeholder-heading" className="text-base font-semibold">
          Desk tools
        </h2>
        <p className="mt-2 text-sm text-cf-muted">
          No queue list yet. This placeholder does not show bookings or named
          people.
        </p>
      </section>
    </AppShell>
  );
}
