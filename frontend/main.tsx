import { createInertiaApp } from "@inertiajs/react";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import { setupI18n } from "@/lib/i18n";
import { resolvePage } from "@/lib/pages";

import "./app.css";

createInertiaApp({
  resolve: resolvePage,
  setup({ el, App, props }) {
    setupI18n(props.initialPage.props.language);
    createRoot(el).render(
      <StrictMode>
        <App {...props} />
      </StrictMode>,
    );
  },
  // Nomes do cookie e do header de CSRF do Django (o padrão do Inertia é o do Laravel).
  http: {
    xsrfCookieName: "csrftoken",
    xsrfHeaderName: "X-CSRFToken",
  },
});
