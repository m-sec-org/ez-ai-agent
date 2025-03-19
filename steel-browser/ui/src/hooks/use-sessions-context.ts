import { SessionsContext } from "@/contexts/sessions-context";
import { SessionsContextType } from "@/contexts/sessions-context/sessions-context.types";
import { useContext } from "react";

export function useSessionsContext(): SessionsContextType {
  const context = useContext(SessionsContext);
  if (!context) {
    throw new Error(
      "useSessionsContext must be used within an SessionsProvider"
    );
  }
  return context;
}
