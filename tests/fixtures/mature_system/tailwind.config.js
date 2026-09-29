const preset = require('./tokens/tailwind-preset');

module.exports = {
  presets: [preset],
  content: ['./site/**/*.{tsx,html}'],
  darkMode: ['class', '[data-theme="dark"]'],
  theme: {
    extend: {
      maxWidth: { prose: '68ch' },
    },
  },
};
