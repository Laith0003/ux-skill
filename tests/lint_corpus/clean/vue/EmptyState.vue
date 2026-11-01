<script setup lang="ts">
defineProps<{ title: string; body: string; actionLabel: string; actionHref: string }>();
</script>

<template>
  <section class="empty-state" aria-labelledby="empty-title">
    <svg class="empty-state__art" viewBox="0 0 240 160" width="240" height="160" aria-hidden="true">
      <rect x="20" y="30" width="200" height="110" rx="8" fill="var(--surface-sunken)" />
      <path d="M40 60h120M40 84h160M40 108h90" stroke="var(--line-strong)" stroke-width="6" stroke-linecap="round" />
    </svg>
    <h2 id="empty-title" class="empty-state__title">{{ title }}</h2>
    <p class="empty-state__body">{{ body }}</p>
    <a class="btn btn-primary" :href="actionHref">{{ actionLabel }}</a>
  </section>
</template>

<style scoped>
.empty-state {
  display: grid;
  justify-items: start;
  gap: var(--space-3);
  max-inline-size: 36rem;
  padding-block: var(--space-10);
}

.empty-state__title {
  font-size: var(--text-xl);
  text-wrap: balance;
}

.empty-state__body {
  color: var(--ink-muted);
}
</style>
