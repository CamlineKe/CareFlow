import type { Metadata } from "next";
import Link from "next/link";
import { AppShell } from "@/components/app-shell";

export const metadata: Metadata = {
  title: "CareFlow",
  description:
    "Kenya pretriage routing to a suitable facility. This is not a diagnosis.",
};

export default function RolePickerPage() {
  return (
    <AppShell width="phone">
      <header className="pt-4">
        <p className="text-sm font-medium tracking-wide text-cf-teal">Kenya</p>
        <h1 className="mt-1 text-3xl font-semibold tracking-tight">CareFlow</h1>
        <p id="pretriage-disclaimer" className="mt-3 text-base text-cf-muted">
          Kenya pretriage routing to a suitable facility. This is{" "}
          <strong className="font-semibold text-cf-ink">not a diagnosis</strong>.
        </p>
      </header>

      <nav
        className="mt-8 flex flex-col gap-3"
        aria-labelledby="role-picker-heading"
      >
        <h2
          id="role-picker-heading"
          className="text-sm font-medium text-cf-muted"
        >
          Who is using CareFlow?
        </h2>

        <Link
          href="/patient"
          aria-describedby="pretriage-disclaimer"
          className="block min-h-16 rounded-xl border border-cf-line bg-cf-card px-4 py-4 text-cf-ink shadow-sm hover:border-cf-teal"
        >
          <span className="block text-lg font-semibold">Care-seeker</span>
          <span className="mt-1 block text-sm text-cf-muted">
            I need care — find a facility and book
          </span>
        </Link>

        <Link
          href="/hospital"
          className="block min-h-16 rounded-xl border border-cf-line bg-cf-card px-4 py-4 text-cf-ink shadow-sm hover:border-cf-teal"
        >
          <span className="block text-lg font-semibold">Hospital staff</span>
          <span className="mt-1 block text-sm text-cf-muted">
            Hospital desk — this facility only
          </span>
        </Link>
      </nav>
    </AppShell>
  );
}
