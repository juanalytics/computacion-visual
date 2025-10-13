import { Canvas } from "@react-three/fiber"
import { OrbitControls, PerspectiveCamera, OrthographicCamera } from "@react-three/drei"
import { useState } from "react"

export default function App() {
  const [isOrtho, setIsOrtho] = useState(false)
  const [fov, setFov] = useState(50)
  const [size, setSize] = useState(5)

  return (
    <div className="w-screen h-screen relative">
      <Canvas shadows>
        {/* Cámara alternable */}
        {isOrtho ? (
          <OrthographicCamera makeDefault zoom={50 / size} position={[5, 5, 5]} />
        ) : (
          <PerspectiveCamera makeDefault fov={fov} position={[5, 5, 5]} />
        )}
        <OrbitControls />

        {/* Luz */}
        <ambientLight intensity={0.5} />
        <directionalLight position={[10, 10, 10]} intensity={1} castShadow />

        {/* Suelo */}
        <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
          <planeGeometry args={[100, 100]} />
          <meshStandardMaterial color="#999999" />
        </mesh>

        {/* Objetos de referencia */}
        <mesh position={[0, 0.5, 0]} castShadow>
          <boxGeometry args={[1, 1, 1]} />
          <meshStandardMaterial color="red" />
        </mesh>

        <mesh position={[0, 0.5, -5]} castShadow>
          <sphereGeometry args={[0.7, 32, 32]} />
          <meshStandardMaterial color="blue" />
        </mesh>

        <mesh position={[0, 0.5, 5]} castShadow>
          <coneGeometry args={[0.6, 1.5, 32]} />
          <meshStandardMaterial color="green" />
        </mesh>
      </Canvas>

      {/* Interfaz de usuario */}
      <div className="absolute top-2 left-2 bg-white/80 p-3 rounded-lg shadow-md text-sm space-y-2">
        <label className="flex items-center gap-2">
          <input
            type="checkbox"
            checked={isOrtho}
            onChange={() => setIsOrtho(!isOrtho)}
          />
          <span>Modo Ortográfico</span>
        </label>

        {!isOrtho && (
          <div>
            <label>FOV: {fov}</label>
            <input
              type="range"
              min="20"
              max="100"
              value={fov}
              onChange={e => setFov(+e.target.value)}
            />
          </div>
        )}

        {isOrtho && (
          <div>
            <label>Size: {size}</label>
            <input
              type="range"
              min="1"
              max="10"
              value={size}
              onChange={e => setSize(+e.target.value)}
            />
          </div>
        )}
      </div>
    </div>
  )
}
