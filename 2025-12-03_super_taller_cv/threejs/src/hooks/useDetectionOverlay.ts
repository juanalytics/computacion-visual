import { create } from "zustand";

export type Box = {
  id: number;
  label: string;
  confidence: number;
  bbox: [number, number, number, number];
};

type FrameSize = { width: number; height: number } | null;

type DetectionState = {
  boxes: Box[];
  frame: FrameSize;
  update: (items: Box[], frame?: FrameSize) => void;
};

export const useDetectionStore = create<DetectionState>((set) => ({
  boxes: [],
  frame: null,
  update: (items: DetectionState["boxes"], frame: FrameSize = null) =>
    set({ boxes: items, frame }),
}));

