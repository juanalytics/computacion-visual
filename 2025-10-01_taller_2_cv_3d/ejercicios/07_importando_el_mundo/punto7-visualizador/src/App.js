import React, { useState, useEffect } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls, useGLTF, Html } from "@react-three/drei";
import { OBJLoader } from "three/examples/jsm/loaders/OBJLoader";
import { STLLoader } from "three/examples/jsm/loaders/STLLoader";
import * as THREE from "three";

// 🔹 Carga y prepara el modelo según formato
function Modelo({ formato, setInfo }) {
  const gltf = useGLTF("/models/scene.gltf"); // ✅ Hook en el nivel superior
  const [model, setModel] = useState(null);

  useEffect(() => {
    async function cargarModelo() {
      let obj;

      if (formato === "OBJ") {
        obj = await new OBJLoader().loadAsync("/models/bunny.obj");
      } else if (formato === "STL") {
        const geometry = await new STLLoader().loadAsync(
          "/models/Utah_teapot_(solid).stl"
        );
        const material = new THREE.MeshStandardMaterial({ color: 0xaaaaaa });
        obj = new THREE.Mesh(geometry, material); // ✅ se convierte a Mesh
      } else {
        obj = gltf.scene.clone(true);
      }

      prepararModelo(obj);
      setModel(obj);
    }

    cargarModelo();
  }, [formato, gltf]);

 function prepararModelo(obj) {
  // Calcular caja, tamaño y centro
  const box = new THREE.Box3().setFromObject(obj);
  const size = box.getSize(new THREE.Vector3());
  const center = box.getCenter(new THREE.Vector3());

  // 🔹 Mover modelo al origen y escalar
  obj.position.sub(center);
  obj.position.set(0, 0, 0);
  obj.rotation.set(0, 0, 0);
  const escala = 1 / Math.max(size.x, size.y, size.z);
  obj.scale.setScalar(escala * 2);

  // 🔹 Contar vértices y caras
  let vertices = 0,
    caras = 0;
  obj.traverse((child) => {
    if (child.isMesh) {
      const geo = child.geometry;
      vertices += geo.attributes.position.count;
      if (geo.index) caras += geo.index.count / 3;
    }
  });

  setInfo({ formato, vertices, caras });
}


  if (!model) return null;
  return <primitive object={model} />;
}

// 🔹 HUD con datos
function HUD({ info }) {
  return (
    <Html position={[0, 1.5, 0]} center>
      <div className="bg-black/70 text-white px-4 py-2 rounded-lg text-sm text-center">
        <p className="font-bold text-blue-400">{info.formato}</p>
        <p>Vértices: {info.vertices}</p>
        <p>Caras: {info.caras}</p>
      </div>
    </Html>
  );
}

// 🔹 Componente principal
export default function App() {
  const [formato, setFormato] = useState("OBJ");
  const [info, setInfo] = useState({ formato: "OBJ", vertices: 0, caras: 0 });

  return (
    <div className="w-full h-screen bg-gray-900 text-white flex flex-col items-center">
      <h1 className="text-2xl mt-4">Comparador de Modelos 3D</h1>

      <div className="flex gap-3 mt-3">
        {["OBJ", "STL", "GLTF"].map((f) => (
          <button
            key={f}
            onClick={() => setFormato(f)}
            className={`px-4 py-2 rounded ${
              formato === f ? "bg-blue-600" : "bg-gray-700 hover:bg-gray-600"
            }`}
          >
            {f}
          </button>
        ))}
      </div>

      <div className="flex-1 w-full">
        <Canvas camera={{ position: [0, 0.5, 3], fov: 50 }}>
          <ambientLight intensity={0.8} />
          <directionalLight position={[2, 2, 2]} intensity={1} />
          <OrbitControls />
          <Modelo formato={formato} setInfo={setInfo} />
          <HUD info={info} />
        </Canvas>
      </div>
    </div>
  );
}
