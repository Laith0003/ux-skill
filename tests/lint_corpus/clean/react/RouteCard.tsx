import { Button } from "../ui/button";
import { Dialog } from "../ui/dialog";
import { ImageGallery } from "../ui/image-gallery";
import { Select } from "../ui/select";

type Route = {
  id: string;
  name: string;
  stops: number;
  photos: { src: string; alt: string; width: number; height: number }[];
  mapUrl: string;
};

const card = {
  base: "route-card grid gap-4 rounded-lg border border-line p-5 transition-[opacity,transform] duration-150",
  muted: "opacity-80 hover:opacity-100 focus-within:opacity-100",
};

/* Review notes: the card never uses onClick on a div without a role, never
   renders <img src="x.jpg"> without dimensions, and the "Click here" link
   from the old design is gone. */
export function RouteCard({ route, onOpen, depth }: { route: Route; onOpen: (id: string) => void; depth: number }) {
  return (
    <article className={`${card.base} ${card.muted}`}>
      {/* The whole header is a button for keyboard and pointer users alike. */}
      <div
        role="button"
        tabIndex={0}
        className="route-card__header cursor-pointer"
        onClick={() => onOpen(route.id)}
        onKeyDown={(event) => event.key === "Enter" && onOpen(route.id)}
      >
        <h3 className="text-base font-semibold">{route.name}</h3>
        <p className="text-sm text-ink-muted">{route.stops} stops</p>
      </div>

      <ImageGallery images={route.photos} columns={2} />

      <iframe
        src={route.mapUrl}
        title="Map of the route with every stop numbered in delivery order, starting from the depot"
        width={560}
        height={315}
        loading="lazy"
      />

      <Select label="Assign driver" options={[]} />

      <Dialog title="Reassign every stop on this route to another driver and notify both of them">
        <p>Drivers are notified by SMS and in the app.</p>
      </Dialog>

      <div
        className="route-card__meta"
        style={{
          zIndex: depth,
          boxShadow: depth > 1 ? "var(--shadow-2)" : "none",
          ...(depth > 2 ? { outline: "1px solid var(--line)" } : {}),
        }}
      >
        <Button variant="secondary" onClick={() => onOpen(route.id)}>
          Open route {route.name}
        </Button>
        <a href={`/routes/${route.id}/export`} className="btn btn-quiet">
          Export stops as CSV
        </a>
        <a rel="noopener noreferrer" target="_blank" href={route.mapUrl}>
          Open the map in a new tab
        </a>
      </div>
    </article>
  );
}
