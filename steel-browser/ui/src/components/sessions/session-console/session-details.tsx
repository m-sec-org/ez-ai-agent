import { useSessionsContext } from "@/hooks/use-sessions-context";
import { Skeleton } from "@radix-ui/themes";
import { ReleaseSessionDialog } from "../release-session-dialog";
import { Button } from "@/components/ui/button";

export default function SessionDetails({ id }: { id: string | null }) {
  const { useSession } = useSessionsContext();
  const { data: session, isLoading, isError } = useSession(id!);

  return (
    <div className="w-full h-full overflow-y-auto overflow-x-scroll bg-[var(--gray-2)] p-3 pt-8 font-mono text-xs flex flex-col">
      {isLoading && (
        <>
          <div className="flex flex-col gap-2 py-2 border-b border-[var(--gray-6)]">
            <Skeleton className="w-full h-4 border-b border-[var(--gray-6)]" />
          </div>
          <div className="flex flex-col gap-2 py-2 border-b border-[var(--gray-6)]">
            <Skeleton className="w-full h-4 border-b border-[var(--gray-6)]" />
          </div>
          <div className="flex flex-col gap-2 py-2 border-b border-[var(--gray-6)]">
            <Skeleton className="w-full h-4 border-b border-[var(--gray-6)]" />
          </div>
          <div className="flex flex-col gap-2 py-2 border-b border-[var(--gray-6)]">
            <Skeleton className="w-full h-4 border-b border-[var(--gray-6)]" />
          </div>
          <div className="flex flex-col gap-2 py-2 border-b border-[var(--gray-6)]">
            <Skeleton className="w-full h-4 border-b border-[var(--gray-6)]" />
          </div>
          <div className="flex flex-col gap-2 py-2 border-b border-[var(--gray-6)]">
            <Skeleton className="w-full h-4 border-b border-[var(--gray-6)]" />
          </div>
          <div className="flex flex-col gap-2 py-2 border-b border-[var(--gray-6)]">
            <Skeleton className="w-full h-4 border-b border-[var(--gray-6)]" />
          </div>
          <div className="flex flex-col gap-2 py-2 border-b border-[var(--gray-6)]">
            <Skeleton className="w-full h-4 border-b border-[var(--gray-6)]" />
          </div>
          <div className="flex flex-col gap-2 py-2 border-b border-[var(--gray-6)]">
            <Skeleton className="w-full h-4 border-b border-[var(--gray-6)]" />
          </div>
        </>
      )}
      {isError && <div>Error loading session</div>}
      {session && (
        <>
          <div className="flex w-full flex-row gap-2 justify-between py-2 border-b border-[var(--gray-6)]">
            <div className="text-[var(--gray-11)]">ID</div>
            <div className="text-right">{session.id}</div>
          </div>

          <div className="flex w-full flex-row gap-2 justify-between py-2 border-b border-[var(--gray-6)]">
            <div className="text-[var(--gray-11)]">Timestamp</div>
            <div className="text-right">
              {session.createdAt.toLocaleString()}
            </div>
          </div>

          <div className="flex w-full flex-row gap-2 justify-between py-2 border-b border-[var(--gray-6)]">
            <div className="text-[var(--gray-11)]">Duration</div>
            <div className="text-right">{session.duration}</div>
          </div>

          <div className="flex w-full flex-row gap-2 justify-between py-2 border-b border-[var(--gray-6)]">
            <div className="text-[var(--gray-11)]">User Agent</div>
            <div className="text-right">{session.userAgent}</div>
          </div>

          <div className="flex w-full flex-row gap-2 justify-between py-2 border-b border-[var(--gray-6)]">
            <div className="text-[var(--gray-11)]">Auto-captcha</div>
            <div className="text-right">{session.solveCaptcha?.toString()}</div>
          </div>

          <div className="flex w-full flex-row gap-2 justify-between py-2 border-b border-[var(--gray-6)]">
            <div className="text-[var(--gray-11)]">isSelenium</div>
            <div className="text-right">{session.isSelenium?.toString()}</div>
          </div>

          <div className="flex w-full flex-row gap-2 justify-between py-2 border-b border-[var(--gray-6)]">
            <div className="text-[var(--gray-11)]">Websocket URL</div>
            <div className="text-right">
              {session.websocketUrl.slice(0, 30)}
            </div>
          </div>
        </>
      )}
      {session?.status === "live" && (
        <div className="mt-auto border-t border-[var(--gray-6)] py-4">
          <ReleaseSessionDialog id={id!}>
            <Button
              variant="outline"
              className="flex w-full bg-transparent text-[var(--red-11)] border-[var(--red-7)] hover:bg-[var(--red-3)]"
            >
              Release Session
            </Button>
          </ReleaseSessionDialog>
        </div>
      )}
    </div>
  );
}
