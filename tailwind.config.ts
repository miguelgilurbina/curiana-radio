import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./content/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // Earth tones palette
        earth: {
          50: "#f8f6f3",
          100: "#ede8e1",
          200: "#dcd2c3",
          300: "#c5b59f",
          400: "#b09880",
          500: "#9d7f66",
          600: "#8a6c57",
          700: "#72584a",
          800: "#5f4a3f",
          900: "#4f3e35",
        },
        // Deep blue palette
        deep: {
          50: "#f0f4f8",
          100: "#d9e3ed",
          200: "#b3c7db",
          300: "#8ca6c4",
          400: "#6685ac",
          500: "#4d6d94",
          600: "#3d5777",
          700: "#2f425b",
          800: "#1f2c3e",
          900: "#0f1621",
        },
        // Accent colors
        frequency: "#FF6B35", // Radio frequency orange (88.8 FM badge)
      },
      fontFamily: {
        serif: ["Lora", "Georgia", "serif"],
        sans: ["Inter", "system-ui", "sans-serif"],
      },
      fontSize: {
        // Custom typography scale for long-form reading
        'body': ['1.125rem', { lineHeight: '1.75' }],
        'intro': ['2rem', { lineHeight: '1.25' }],
        'display': ['3.5rem', { lineHeight: '1.1' }],
      },
      spacing: {
        '18': '4.5rem',
        '22': '5.5rem',
      },
      maxWidth: {
        'reading': '65ch', // Optimal line length for reading
      },
    },
  },
  plugins: [],
};

export default config;
