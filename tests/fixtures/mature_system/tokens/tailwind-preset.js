/** Maps utility names to the system's custom properties. */
module.exports = {
  theme: {
    extend: {
      colors: {
        canvas: 'var(--brand-canvas)',
        surface: 'var(--brand-surface)',
        ink: { DEFAULT: 'var(--brand-text-primary)', muted: 'var(--brand-text-secondary)' },
        hairline: 'var(--brand-hairline)',
        primary: { DEFAULT: 'var(--brand-primary)', foreground: 'var(--brand-on-primary)' },
        success: 'var(--status-success)',
      },
      fontFamily: {
        display: ['var(--type-family-display)'],
        data: 'var(--type-family-data)',
      },
      borderRadius: { card: 'var(--radius-medium)' },
      transitionDuration: { fast: 'var(--motion-duration-fast)' },
      screens: { tablet: '768px' },
      spacing: { gutter: gutter(4) },
    },
  },
};
