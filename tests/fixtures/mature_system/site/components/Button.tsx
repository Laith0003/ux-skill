export function Button({ children }) {
  return (
    <button className="bg-primary text-primary-foreground hover:bg-primary/90 focus:ring-2 md:px-6 px-6 rounded-card duration-fast">
      {children}
    </button>
  );
}
