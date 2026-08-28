import type { Metadata } from "next";
import { AppShell, BackToRolePicker } from "@/components/app-shell";

export const metadata: Metadata = {
  title: "Care-seeker",
  description:
    "Care-seeker pretriage shell. This is not a diagnosis. If this is an emergency, call 999 or go now.",
};

export default function CareSeekerPage() {
  return (
    <AppShell width="phone">
      <BackToRolePicker />

      <header>
        <h1 className="text-2xl font-semibold tracking-tight">Care-seeker</h1>
        <p className="mt-2 text-base font-semibold text-cf-ink">
          This is not a diagnosis.
        </p>
        <p className="mt-2 text-sm text-cf-muted">
          CareFlow is Kenya pretriage routing to a suitable facility — not in-hospital
          triage.
        </p>
      </header>

      <section
        className="mt-6 rounded-xl border border-cf-emergency bg-cf-emergency-bg px-4 py-4"
        aria-labelledby="emergency-heading"
      >
        <h2 id="emergency-heading" className="text-base font-semibold text-cf-emergency">
          Emergency
        </h2>
        <p className="mt-2 text-sm text-cf-ink">
          If this is an emergency, call 999 or go now to the nearest emergency
          facility.
        </p>
        <p className="mt-3">
          <a
            href="tel:999"
            className="inline-flex min-h-12 min-w-32 items-center justify-center rounded-lg bg-cf-emergency px-4 text-base font-semibold text-white hover:brightness-110"
          >
            Call 999
          </a>
        </p>
        <p className="mt-3 text-sm font-medium text-cf-ink">Go now</p>
      </section>

      <p className="mt-8 text-sm text-cf-muted">
        Pretriage questions and booking will appear here. There is no symptom form
        in this shell.
      </p>
    </AppShell>
  );
}
