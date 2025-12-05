import { useFrame, useThree } from "@react-three/fiber";
import { MeshDistortMaterial, Environment } from "@react-three/drei";
import { useEffect, useMemo, useRef, useState } from "react";
import * as THREE from "three";
import { useWsCommands, type CommandPayload } from "../hooks/useWsCommands";

export function Scene() {
  const cubeRef = useRef<THREE.Mesh>(null);
  const lightRef = useRef<THREE.DirectionalLight>(null);
  const { camera } = useThree();

  const [color, setColor] = useState(new THREE.Color("#00aaff"));
  const [pulse, setPulse] = useState(false);
  const [lightOn, setLightOn] = useState(true);
  const [cameraFar, setCameraFar] = useState(false);
  const camNear = useMemo(() => new THREE.Vector3(0, 1.5, 4), []);
  const camFar = useMemo(() => new THREE.Vector3(0, 2.5, 8), []);

  const { register } = useWsCommands();

  useFrame((_, delta) => {
    if (cubeRef.current) {
      cubeRef.current.rotation.x += delta * 0.4;
      cubeRef.current.rotation.y += delta * 0.7;
      if (pulse) {
        const scale = 1 + Math.sin(performance.now() * 0.01) * 0.2;
        cubeRef.current.scale.set(scale, scale, scale);
      } else {
        cubeRef.current.scale.set(1, 1, 1);
      }
    }
    const target = cameraFar ? camFar : camNear;
    camera.position.lerp(target, 0.05);
    camera.lookAt(0, 0, 0);
  });

  useEffect(() => {
    if (lightRef.current) {
      lightRef.current.intensity = lightOn ? 1.2 : 0.2;
    }
  }, [lightOn]);

  const handleCommand = (payload: CommandPayload) => {
    const action = payload.action ?? "unknown";
    if (action === "change_material") {
      const hex = (payload.params?.color as string) ?? randomHex();
      setColor(new THREE.Color(hex));
    } else if (action === "trigger_animation") {
      setPulse(true);
      setTimeout(() => setPulse(false), 600);
    } else if (action === "switch_camera") {
      setCameraFar((prev) => !prev);
    } else if (action === "toggle_light") {
      setLightOn((prev) => !prev);
    }
  };

  useEffect(() => {
    const unregister = register(handleCommand);
    return () => unregister();
  }, [register]);

  return (
    <>
      <Environment preset="studio" />
      <ambientLight intensity={0.4} />
      <directionalLight
        ref={lightRef}
        position={[5, 5, 5]}
        intensity={1.2}
        castShadow
      />
      <mesh ref={cubeRef} castShadow receiveShadow>
        <boxGeometry args={[1, 1, 1]} />
        <MeshDistortMaterial color={color} roughness={0.2} distort={0.1} />
      </mesh>
      <mesh
        rotation={[-Math.PI / 2, 0, 0]}
        position={[0, -0.6, 0]}
        receiveShadow
      >
        <planeGeometry args={[6, 6]} />
        <shadowMaterial opacity={0.3} />
      </mesh>
    </>
  );
}

const randomHex = () => {
  const hue = Math.floor(Math.random() * 360);
  return new THREE.Color(`hsl(${hue}, 70%, 55%)`).getStyle();
};

