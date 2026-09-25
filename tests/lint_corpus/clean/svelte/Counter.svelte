<script lang="ts">
  export let label: string;
  export let min = 0;
  export let max = 99;
  let value = min;

  // Clamp instead of disabling so keyboard users always hear the limit.
  function change(delta: number) {
    value = Math.min(max, Math.max(min, value + delta));
  }
</script>

<div class="counter" role="group" aria-label={label}>
  <button type="button" class="counter__step" aria-label="Decrease {label}" on:click={() => change(-1)}>
    <svg aria-hidden="true" viewBox="0 0 16 16" width="16" height="16"><path d="M3 8h10" stroke="currentColor" stroke-width="1.5" /></svg>
  </button>
  <output class="counter__value" aria-live="polite">{value}</output>
  <button type="button" class="counter__step" aria-label="Increase {label}" on:click={() => change(1)}>
    <svg aria-hidden="true" viewBox="0 0 16 16" width="16" height="16"><path d="M3 8h10M8 3v10" stroke="currentColor" stroke-width="1.5" /></svg>
  </button>
</div>

<style>
  .counter {
    display: inline-flex;
    align-items: center;
    border: 1px solid var(--line-strong);
    border-radius: var(--radius-sm);
  }

  .counter__step {
    display: grid;
    place-items: center;
    inline-size: 2.75rem;
    block-size: 2.75rem;
  }

  .counter__step:focus-visible {
    outline: 2px solid var(--focus);
    outline-offset: -2px;
  }

  .counter__value {
    min-inline-size: 3ch;
    text-align: center;
    font-variant-numeric: tabular-nums;
  }
</style>
