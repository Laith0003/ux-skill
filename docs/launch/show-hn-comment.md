# Show HN — first comment to post as OP reply

> Post this as a reply to your own Show HN post within 60 seconds of submission. HN convention; signals you're engaged.

---

Builder here. I'm Laith, a solo founder shipping a MENA loyalty platform.
I kept hitting the same wall: I'd ask Claude Code to build a landing,
and what came back was clean, but it had the same fingerprints every time.

Three months later I have 30 of those fingerprints catalogued as deterministic
lint rules, 37 motion principles from Sonner/Vaul's author, 72 brand DESIGN.md
specs (Apple, Stripe, Linear, Figma, Tesla), and a discovery protocol that asks
10 questions before producing anything.

Some of what gets caught:

  - Inter as the brand display face
  - Purple-to-blue gradients on white
  - Three equal cards in a row
  - "John Doe" / "Acme" / 99.99% in placeholders
  - Centered hero over a dark image
  - h-screen on mobile (use min-h-[100dvh])
  - Decorative animation with no meaning
  - Marketing filler verbs (Elevate / Seamless / Unleash)

There's a /ux-lint command that runs the regex pass with zero LLM, exits
non-zero on Critical/High, wires into CI. There's /ux-design that produces
a full landing in the named brand's design language. There's /ux-audit that
walks 6 lenses (Norman, Krug, Laws of UX, WCAG, microcopy, error recovery).

Install:

    /plugin marketplace add https://github.com/Laith0003/ux-skill.git
    /plugin install ux@ux-skill

Open to critique. Especially interested in fingerprints I missed.

Repo: https://github.com/Laith0003/ux-skill
