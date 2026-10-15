import { screen, waitFor } from "@testing-library/react";
import { expect, test } from "vitest";

import { inertiaPage, renderPage } from "@/tests/inertia";

function renderWelcome() {
  return renderPage(
    inertiaPage("Welcome", "/", {
      project_name: "Minha Loja",
      django_version: "5.2.1",
      admin_url: "/staff/",
    }),
  );
}

test("shows the success heading", async () => {
  await renderWelcome();

  expect(
    await screen.findByRole("heading", { level: 1, name: "A instalação funcionou com sucesso! Parabéns!" }),
  ).toBeInTheDocument();
});

test("shows the project name and the Django version", async () => {
  await renderWelcome();

  expect(
    await screen.findByText(
      "Você está vendo esta página porque o Minha Loja está rodando com Django 5.2.1, Inertia e React.",
    ),
  ).toBeInTheDocument();
});

test("links to the admin URL sent by the view", async () => {
  await renderWelcome();

  expect(await screen.findByRole("link", { name: /Admin/ })).toHaveAttribute("href", "/staff/");
});

test("uses the project name as the document title", async () => {
  await renderWelcome();

  await waitFor(() => expect(document.title).toBe("Minha Loja"));
});
