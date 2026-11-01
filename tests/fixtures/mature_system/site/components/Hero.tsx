export function Hero() {
  return (
    <section className="relative bg-navy-deep">
      <img src="/hero.jpg" alt="" className="absolute inset-0" />
      <div className="-z-10 absolute inset-0 bg-white/80"></div>
      <h1 className="relative z-10 text-white font-display">Harbor light</h1>
    </section>
  );
}
