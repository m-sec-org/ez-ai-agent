import { CopyIcon } from "@radix-ui/react-icons";
import { Badge } from "@/components/ui/badge";
import { copyText } from "@/utils/toasts";

export function WebsocketUrlBadge({ url }: { url: string }) {
  return (
    <Badge
      variant="secondary"
      className="text-[var(--gray-11)] gap-2 py-1 px-3 flex items-center justify-between max-w-fit	"
    >
      {url}
      <CopyIcon
        className="cursor-pointer text-[var(--gray-11)] hover:text-[var(--gray-12)]"
        width={16}
        height={16}
        onClick={() => copyText(url, "Websocket URL")}
      />
    </Badge>
  );
}
