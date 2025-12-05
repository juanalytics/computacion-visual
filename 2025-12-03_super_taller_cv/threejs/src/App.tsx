import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import { Suspense } from "react";
import { useWsCommands } from "./hooks/useWsCommands";
import { Scene } from "./components/Scene";
import { Overlay } from "./components/Overlay";
import "./App.css";

function App() {
  const { status } = useWsCommands();

  return (
    <div className="app">
      <div className="hud">
        <h1>Three.js WS Stage</h1>
        <p>Status: {status}</p>
      </div>
      <div className="canvas-wrapper">
        <Canvas
          camera={{ position: [0, 1.5, 4], fov: 60 }}
          shadows
          style={{ width: "100%", height: "100%" }}
        >
          <color attach="background" args={["#050505"]} />
          <fog attach="fog" args={["#050505", 4, 12]} />
          <Suspense fallback={null}>
            <Scene />
          </Suspense>
          <OrbitControls enablePan={false} />
        </Canvas>
        <Overlay />
      </div>
    </div>
  );
}

export default App;
