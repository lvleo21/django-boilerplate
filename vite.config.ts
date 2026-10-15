/// <reference types="vitest/config" />
import { fileURLToPath, URL } from "node:url";

import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  // Precisa bater com o STATIC_URL do Django.
  base: "/static/",
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./frontend", import.meta.url)),
    },
  },
  server: {
    // Escuta em todas as interfaces para ser acessível de fora do container
    // do compose; o navegador continua usando localhost (ver `origin`).
    host: true,
    port: 5173,
    strictPort: true,
    // Assets referenciados em CSS/JS vêm do servidor do Vite, não da origem
    // do Django.
    origin: "http://localhost:5173",
  },
  test: {
    environment: "jsdom",
    setupFiles: ["frontend/tests/setup.ts"],
    // Folga para os findBy* em imports de página a frio (tests/setup.ts).
    testTimeout: 15_000,
    projects: [
      {
        extends: true,
        test: {
          name: "unit",
          include: ["frontend/**/*.test.{ts,tsx}"],
          exclude: ["frontend/tests/integration/**"],
        },
      },
      {
        extends: true,
        test: {
          name: "integration",
          include: ["frontend/tests/integration/**/*.test.{ts,tsx}"],
        },
      },
    ],
  },
  build: {
    // Incluído no STATICFILES_DIRS do Django.
    outDir: "frontend/dist",
    emptyOutDir: true,
    manifest: "manifest.json",
    rolldownOptions: {
      input: "frontend/main.tsx",
    },
  },
});
