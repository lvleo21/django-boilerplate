import { expect, test } from "@playwright/test";

test("a visitor opens the home page and sees the success message", async ({ page }) => {
  await page.goto("/");

  await expect(
    page.getByRole("heading", { level: 1, name: "A instalação funcionou com sucesso! Parabéns!" }),
  ).toBeVisible();
});

// Criado por apps/account/fixtures/e2e_users.json.
const ADMIN = { username: "e2e_admin", password: "e2e-pass-123" };

test("the admin card takes the visitor to the admin login", async ({ page }) => {
  await page.goto("/");

  await page.getByRole("link", { name: /Admin/ }).click();

  await expect(page).toHaveURL(/\/staff\/login\//);
});

test("an admin logs in through the admin card and reaches the admin index", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("link", { name: /Admin/ }).click();

  await page.locator("#id_username").fill(ADMIN.username);
  await page.locator("#id_password").fill(ADMIN.password);
  await page.locator("input[type=submit]").click();

  await expect(page).toHaveURL("/staff/");
});
