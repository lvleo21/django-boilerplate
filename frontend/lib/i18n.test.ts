import i18next from "i18next";
import { expect, test } from "vitest";

test("returns the pt-BR source text, interpolated, while there is no catalog", () => {
  expect(i18next.t("Olá, {{name}}", { name: "Ana" })).toBe("Olá, Ana");
});
