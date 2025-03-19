const { join } = require("path");

/**
 * @type {import("puppeteer").Configuration}
 */
module.exports = {
  defaultProduct: "chrome",
  cacheDirectory: join(__dirname, ".cache", "puppeteer"),
};
