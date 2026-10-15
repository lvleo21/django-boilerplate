import type { ComponentType } from "react";

// Testes ao lado das páginas ficam de fora, então nunca entram no bundle.
const pages = import.meta.glob<{ default: ComponentType }>([
  "../pages/**/*.tsx",
  "!../pages/**/*.test.tsx",
]);

export async function resolvePage(name: string) {
  const page = pages[`../pages/${name}.tsx`];
  if (!page) {
    throw new Error(`Inertia page not found: ${name}`);
  }
  return (await page()).default;
}
