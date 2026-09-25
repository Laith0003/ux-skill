type Quote = {
  body: string;
  name: string;
  role: string;
  company: string;
  portrait: { src: string; width: number; height: number };
  rating?: number;
};

// Ratings come from the review export; we print the number, never a row of
// star glyphs, and never "5/5" when the source says 4.6.
export function Testimonial({ quote }: { quote: Quote }) {
  return (
    <figure className="testimonial grid gap-4 border-s-2 border-line ps-5">
      <blockquote className="text-lg leading-relaxed">
        <p>{quote.body}</p>
      </blockquote>
      <figcaption className="flex items-center gap-3">
        <img
          src={quote.portrait.src}
          alt=""
          width={quote.portrait.width}
          height={quote.portrait.height}
          className="size-10 rounded-full object-cover"
        />
        <span>
          <span className="block font-medium">{quote.name}</span>
          <span className="block text-sm text-ink-muted">
            {quote.role}, {quote.company}
          </span>
        </span>
        {quote.rating ? (
          <span className="ms-auto text-sm tabular-nums">Rated {quote.rating.toFixed(1)} of 5</span>
        ) : null}
      </figcaption>
    </figure>
  );
}
