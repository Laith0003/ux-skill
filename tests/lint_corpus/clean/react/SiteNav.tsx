import { useState } from "react";

const links = [
  { href: "/pricing", label: "Pricing" },
  { href: "/customers", label: "Customers" },
  { href: "/changelog", label: "Changelog" },
];

export function SiteNav() {
  const [open, setOpen] = useState(false);

  return (
    <header className="site-header border-b border-line">
      <nav aria-label="Primary" className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <a href="/" className="font-display text-lg">
          Freightline
        </a>
        <ul className="hidden gap-6 md:flex">
          {links.map((link) => (
            <li key={link.href}>
              <a className="nav-link" href={link.href}>
                {link.label}
              </a>
            </li>
          ))}
          <li>
            <a
              className="nav-link"
              href="https://status.freightline.example"
              target="_blank"
              rel="noopener noreferrer"
            >
              System status
            </a>
          </li>
        </ul>
        <button
          type="button"
          className="menu-toggle md:hidden"
          aria-expanded={open}
          aria-controls="mobile-menu"
          onClick={() => setOpen((v) => !v)}
        >
          <span className="sr-only">Open menu</span>
          <svg aria-hidden="true" viewBox="0 0 24 24" width="24" height="24">
            <path d="M4 7h16M4 12h16M4 17h16" stroke="currentColor" strokeWidth="1.5" />
          </svg>
        </button>
      </nav>
      {open ? (
        <ul id="mobile-menu" className="flex flex-col gap-2 px-6 pb-4 md:hidden">
          {links.map((link) => (
            <li key={link.href}>
              <a className="block py-2" href={link.href}>
                {link.label}
              </a>
            </li>
          ))}
        </ul>
      ) : null}
    </header>
  );
}
