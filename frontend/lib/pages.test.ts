import { expect, test } from "vitest";

import { resolvePage } from "./pages";

test("rejects a page that does not exist", async () => {
  await expect(resolvePage("Missing")).rejects.toThrow("Inertia page not found: Missing");
});
