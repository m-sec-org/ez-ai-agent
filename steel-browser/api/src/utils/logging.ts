export const updateLog = async (logUrl: string, log: any) => {
  try {
    const response = await fetch(logUrl, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(log),
    });
    if (!response.ok) {
      const error = await response.text();
      console.error("Failed to update log", error);
    }
  } catch (e: unknown) {
    console.error(e);
  }
};
