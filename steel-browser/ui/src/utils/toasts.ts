import { toast } from "@/hooks/use-toast";

export const copyText = (text: string, valueCopied?: string) => {
  navigator.clipboard.writeText(text);
  toast({
    title: valueCopied
      ? `${valueCopied} copied to clipboard`
      : "Text copied to clipboard",
    className: "bg-[var(--gray-1)] border-none text-[var(--gray-12)] px-8 py-6",
    duration: 700,
  });
};
