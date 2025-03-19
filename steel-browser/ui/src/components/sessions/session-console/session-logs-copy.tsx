// import { env } from "@/env";
import { useEffect, useState, useRef } from "react"
import Markdown from "react-markdown"

export default function SessionLogs({}: { id: string }) {
    const [logs, setLogs] = useState<any[]>([])
    const [url, setUrl] = useState<string>("")
    const consoleRef = useRef<HTMLDivElement>(null)
    const [eventSource, setEventSource] = useState<EventSource | null>(null)
    const [isConnected, setIsConnected] = useState(false)

    const addLog = (message: string, type: string = "Console") => {
        setLogs((prevLogs) => [
            ...prevLogs,
            {
                id: Date.now(),
                timestamp: new Date().toISOString(),
                type,
                text: JSON.stringify({ message }),
            },
        ])
    }

    const startTest = async () => {
        if (!url) {
            alert("请输入目标 URL")
            return
        }

        // 清空之前的日志
        setLogs([])
        setIsConnected(false)

        // 关闭之前的 EventSource
        if (eventSource && eventSource.readyState !== EventSource.CLOSED) {
            eventSource.close()
        }

        try {
            // 先发送开始测试请求
            const response = await fetch("http://127.0.0.1:5555/start_test", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ url: "pentest " + url }),
            })

            const data = await response.json()
            if (data.status !== "success") {
                alert("启动测试失败: " + data.message)
                return
            }

            addLog("测试任务已启动")

            // 创建新的 EventSource
            const newEventSource = new EventSource("http://127.0.0.1:5555/stream_output", {
                withCredentials: false,
            })
            setEventSource(newEventSource)

            // 连接打开时的处理
            newEventSource.onopen = () => {
                console.log("SSE连接已建立")
                setIsConnected(true)
                addLog("SSE连接已建立")
            }

            // 消息处理
            newEventSource.onmessage = (event) => {
                try {
                    console.log("收到SSE消息:", event.data)
                    if (!event.data) return

                    // 尝试解析消息
                    let messageText = event.data
                    if (messageText.startsWith("data: ")) {
                        messageText = messageText.substring(6)
                    }

                    // 处理多行消息
                    const lines = messageText.split("\n")
                    for (const line of lines) {
                        if (line && line.trim()) {
                            addLog(line.trim())
                        }
                    }
                } catch (error) {
                    console.error("消息处理错误:", error)
                    addLog("消息处理错误: " + String(error), "Error")
                }
            }

            // 错误处理
            newEventSource.onerror = (error) => {
                console.error("SSE error:", error)
                // 只有在连接已建立的情况下才显示错误
                if (isConnected) {
                    addLog("SSE连接错误", "Error")
                    setIsConnected(false)
                    newEventSource.close()
                }
            }
        } catch (error) {
            console.error("操作失败:", error)
            addLog("操作失败: " + (error instanceof Error ? error.message : String(error)), "Error")
            setIsConnected(false)
        }
    }

    // 组件卸载时清理
    useEffect(() => {
        return () => {
            if (eventSource && eventSource.readyState !== EventSource.CLOSED) {
                eventSource.close()
                setIsConnected(false)
            }
        }
    }, [eventSource])

    // 自动滚动到底部
    useEffect(() => {
        if (consoleRef.current) {
            consoleRef.current.scrollTop = consoleRef.current.scrollHeight
        }
    }, [logs])

    // useEffect(() => {
    //   const a: any = []
    //   for(let i = 0;i < 100;i++) {
    //     a.push({
    //       id: Date.now(),
    //       timestamp: new Date().toISOString(),
    //       type: "Console",
    //       text: JSON.stringify({ message: "aaa" })
    //     })
    //   }
    //   setLogs(a)
    // }, [])

    const logTypeToColor = (type: string) => {
        if (type === "Console") return "var(--cyan-a11)"
        if (type === "Request") return "var(--pink-a11)"
        if (type === "Response") return "var(--green-a11)"
        if (type === "Error") return "var(--red-a11)"
        return "var(--gray-11)"
    }

    const logTypeToFormat = (type: string, log: Record<string, any>) => {
        if (type === "Console") {
            if (log.message) {
                return log.message
                    .replace(/^\d{2}:\d{2}:\d{2}\.\d{3}\s+(INFO|WARN|ERROR|DEBUG)\s+/, "")
                    .replace("\n", "")
                    .replace("\t", "")
            }
            return log.text
        }
        if (type === "Request") return `[${log.method}] ${log.url}`
        if (type === "Response") return `[${log.status}] ${log.url}`
        if (type === "Error") return log.message
        if (type === "Navigation") return log.url || JSON.stringify(log)
        return log.message || JSON.stringify(log)
    }

    return (
        <div className="flex flex-col h-full">
            <div className="flex items-center gap-2 p-2 bg-[var(--gray-3)]">
                <input
                    type="text"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    placeholder="请输入目标 URL"
                    className="px-3 py-1 rounded bg-[var(--gray-2)] text-[var(--gray-12)] border border-[var(--gray-7)]"
                />
                <button
                    onClick={startTest}
                    disabled={isConnected}
                    className={`px-3 py-1 rounded ${isConnected ? "bg-[var(--gray-9)] cursor-not-allowed" : "bg-[var(--cyan-9)] hover:bg-[var(--cyan-10)]"} text-white`}
                >
                    {isConnected ? "测试中..." : "开始测试"}
                </button>
            </div>

            <div ref={consoleRef} className="flex-1 pb-14 overflow-y-auto overflow-x-scroll bg-[var(--gray-2)] p-2 font-mono text-xs">
                {logs.length === 0 && <p className="text-[var(--gray-11)]">暂无测试输出...</p>}
                {logs.map((log) => {
                    const logBody = JSON.parse(log.text)
                    const cleanMessage = logTypeToFormat(log.type, logBody)

                    return (
                        <pre key={log.id} className="text-overflow-ellipsis mb-1 whitespace-pre-wrap">
                            <span className="text-[var(--gray-11)]">
                                {new Date(log.timestamp).toLocaleTimeString("en-US", {
                                    hour: "2-digit",
                                    minute: "2-digit",
                                    second: "2-digit",
                                    hour12: false,
                                })}
                            </span>{" "}
                            <span style={{ color: logTypeToColor(log.type) }}>[{log.type}]</span> <Markdown>{cleanMessage}</Markdown>
                        </pre>
                    )
                })}
            </div>
        </div>
    )
}
