import { CopyIcon } from "@radix-ui/react-icons";
import { Badge } from "@/components/ui/badge";
import { copyText } from "@/utils/toasts";

export function ProxyBadge({ proxy }: { proxy: string }) {
  return (
    <Badge
      variant="secondary"
      className="text-[var(--gray-11)] bg-[var(--gray-a3)] gap-2 py-1 px-3 flex items-center justify-between max-w-fit	"
    >
      {proxy}
      <CopyIcon
        className="cursor-pointer text-[var(--gray-11)] hover:text-[var(--gray-12)]"
        width={16}
        height={16}
        onClick={() => copyText(proxy, "Proxy IP")}
      />
    </Badge>
  );
}
