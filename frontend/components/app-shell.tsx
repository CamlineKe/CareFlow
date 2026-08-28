import Link from "next/link";

type AppShellProps = {
  children: React.ReactNode;
  /** Care-seeker is phone-width; hospital desk may be slightly wider. */
  width?: "phone" | "desk";
};

export function AppShell({ children, width = "phone" }: AppShellProps) {
  const maxWidth = width === "desk" ? "max-w-xl" : "max-w-md";

  return (
    <div className={`mx-auto min-h-dvh w-full ${maxWidth} px-4 py-6 sm:px-5`}>
      {children}
    </div>
  );
}

export function BackToRolePicker() {
  return (
    <p className="mb-6">
      <Link
        href="/"
        className="inline-flex min-h-11 items-center text-sm font-medium text-cf-teal underline-offset-4 hover:underline"
      >
        Back to role picker
      </Link>
    </p>
  );
}
