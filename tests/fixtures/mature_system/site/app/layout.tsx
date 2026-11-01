import './globals.css';

export default function RootLayout({ children }) {
  return (
    <html lang="ar" dir="rtl">
      <body className="bg-canvas text-ink">{children}</body>
    </html>
  );
}
