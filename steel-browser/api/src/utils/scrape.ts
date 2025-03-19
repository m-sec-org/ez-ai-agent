import { Readability } from "@mozilla/readability";
import { JSDOM } from "jsdom";
import Turndown from "turndown";

type ReadabilityResult = {
  title: string;
  content: string;
  textContent: string;
  length: number;
  excerpt: string;
  byline: string;
  dir: string;
  siteName: string;
  lang: string;
  publishedTime: string;
};

export function getReadabilityContent(htmlString: string): ReadabilityResult | null {
  const doc = new JSDOM(htmlString);
  const reader = new Readability(doc.window.document);
  const articleContent = reader.parse();
  if (!articleContent) return null;
  return articleContent;
}

export const cleanHtml = (html: string): string => {
  const blacklistedElements = new Set([
    "head",
    "title",
    "meta",
    "script",
    "style",
    "path",
    "svg",
    "br",
    "hr",
    "link",
    "object",
    "embed",
  ]);

  const blacklistedAttributes = [
    "style",
    "ping",
    "src",
    "item.*",
    "aria.*",
    "js.*",
    "data-.*",
    "role",
    "tabindex",
    "onerror",
  ];

  const dom = new JSDOM(html);
  const document = dom.window.document;

  // Remove blacklisted elements
  blacklistedElements.forEach((tag) => {
    const elements = document.querySelectorAll(tag);
    elements.forEach((element) => {
      element.remove();
    });
  });

  // Remove blacklisted attributes
  const elements = document.querySelectorAll("*");
  elements.forEach((element) => {
    blacklistedAttributes.forEach((attrPattern) => {
      const regex = new RegExp(`^${attrPattern}$`);
      Array.from(element.attributes).forEach((attr: any) => {
        if (regex.test(attr.name)) {
          element.removeAttribute(attr.name);
        }
      });
    });
  });

  // Remove empty elements
  elements.forEach((element) => {
    if (!element.hasAttributes() && element.textContent?.trim() === "") {
      element.remove();
    }
  });

  const sourceCode = document.documentElement.outerHTML;

  return sourceCode;
};

export const getMarkdown = (html: string): string => {
  const turndownService = new Turndown();
  const markdown = turndownService.turndown(html);
  return markdown;
};
