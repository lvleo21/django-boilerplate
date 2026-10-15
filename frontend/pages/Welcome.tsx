import { Head } from "@inertiajs/react";
import { BookOpenIcon, LayoutDashboardIcon, type LucideIcon, RocketIcon } from "lucide-react";
import { useTranslation } from "react-i18next";

import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

type WelcomeProps = {
  project_name: string;
  django_version: string;
  admin_url: string;
};

type Resource = {
  href: string;
  title: string;
  description: string;
  icon: LucideIcon;
};

export default function Welcome({ project_name, django_version, admin_url }: WelcomeProps) {
  const { t } = useTranslation();

  const resources: Resource[] = [
    {
      href: "https://docs.djangoproject.com/pt-br/5.2/",
      title: t("Django"),
      description: t("Models, views, admin e tudo o que roda no backend."),
      icon: BookOpenIcon,
    },
    {
      href: "https://inertiajs.com/",
      title: t("Inertia.js"),
      description: t("Como as views do Django renderizam páginas React."),
      icon: BookOpenIcon,
    },
    {
      href: "https://react.dev/",
      title: t("React"),
      description: t("Componentes, hooks e o restante do frontend."),
      icon: BookOpenIcon,
    },
    {
      href: admin_url,
      title: t("Admin"),
      description: t("Painel de administração do Django."),
      icon: LayoutDashboardIcon,
    },
  ];

  return (
    <>
      <Head title={project_name} />
      <main className="mx-auto flex min-h-[100dvh] w-full max-w-3xl flex-col justify-center gap-10 px-6 py-16">
        <div className="flex flex-col items-start gap-4">
          <RocketIcon className="size-10 text-primary" aria-hidden="true" />
          <h1 className="text-3xl font-bold tracking-tight sm:text-4xl">
            {t("A instalação funcionou com sucesso! Parabéns!")}
          </h1>
          <p className="max-w-[60ch] text-lg text-muted-foreground">
            {t(
              "Você está vendo esta página porque o {{project_name}} está rodando com Django {{django_version}}, Inertia e React.",
              { project_name, django_version },
            )}
          </p>
        </div>

        <ul className="grid gap-4 sm:grid-cols-2">
          {resources.map(({ href, title, description, icon: Icon }) => (
            <li key={href}>
              <a href={href} className="block h-full rounded-xl focus-visible:ring-3 focus-visible:ring-ring/50 focus-visible:outline-none">
                <Card className="h-full transition-colors hover:bg-muted">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Icon className="size-4" aria-hidden="true" />
                      {title}
                    </CardTitle>
                    <CardDescription>{description}</CardDescription>
                  </CardHeader>
                </Card>
              </a>
            </li>
          ))}
        </ul>
      </main>
    </>
  );
}
