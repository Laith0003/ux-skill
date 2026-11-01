<script setup lang="ts">
defineProps<{ steps: string[]; current: number }>();
</script>

<template>
  <nav aria-label="Checkout progress" class="stepper">
    <ol class="stepper__list">
      <li
        v-for="(step, index) in steps"
        :key="step"
        class="stepper__item"
        :class="{
          'stepper__item--done': index < current,
          'stepper__item--current': index === current,
        }"
        :aria-current="index === current ? 'step' : undefined"
      >
        <span class="stepper__index">{{ index + 1 }}</span>
        <span class="stepper__label">{{ step }}</span>
      </li>
    </ol>
  </nav>
</template>

<style scoped>
.stepper__list {
  display: flex;
  gap: var(--space-4);
  counter-reset: step;
  list-style: none;
  padding: 0;
}

.stepper__item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  color: var(--ink-muted);
}

.stepper__item--current {
  color: var(--ink);
  font-weight: 600;
}

.stepper__index {
  display: inline-grid;
  place-items: center;
  inline-size: 1.75rem;
  block-size: 1.75rem;
  border: 1px solid currentColor;
  border-radius: 50%;
  font-size: 0.8125rem;
}
</style>
