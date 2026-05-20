import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Mic&Pose Evaluator",
  description: "Evaluador de conversaciones comerciales con IA",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  );
}
