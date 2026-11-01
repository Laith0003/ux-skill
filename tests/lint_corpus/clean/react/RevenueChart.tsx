type Point = { month: string; value: number };

const WIDTH = 640;
const HEIGHT = 240;

export function RevenueChart({ points, currency }: { points: Point[]; currency: string }) {
  const max = Math.max(...points.map((p) => p.value));
  const step = WIDTH / Math.max(points.length - 1, 1);
  const path = points
    .map((p, i) => `${i === 0 ? "M" : "L"}${i * step},${HEIGHT - (p.value / max) * HEIGHT}`)
    .join(" ");

  return (
    <figure className="chart">
      <svg
        role="img"
        aria-labelledby="revenue-title revenue-desc"
        viewBox={`0 0 ${WIDTH} ${HEIGHT}`}
        width="100%"
        height={HEIGHT}
      >
        <title id="revenue-title">Monthly recurring revenue</title>
        <desc id="revenue-desc">Revenue in {currency} for the last twelve months.</desc>
        <defs>
          <linearGradient id="area-fill" x1="0" x2="0" y1="0" y2="1">
            <stop offset="0%" stopColor="var(--chart-series-1)" stopOpacity="0.24" />
            <stop offset="100%" stopColor="var(--chart-series-1)" stopOpacity="0" />
          </linearGradient>
        </defs>
        <path d={`${path} L${WIDTH},${HEIGHT} L0,${HEIGHT} Z`} fill="url(#area-fill)" />
        <path d={path} fill="none" stroke="var(--chart-series-1)" strokeWidth={2} />
      </svg>
      <figcaption className="chart-caption">
        Source: billing ledger, closed months only.
      </figcaption>
    </figure>
  );
}
