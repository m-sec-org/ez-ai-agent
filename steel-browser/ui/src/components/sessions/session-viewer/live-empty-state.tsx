import { Globe } from "@/components/illustrations/globe";
import { Badge } from "@/components/ui/badge";
import { copyText } from "@/utils/toasts";
import { CopyIcon } from "@radix-ui/react-icons";
import { SessionDetails } from "@/steel-client";

export function LiveEmptyState({ session }: { session: SessionDetails }) {
  return (
    <div className="flex flex-col w-full flex-1 px-24 pt-10 bg-[url('/grid.svg')] bg-no-repeat bg-center border-[var(--gray-6)] bg-cover items-center">
      <div className="flex flex-col gap-4 max-w-[396px] mx-auto">
        <div className="flex flex-col gap-4 mx-auto">
          <h1 className="text-primary text-2xl  font-medium text-center">
            Your session is live!
          </h1>
          <p className="text-muted-foreground text-lg text-center max-w-[280px]">
            You'll be able to view and monitor it from here.
          </p>
        </div>
        <div className="flex justify-center items-center w-full">
          <Globe />
        </div>
        <div className="flex flex-col gap-2 justify-center items-center">
          <p className="text-muted-foreground text-lg text-center max-w-[280px]">
            Connect via this websocket URL
          </p>
          <Badge
            variant="secondary"
            className="text-primary bg-[var(--gray-3)] py-2 px-3 flex items-center justify-between min-w-[400px] max-w-[700px] hover:bg-[var(--gray-4)] ml-auto"
          >
            <span className="text-xs text-muted-foreground font-regular">
              {session?.websocketUrl.substring(0, 50)}
            </span>
            <div
              className="flex items-center ml-auto hover:cursor-pointer"
              onClick={() =>
                copyText(session?.websocketUrl || "", "Websocket URL")
              }
            >
              <CopyIcon className="w-4 h-4" />
            </div>
          </Badge>
        </div>
      </div>
    </div>
  );
}
