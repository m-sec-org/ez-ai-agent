export function getErrors(e: unknown) {
  let error: string;
  if (typeof e === "string") {
    error = e;
  } else if (e instanceof Error) {
    error = e.message;
  } else {
    error = "Unknown error";
  }

  return error;
}
