import { useDetectionStore } from "../hooks/useDetectionOverlay";
import "./Overlay.css";

export function Overlay() {
  const boxes = useDetectionStore((state) => state.boxes);
  const frame = useDetectionStore((state) => state.frame);

  const width = frame?.width ?? 1;
  const height = frame?.height ?? 1;

  return (
    <div className="overlay">
      {boxes.map((box) => {
        const left = clamp(box.bbox[0] / width);
        const top = clamp(box.bbox[1] / height);
        const w = clamp((box.bbox[2] - box.bbox[0]) / width);
        const h = clamp((box.bbox[3] - box.bbox[1]) / height);

        return (
          <div
            key={box.id}
            className="bbox"
            style={{
              left: `${left * 100}%`,
              top: `${top * 100}%`,
              width: `${w * 100}%`,
              height: `${h * 100}%`,
            }}
          >
            <span>
              {box.label} {(box.confidence * 100).toFixed(1)}%
            </span>
          </div>
        );
      })}
    </div>
  );
}

const clamp = (value: number, min = 0, max = 1) =>
  Math.min(Math.max(value, min), max);

