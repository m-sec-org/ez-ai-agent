import { writeFileSync } from "fs";
import { server } from "../src";

server.ready(() => {
  const openApiJSON = server.swagger();
  writeFileSync("./openapi/schemas.json", JSON.stringify(openApiJSON, null, 2), "utf-8");
  console.log("OpenAPI JSON has been written to schemas.json");

  server.close(() => {
    console.log("Server closed after generating schemas.");
    process.exit(0);
  });
});
