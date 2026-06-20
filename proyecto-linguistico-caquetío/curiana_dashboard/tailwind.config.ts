import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // Paleta Caquetía: ocre, siena, verde golfete, blanco arena
        caquetio:   "#C47A2B",
        wayunaiki:  "#2E7D4F",
        lokono:     "#5B4FCF",
        taino:      "#B04040",
        "proto-arahuaco": "#6D8A9E",
        arena:      "#F5EDD6",
        oscuro:     "#1C1510",
      },
    },
  },
  plugins: [],
};

export default config;
