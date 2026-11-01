// Theme object consumed by the sx prop. Numbers under `space` are pixels;
// numbers passed to spacing keys in sx are multipliers of `space[1]`.
export const theme = {
  space: [0, 4, 8, 12, 16, 24, 32, 48],
  radii: { sm: 4, md: 8, lg: 12 },
  fontSizes: { sm: 14, md: 16, lg: 18, xl: 22, display: 56 },
  fonts: {
    display: '"Fraunces", Georgia, serif',
    body: '"Public Sans", system-ui, sans-serif',
  },
  zIndices: { sticky: 20, popover: 40, modal: 60, toast: 80 },
  shadows: {
    raised: "0 4px 12px rgb(28 25 23 / 0.08)",
    focus: "0 0 0 3px rgb(180 83 9 / 0.45)",
  },
  transitions: {
    fast: "120ms cubic-bezier(0.2, 0.8, 0.2, 1)",
  },
} as const;

export type Theme = typeof theme;
