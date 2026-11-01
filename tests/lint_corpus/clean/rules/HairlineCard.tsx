export function HairlineCard({ title, body }: { title: string; body: string }) {
  return (
    <div className="rounded-lg border border-stone-200 bg-white p-5 shadow-sm">
      <h3 className="font-semibold">{title}</h3>
      <p className="mt-1 text-sm text-stone-600">{body}</p>
      <div className="mt-4 rounded-md shadow-xl ring-0">
        <p className="p-3 text-sm">Floating preview with no border.</p>
      </div>
    </div>
  );
}
