import { useCallback, useEffect, useRef, useState } from "react";
import { useDetectionStore, type Box } from "./useDetectionOverlay";

export type CommandPayload = {
  action?: string;
  params?: Record<string, unknown>;
  source?: string;
};

const listeners = new Set<(payload: CommandPayload) => void>();

export function useWsCommands() {
  const [status, setStatus] = useState<"connecting" | "connected" | "error">(
    "connecting"
  );
  const wsRef = useRef<WebSocket | null>(null);
  const updateBoxes = useDetectionStore((state) => state.update);

  useEffect(() => {
    const url =
      localStorage.getItem("threejs_ws_url") ?? "ws://localhost:8000/ws";
    const ws = new WebSocket(url);
    wsRef.current = ws;

    ws.addEventListener("open", () => setStatus("connected"));
    ws.addEventListener("close", () => setStatus("error"));
    ws.addEventListener("error", () => setStatus("error"));
    ws.addEventListener("message", (event) => {
      try {
        const message = JSON.parse(event.data);
        if (
          message?.type === "command" ||
          message?.type === "fusion_command"
        ) {
          const payload = message.payload ?? {};
          listeners.forEach((cb) => cb(payload));
        } else if (message?.type === "detections") {
          const items = (message.payload?.items ?? []) as Box[];
          const frame = message.payload?.frame ?? null;
          updateBoxes(items, frame);
        }
      } catch (err) {
        console.error("Invalid WS message", err);
      }
    });

    return () => {
      ws.close();
      wsRef.current = null;
    };
  }, [updateBoxes]);

  const register = useCallback((cb: (payload: CommandPayload) => void) => {
    listeners.add(cb);
    return () => {
      listeners.delete(cb);
    };
  }, []);

  return { status, register };
}

