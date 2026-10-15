import { defineConfig, devices } from "@playwright/test";

const DJANGO_PORT = 8010;
const baseURL = `http://localhost:${DJANGO_PORT}`;

/**
 * Testes end-to-end contra um servidor Django real.
 *
 * `manage.py testserver` cria um banco de teste descartável (SQLite em memória,
 * pela DATABASE_URL abaixo), carrega as fixtures e2e e serve o app, então nunca
 * toca nos dados de dev.
 * Os assets vêm do servidor do Vite (DEBUG -> modo dev do django-vite).
 */
export default defineConfig({
  testDir: "e2e",
  fullyParallel: false,
  workers: 1,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  reporter: "list",
  use: {
    baseURL,
    trace: "retain-on-failure",
  },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
  webServer: [
    {
      command: "yarn dev",
      url: "http://localhost:5173/static/@vite/client",
      reuseExistingServer: true,
    },
    {
      command: `poetry run python backend/manage.py testserver e2e_users --noinput --addrport localhost:${DJANGO_PORT}`,
      // Variáveis do ambiente vencem as do .env (o django-environ não as sobrescreve).
      env: {
        DJANGO_SETTINGS_MODULE: "config.settings.test",
        SECRET_KEY: process.env.SECRET_KEY ?? "e2e-secret-key",
        DEBUG: "True",
        DATABASE_URL: "sqlite:///e2e.sqlite3",
        USE_CELERY: "False",
      },
      url: `${baseURL}/`,
      reuseExistingServer: false,
      timeout: 120_000,
    },
  ],
});
