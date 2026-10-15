import "@inertiajs/core";

// Props compartilhadas com toda página por apps.core.middlewares.inertia
// (`errors` já faz parte do tipo de props de página do próprio Inertia).
declare module "@inertiajs/core" {
  export interface InertiaConfig {
    sharedPageProps: {
      language: string;
    };
  }
}
