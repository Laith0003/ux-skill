export function Feed({ loadMore }: { loadMore: () => void }) {
  const observer = new IntersectionObserver(() => loadMore());
  return <ul ref={(el) => el && observer.observe(el)} />;
}
