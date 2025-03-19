import {
  redDark,
  redDarkA,
  greenDark,
  greenDarkA,
  amberDark,
  amberDarkA,
  indigoDark,
  indigoDarkA,
  slateDark,
  slateDarkA,
  skyDark,
  skyDarkA,
} from "@radix-ui/colors";

type ReplaceKeyPrefix<
  Obj,
  OldPrefix extends string,
  NewPrefix extends string,
> = {
  [K in keyof Obj as K extends `${OldPrefix}${infer Rest}`
    ? `${NewPrefix}${Rest}`
    : never]: Obj[K];
};
function renameKeysWithPrefix<
  Obj extends Record<string, string>,
  OldPrefix extends string,
  NewPrefix extends string,
>(
  obj: Obj,
  oldPrefix: OldPrefix,
  newPrefix: NewPrefix,
): ReplaceKeyPrefix<Obj, OldPrefix, NewPrefix> {
  const result: any = {};

  Object.keys(obj).forEach((key) => {
    const newKey = key.replace(oldPrefix, newPrefix);
    result[newKey] = obj[key];
  });

  return result;
}

export const theme = {
  colors: {
    white: "#FFFFFF",
    black: "#1C2024",
    panelDefault: "#1D1D21B2",
    ...renameKeysWithPrefix(indigoDark, "indigo", "accent"),
    ...renameKeysWithPrefix(indigoDarkA, "indigoA", "accentAlpha"),
    ...renameKeysWithPrefix(slateDark, "slate", "neutral"),
    ...renameKeysWithPrefix(slateDarkA, "slateA", "neutralAlpha"),
    ...renameKeysWithPrefix(redDark, "red", "error"),
    ...renameKeysWithPrefix(redDarkA, "redA", "errorAlpha"),
    ...renameKeysWithPrefix(greenDark, "green", "success"),
    ...renameKeysWithPrefix(greenDarkA, "greenA", "successAlpha"),
    ...renameKeysWithPrefix(amberDark, "amber", "warning"),
    ...renameKeysWithPrefix(amberDarkA, "amberA", "warningAlpha"),
    ...renameKeysWithPrefix(skyDark, "sky", "info"),
    ...renameKeysWithPrefix(skyDarkA, "skyA", "infoAlpha"),
  },
};

export type Theme = typeof theme;
