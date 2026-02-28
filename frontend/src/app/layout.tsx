import type { Metadata } from "next";
import { Inter, Noto_Sans_KR } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
const notoSansKR = Noto_Sans_KR({
  subsets: ["latin"],
  weight: ["400", "500", "700"],
  variable: "--font-noto-kr",
});

export const metadata: Metadata = {
  title: "Soju Wars: 100-Year Brand Evolution",
  description:
    "Timeline-based visualization of Korean soju brand wars + influencer evolution (1924-2026)",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ko">
      <body className={`${inter.variable} ${notoSansKR.variable}`}>{children}</body>
    </html>
  );
}
