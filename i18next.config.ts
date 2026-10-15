import { defineConfig } from "i18next-cli";

// `yarn i18n:extract` grava um catálogo JSON plano por idioma, com o texto-fonte
// em pt-BR como chave (ver frontend/lib/i18n.ts).
export default defineConfig({
  locales: ["pt-BR"],
  extract: {
    input: ["frontend/**/*.{ts,tsx}"],
    ignore: ["frontend/**/*.test.{ts,tsx}", "frontend/test/**", "frontend/dist/**"],
    output: "frontend/locales/{{language}}.json",
    defaultNS: false,
    keySeparator: false,
    nsSeparator: false,
  },
});
