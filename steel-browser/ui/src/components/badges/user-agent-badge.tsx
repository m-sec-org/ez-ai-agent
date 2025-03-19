import { DesktopIcon, CopyIcon } from "@radix-ui/react-icons";
import { Badge } from "@/components/ui/badge";
import { ChromeIcon } from "@/components/icons/ChromeIcon";
import { copyText } from "@/utils/toasts";
import UAParser from "ua-parser-js";
export function UserAgentBadge({ userAgent }: { userAgent: string }) {
  const parser = new UAParser(userAgent);

  return (
    <Badge
      variant="secondary"
      className="text-[var(--gray-11)] bg-[var(--gray-a3)] gap-2 py-1 px-3 flex items-center justify-between max-w-fit"
    >
      <DesktopIcon width={16} height={16} color="var(--gray-11)" />{" "}
      {parser.getDevice().type || "Desktop"}
      <ChromeIcon width={16} height={16} color="var(--gray-11)" />{" "}
      {`${parser.getBrowser().name} (v${parser.getBrowser().version})`}
      <CopyIcon
        width={16}
        height={16}
        className="cursor-pointer text-[var(--gray-11)] hover:text-[var(--gray-12)]"
        onClick={() => copyText(userAgent, "User Agent")}
      />
    </Badge>
  );
}
