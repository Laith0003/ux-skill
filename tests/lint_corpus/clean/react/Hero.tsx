import type { CSSProperties } from "react";
import { cn } from "../lib/cn";

type HeroProps = {
  eyebrow: string;
  title: string;
  lede: string;
  accent: string;
  compact?: boolean;
};

// The hero sets its accent through a custom property so the stylesheet owns
// every declaration. Do not hardcode purple-to-blue gradients here; the
// accent comes from the tenant theme.
export function Hero({ eyebrow, title, lede, accent, compact = false }: HeroProps) {
  const themed = { "--hero-accent": accent } as CSSProperties;

  return (
    <section
      aria-labelledby="hero-title"
      className={cn(
        "relative isolate grid gap-10 px-6 pb-16 pt-24 md:grid-cols-[7fr_5fr] md:px-12",
        compact && "pt-12",
      )}
      style={themed}
    >
      <div className="flex flex-col gap-5">
        <p className="text-sm font-medium text-[color:var(--hero-accent)]">{eyebrow}</p>
        <h1 id="hero-title" className="max-w-[18ch] text-balance font-display text-5xl leading-[1.05]">
          {title}
        </h1>
        <p className="max-w-prose text-lg text-ink-muted">{lede}</p>
        <div className="flex flex-wrap items-center gap-3">
          <a className="btn btn-primary" href="/signup?plan=team">
            Start a team trial
          </a>
          <a className="btn btn-quiet" href="/tour">
            Take the product tour
          </a>
        </div>
      </div>
      <figure className="relative overflow-hidden rounded-lg border border-line">
        <img
          src="/media/hero-dispatch-board.avif"
          alt="Dispatch board showing six open routes sorted by arrival time"
          width={1280}
          height={960}
          loading="eager"
          fetchPriority="high"
          className="h-full w-full object-cover"
        />
        <figcaption className="sr-only">Live dispatch board</figcaption>
      </figure>
    </section>
  );
}
