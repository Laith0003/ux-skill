<script setup lang="ts">
defineProps<{
  orders: Array<{ id: string; number: string; placedAt: string; total: string; status: string }>;
  locale: string;
}>();
</script>

<template>
  <table class="orders">
    <caption class="orders__caption">Orders placed in the last 30 days</caption>
    <thead>
      <tr>
        <th scope="col">Order</th>
        <th scope="col">Placed</th>
        <th scope="col" class="orders__num">Total</th>
        <th scope="col">Status</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="order in orders" :key="order.id">
        <th scope="row">
          <a :href="`/orders/${order.id}`">{{ order.number }}</a>
        </th>
        <td>
          <time :datetime="order.placedAt">{{ new Date(order.placedAt).toLocaleDateString(locale) }}</time>
        </td>
        <td class="orders__num">{{ order.total }}</td>
        <td>{{ order.status }}</td>
      </tr>
    </tbody>
  </table>
</template>

<style scoped>
.orders {
  inline-size: 100%;
  border-collapse: collapse;
  font-variant-numeric: tabular-nums;
}

.orders th,
.orders td {
  padding-block: var(--space-2);
  padding-inline: var(--space-3);
  border-block-end: 1px solid var(--line);
  text-align: start;
}

.orders__num {
  text-align: end;
}

.orders__caption {
  caption-side: top;
  padding-block-end: var(--space-2);
  color: var(--ink-muted);
  text-align: start;
}
</style>
