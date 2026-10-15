import i18next from "i18next";
import { initReactI18next } from "react-i18next";

/**
 * Inicia o i18next no idioma ativo do Django (a shared prop `language`).
 *
 * As chaves são o texto-fonte em pt-BR e ainda não há catálogo (`resources`
 * vazio), então `t()` devolve o próprio texto, interpolado.
 */
export function setupI18n(language: string) {
  return i18next.use(initReactI18next).init({
    lng: language,
    // Nada a carregar: termina antes do primeiro render (main.tsx não espera).
    initAsync: false,
    fallbackLng: false,
    resources: {},
    keySeparator: false,
    nsSeparator: false,
    // O React já escapa os valores renderizados.
    interpolation: { escapeValue: false },
  });
}
