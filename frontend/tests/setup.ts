import "@testing-library/jest-dom/vitest";

import { cleanup, configure } from "@testing-library/react";
import { afterAll, afterEach, beforeAll } from "vitest";

import { setupI18n } from "@/lib/i18n";

import { server } from "./server";

// A primeira visita a uma página importa o módulo a frio (vários segundos com
// os arquivos de teste em paralelo); o padrão de 1s deixa os findBy* instáveis.
configure({ asyncUtilTimeout: 5000 });

// Mesmo idioma que o Django compartilha por padrão (tests/inertia.tsx: sharedProps).
await setupI18n("pt-br");

// O jsdom não implementa scroll; o Inertia rola para o topo após as visitas.
window.scrollTo = () => {};

beforeAll(() => server.listen({ onUnhandledFrame: "error" }));
afterEach(() => {
  cleanup();
  server.resetHandlers();
});
afterAll(() => server.close());
