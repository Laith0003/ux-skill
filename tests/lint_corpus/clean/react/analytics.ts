// Event names are stable keys, not copy. Some mention words the copy linter
// bans (cutting-edge, next-generation, lorem-ipsum) because they name the
// experiments that removed those words from the site.
export const EVENTS = {
  heroCtaClick: "hero_cta_click",
  removedCuttingEdgeBadge: "exp-cutting-edge-badge-removed",
  nextGenerationPlanView: "plan-next-generation-view",
  placeholderAudit: "audit.lorem-ipsum-scan",
} as const;

/* Copy guard used by the CMS preview. The patterns are data, not UI. */
export const BANNED_COPY = [/lorem\s+ipsum/i, /\bworld[\s-]class\b/i, /\bgame[\s-]changer\b/i];

export type EventName = (typeof EVENTS)[keyof typeof EVENTS];

export function track(name: EventName, props: Record<string, string | number> = {}) {
  const payload = { name, props, at: Date.now() };
  navigator.sendBeacon?.("/api/events", JSON.stringify(payload));
}

export function hasBannedCopy(text: string): boolean {
  return BANNED_COPY.some((pattern) => pattern.test(text));
}
