import type { Metadata, Viewport } from "next";
import { RegisterServiceWorker } from "@/components/register-service-worker";
import "./globals.css";

export const metadata: Metadata = {
  title: {
    default: "CareFlow",
    template: "%s · CareFlow",
  },
  description:
    "Kenya pretriage routing to a suitable facility. This is not a diagnosis.",
  applicationName: "CareFlow",
  appleWebApp: {
    capable: true,
    title: "CareFlow",
    statusBarStyle: "default",
  },
};

export const viewport: Viewport = {
  themeColor: "#0f5c4c",
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <RegisterServiceWorker />
        {children}
      </body>
    </html>
  );
}
