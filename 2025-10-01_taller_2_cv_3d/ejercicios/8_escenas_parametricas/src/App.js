import React, { useState } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import * as THREE from "three";

function Escena({ objetos }) {
  return (
    <>
      <ambientLight intensity={0.7} />
      <directionalLight position={[5, 10, 5]} intensity={1} />
      <gridHelper args={[15, 15, "gray", "gray"]} />
      <axesHelper args={[3]} />
      {objetos.map((obj, i) => (
        <mesh
          key={i}
          position={[obj.x, obj.y, obj.z]}
          rotation={[obj.rx, obj.ry, 0]}
          scale={obj.scale}
        >
          {obj.tipo === "cubo" && <boxGeometry args={[1, 1, 1]} />}
          {obj.tipo === "esfera" && <sphereGeometry args={[0.6, 32, 32]} />}
          {obj.tipo === "cono" && <coneGeometry args={[0.6, 1.2, 32]} />}
          <meshStandardMaterial color={obj.color} roughness={0.4} metalness={0.3} />
        </mesh>
      ))}
    </>
  );
}

export default function App() {
  const [objetos, setObjetos] = useState([]);

  const generarEscena = () => {
    const tipos = ["cubo", "esfera", "cono"];
    const nuevos = Array.from({ length: 10 }, () => ({
      tipo: tipos[Math.floor(Math.random() * tipos.length)],
      x: Math.random() * 8 - 4,
      y: Math.random() * 2,
      z: Math.random() * 8 - 4,
      rx: Math.random() * Math.PI,
      ry: Math.random() * Math.PI,
      scale: Math.random() * 0.6 + 0.7,
      color: new THREE.Color(Math.random(), Math.random(), Math.random()),
    }));
    setObjetos(nuevos);
  };

  return (
    <div className="w-full h-screen bg-gradient-to-b from-gray-800 to-gray-900 text-white flex flex-col">
      <button
        onClick={generarEscena}
        className="absolute top-4 left-4 bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded text-white z-10"
      >
        Generar nueva escena
      </button>

      <Canvas camera={{ position: [6, 4, 8], fov: 50 }}>
        <OrbitControls makeDefault enableDamping />
        <Escena objetos={objetos} />
      </Canvas>
    </div>
  );
}
