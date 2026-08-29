/**
 * Tailwind class recipes for Wave 2 UI. Tokens live in globals.css @theme.
 * Do not invent radii or ad hoc hex. No bottom-tab or Health Score styles.
 */
export const card =
  "rounded-2xl border border-cf-line bg-cf-card p-5 shadow-md";

export const primaryBtn =
  "inline-flex w-full min-h-12 items-center justify-center rounded-xl bg-cf-teal px-4 text-base font-semibold text-white hover:bg-cf-teal-hover";

export const secondaryBtn =
  "inline-flex w-full min-h-12 items-center justify-center rounded-xl border border-cf-teal bg-transparent px-4 text-base font-semibold text-cf-teal hover:bg-cf-teal-wash";

export const emergencyBtn =
  "inline-flex w-full min-h-12 items-center justify-center rounded-xl bg-cf-emergency px-4 text-base font-semibold text-white hover:brightness-110";

export const disabledBtn =
  "inline-flex w-full min-h-12 cursor-not-allowed items-center justify-center rounded-xl border border-cf-disabled-bg bg-cf-disabled-bg px-4 text-base font-semibold text-cf-disabled-text";

/** Search-bar treatment: large radius, min-h-12, 3:1 border. */
export const input =
  "w-full min-h-12 rounded-xl border border-cf-line-strong bg-cf-card px-4 text-base text-cf-ink placeholder:text-cf-placeholder";

export const textarea =
  "w-full min-h-32 rounded-xl border border-cf-line-strong bg-cf-card px-4 py-3 text-base text-cf-ink placeholder:text-cf-placeholder";

export const pageTitle = "text-2xl font-semibold tracking-tight text-cf-ink";

export const subtitle = "text-base text-cf-muted";

export const emergencyCard =
  "rounded-2xl border border-cf-emergency bg-cf-emergency-bg p-4 shadow-md";

export const textLink =
  "inline-flex min-h-11 items-center text-sm font-medium text-cf-teal underline-offset-4 hover:underline";

export const localeTrack = "inline-flex shrink-0 rounded-xl bg-cf-teal-wash p-1";

export const localeOptionOn =
  "inline-flex min-h-11 items-center justify-center rounded-lg bg-cf-teal px-3 text-sm font-semibold text-white";

export const localeOptionOff =
  "inline-flex min-h-11 items-center justify-center rounded-lg bg-transparent px-3 text-sm font-semibold text-cf-muted hover:text-cf-ink";

export const ui = {
  card,
  primaryBtn,
  secondaryBtn,
  emergencyBtn,
  disabledBtn,
  input,
  textarea,
  pageTitle,
  subtitle,
  emergencyCard,
  textLink,
  localeTrack,
  localeOptionOn,
  localeOptionOff,
} as const;
