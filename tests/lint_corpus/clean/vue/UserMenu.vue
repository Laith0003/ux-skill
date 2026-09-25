<script setup lang="ts">
import { computed, ref } from "vue";

const props = defineProps<{ user: { name: string; email: string; avatarUrl: string } }>();
const open = ref(false);
const initials = computed(() =>
  props.user.name
    .split(" ")
    .map((part) => part[0])
    .join("")
    .slice(0, 2),
);
</script>

<template>
  <div class="user-menu" :class="{ 'is-open': open }">
    <button
      type="button"
      class="user-menu__trigger"
      :aria-expanded="open"
      aria-controls="user-menu-list"
      @click="open = !open"
    >
      <img
        v-if="user.avatarUrl"
        :src="user.avatarUrl"
        :alt="`${user.name}, account menu`"
        width="32"
        height="32"
        class="user-menu__avatar"
      />
      <span v-else class="user-menu__initials" aria-hidden="true">{{ initials }}</span>
      <span class="sr-only">Account menu for {{ user.name }}</span>
    </button>
    <ul v-show="open" id="user-menu-list" class="user-menu__list">
      <li><a href="/account">Account settings</a></li>
      <li><a href="/billing">Billing and invoices</a></li>
      <li>
        <form method="post" action="/logout">
          <button type="submit" class="user-menu__signout">Sign out of {{ user.email }}</button>
        </form>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.user-menu {
  position: relative;
}

.user-menu__trigger {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding-block: var(--space-1);
  padding-inline: var(--space-2);
  border-radius: var(--radius-sm);
}

.user-menu__trigger:focus-visible {
  outline: 2px solid var(--focus);
  outline-offset: 2px;
}

.user-menu__list {
  position: absolute;
  inset-block-start: calc(100% + var(--space-1));
  inset-inline-end: 0;
  min-inline-size: 14rem;
  padding: var(--space-2);
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  background: var(--surface);
  box-shadow: 0 4px 12px rgb(15 23 42 / 0.08);
  z-index: var(--z-popover);
}
</style>
