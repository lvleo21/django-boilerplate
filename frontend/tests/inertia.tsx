import { App } from "@inertiajs/react";
import type { Page } from "@inertiajs/core";
import { render } from "@testing-library/react";
import { HttpResponse } from "msw";

import { resolvePage } from "@/lib/pages";
import type { WelcomeProps } from "@/pages/Welcome";

/**
 * As props de cada página, além das compartilhadas: o que a view do Django
 * manda. Uma fixture que diverge da página não compila. Toda página nova
 * exporta o tipo das props e ganha uma entrada aqui.
 */
type PagePropsByComponent = {
  Welcome: WelcomeProps;
};

/** Props que o Django compartilha com toda página (apps.core.middlewares.inertia). */
export function sharedProps() {
  return {
    language: "pt-br",
    errors: {},
  };
}

/** O objeto de página que o Django envia numa resposta Inertia. */
export function inertiaPage<Component extends keyof PagePropsByComponent>(
  component: Component,
  url: string,
  // `errors`: o que a view devolve quando um formulário é inválido.
  props: PagePropsByComponent[Component] & { errors?: Page["props"]["errors"] },
): Page {
  return {
    component,
    url,
    props: { ...sharedProps(), ...props },
    version: "test",
    encryptHistory: false,
    clearHistory: false,
    rescuedProps: [],
    flash: {},
    rememberedState: {},
  };
}

/** Resposta JSON do Inertia, como o Django devolve a visitas com X-Inertia. */
export function inertiaResponse(page: Page) {
  return HttpResponse.json(page, {
    headers: { "X-Inertia": "true", Vary: "X-Inertia" },
  });
}

/** Renderiza a página dentro de um app Inertia real, na URL da página. */
export async function renderPage(page: Page) {
  window.history.replaceState({}, "", page.url);
  const initialComponent = await resolvePage(page.component);
  return render(
    <App
      initialPage={page}
      initialComponent={initialComponent}
      resolveComponent={resolvePage}
    />,
  );
}
