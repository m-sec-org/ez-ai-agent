import { defineConfig } from "@hey-api/openapi-ts";
import dotenv from "dotenv";

dotenv.config({ path: ".env.local" });

export default defineConfig({
  client: "@hey-api/client-fetch",
  input: "../api/openapi/schemas.json",
  output: {
    format: "prettier",
    path: "./src/steel-client",
  },
  types: {
    dates: "types+transform",
    enums: "javascript",
  },
});
