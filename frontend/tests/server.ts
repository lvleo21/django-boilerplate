import { setupServer } from "msw/node";

/**
 * Servidor MSW no lugar do Django via HTTP (a fronteira do sistema).
 * Cada teste registra os endpoints que usa com `server.use(...)`.
 */
export const server = setupServer();
