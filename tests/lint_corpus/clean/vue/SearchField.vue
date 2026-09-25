<script setup lang="ts">
import { ref, watch } from "vue";

const emit = defineEmits<{ (e: "search", query: string): void }>();
const query = ref("");
let timer: ReturnType<typeof setTimeout> | undefined;

watch(query, (value) => {
  clearTimeout(timer);
  timer = setTimeout(() => emit("search", value.trim()), 250);
});
</script>

<template>
  <div class="search-field" role="search">
    <label for="site-search" class="search-field__label">Search the help center</label>
    <div class="search-field__control">
      <svg aria-hidden="true" viewBox="0 0 20 20" width="18" height="18" class="search-field__icon">
        <circle cx="9" cy="9" r="6" fill="none" stroke="currentColor" stroke-width="1.5" />
        <path d="M13.5 13.5L17 17" stroke="currentColor" stroke-width="1.5" />
      </svg>
      <input
        id="site-search"
        v-model="query"
        type="search"
        placeholder="Try: change billing email"
        autocomplete="off"
      />
    </div>
  </div>
</template>

<style scoped>
.search-field__control {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding-inline: var(--space-3);
  border: 1px solid var(--line-strong);
  border-radius: var(--radius-sm);
  background: var(--surface);
}

.search-field__control:focus-within {
  outline: 2px solid var(--focus);
  outline-offset: 1px;
}

.search-field input {
  flex: 1;
  min-block-size: 2.75rem;
  border: 0;
  background: transparent;
}

/* The ring moves to the wrapper through :focus-within above. */
.search-field input:focus {
  outline: none;
}
</style>
