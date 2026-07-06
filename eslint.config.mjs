import coreWebVitals from "eslint-config-next/core-web-vitals";
import typescript from "eslint-config-next/typescript";

/** @type {import('eslint').Linter.Config[]} */
const config = [
  {
    ignores: [
      "**/.next/**",
      "**/node_modules/**",
      "out/**",
      "build/**",
      ".claude/**",
      "proyecto-linguistico-caquetío/**",
    ],
  },
  ...coreWebVitals,
  ...typescript,
  {
    // Honrar el prefijo `_` y el patrón omit-via-rest ({ id: _id, ...rest }):
    // variables deliberadamente descartadas no deben marcarse como sin usar.
    rules: {
      "@typescript-eslint/no-unused-vars": [
        "warn",
        { argsIgnorePattern: "^_", varsIgnorePattern: "^_", ignoreRestSiblings: true },
      ],
    },
  },
];

export default config;
