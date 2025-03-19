export enum ProtocolCommands {
  "Input.dispatchKeyEvent" = "Input.dispatchKeyEvent",
  "Input.emulateTouchFromMouseEvent" = "Input.emulateTouchFromMouseEvent",
}

export enum HostCommands {
  "start" = "start",
  "run" = "run",
  "close" = "close",
  "setViewport" = "setViewport",
}

export enum WorkerCommands {
  "startComplete" = "startComplete",
  "runComplete" = "runComplete",
  "screencastFrame" = "screencastFrame",
  "browserClose" = "browserClose",
  "error" = "error",
}

export interface Message {
  command: string;
  data: any;
}
