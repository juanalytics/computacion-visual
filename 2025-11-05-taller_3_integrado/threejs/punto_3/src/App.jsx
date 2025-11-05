/*
Fixed: React Three Shaders Playground + Interacción funcional

Instrucciones:
  npx create-vite@latest my-shaders -- --template react
  cd my-shaders
  npm install three @react-three/fiber @react-three/drei
  Reemplazar src/App.jsx con este archivo
  npm run dev
*/

import React, { useRef, useMemo, useState, useEffect } from 'react'
import { createRoot } from 'react-dom/client'
import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls, Stats } from '@react-three/drei'
import * as THREE from 'three'

// ---------------- GLSL SHADERS ----------------
const vertex_common = `
precision highp float;
precision highp int;
varying vec2 vUv;
varying vec3 vPosition;
void main() {
  vUv = uv;
  vPosition = position;
  gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}
`;

const frag_pos_time = `
precision highp float;
uniform float uTime;
uniform vec2 uMouse;
varying vec2 vUv;
varying vec3 vPosition;
vec3 palette(float t){
  return vec3(0.5 + 0.5*cos(6.2831*(t+vec3(0.0,0.33,0.66))));
}
void main(){
  float height = (vPosition.y + 1.0) * 0.5;
  float stripe = sin((vPosition.x + uTime*0.8) * 6.0);
  float t = clamp(height + 0.25*stripe, 0.0, 1.0);
  vec2 m = uMouse - vUv;
  float dist = length(m);
  float glow = smoothstep(0.2, 0.0, dist);
  vec3 col = palette(t + 0.2*sin(uTime*0.6));
  col += vec3(1.0,0.6,0.1) * glow * 0.6;
  gl_FragColor = vec4(col, 1.0);
}
`;

const vert_toon = `
precision highp float;
varying vec3 vNormal;
varying vec3 vWorldPos;
void main(){
  vNormal = normalMatrix * normal;
  vWorldPos = (modelMatrix * vec4(position,1.0)).xyz;
  gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0);
}
`;

const frag_toon = `
precision highp float;
uniform vec3 uLightPos;
uniform vec3 uBaseColor;
uniform float uHover;
varying vec3 vNormal;
varying vec3 vWorldPos;
void main(){
  vec3 N = normalize(vNormal);
  vec3 L = normalize(uLightPos - vWorldPos);
  float lambert = dot(N,L);
  float bands = floor(lambert * 4.0) / 4.0;
  bands = clamp(bands, 0.05, 1.0);
  float rim = pow(1.0 - max(0.0, dot(N, normalize(-L))), 2.0) * 0.25;
  vec3 col = uBaseColor * (0.2 + 0.9 * bands) + rim;
  col += vec3(1.0,0.8,0.3) * uHover * 0.7;
  gl_FragColor = vec4(col, 1.0);
}
`;

const vert_uv_dist = `
precision highp float;
varying vec2 vUv;
varying vec3 vPos;
uniform float uTime;
void main(){
  vUv = uv;
  vPos = position;
  vec3 pos = position;
  pos.z += 0.05 * sin(uTime + position.x * 4.0) * sin(uTime*0.5 + position.y * 3.0);
  gl_Position = projectionMatrix * modelViewMatrix * vec4(pos,1.0);
}
`;

const frag_uv_dist = `
precision highp float;
uniform float uTime;
uniform float uHover;
uniform float uClick;
varying vec2 vUv;
varying vec3 vPos;
float noise(vec2 p){
  float n=0.0;
  n += 0.5 * sin(p.x*3.0 + p.y*2.1 + uTime*1.1);
  n += 0.25 * sin(p.x*7.0 - p.y*4.2 + uTime*1.7);
  n += 0.12 * sin(p.x*12.0 + p.y*9.0 + uTime*2.3);
  return n;
}
void main(){
  vec2 uv = vUv;
  uv += 0.06 * noise(uv * 3.0 + uTime*0.6);
  float mapA = smoothstep(-0.1, 0.1, sin((uv.x+uv.y*1.3)*10.0 + uTime*1.3));
  float mapB = smoothstep(0.0, 0.6, noise(uv*4.0));
  vec3 colA = vec3(0.9, 0.4, 0.2) * mapA;
  vec3 colB = vec3(0.2, 0.4, 0.9) * mapB;
  vec3 final = mix(colA, colB, 0.5 + 0.5*sin(uTime*0.7 + vPos.y*2.0));
  final += vec3(0.8,0.7,0.1) * uHover * 0.6;
  if(uClick > 0.5){
    final = vec3(1.0) - final;
  }
  gl_FragColor = vec4(final, 1.0);
}
`;

// ---------------- Helpers ----------------
function useMouseGlobal() {
  const mouse = useRef([0.5, 0.5]);
  useEffect(() => {
    const onMove = (e) => {
      mouse.current = [e.clientX / window.innerWidth, 1.0 - e.clientY / window.innerHeight];
    };
    window.addEventListener('mousemove', onMove);
    return () => window.removeEventListener('mousemove', onMove);
  }, []);
  return mouse;
}

// ---------------- Components corregidos ----------------
function Ground() {
  const materialRef = useRef(null);
  const mouse = useMouseGlobal();

  const material = useMemo(() => {
    return new THREE.ShaderMaterial({
      vertexShader: vertex_common,
      fragmentShader: frag_pos_time,
      uniforms: {
        uTime: { value: 0 },
        uMouse: { value: new THREE.Vector2(0.5, 0.5) }
      },
      side: THREE.DoubleSide
    });
  }, []);

  // linkea ref y limpia
  useEffect(() => {
    materialRef.current = material;
    return () => {
      material.dispose();
    };
  }, [material]);

  useFrame(({ clock }) => {
    if (materialRef.current) {
      materialRef.current.uniforms.uTime.value = clock.getElapsedTime();
      materialRef.current.uniforms.uMouse.value.set(...mouse.current);
    }
  });

  return (
    <mesh material={material} rotation-x={-Math.PI/2} receiveShadow>
      <planeGeometry args={[6, 6, 64, 64]} />
    </mesh>
  );
}

function ToonSphere() {
  const materialRef = useRef(null);
  const [hover, setHover] = useState(false);

  const material = useMemo(() => new THREE.ShaderMaterial({
    vertexShader: vert_toon,
    fragmentShader: frag_toon,
    uniforms: {
      uLightPos: { value: new THREE.Vector3(5,3,2) },
      uBaseColor: { value: new THREE.Color(0.9,0.7,0.3) },
      uHover: { value: 0 }
    }
  }), []);

  useEffect(() => {
    materialRef.current = material;
    return () => material.dispose();
  }, [material]);

  useFrame(() => {
    if (materialRef.current) {
      const t = performance.now() * 0.001;
      materialRef.current.uniforms.uLightPos.value.set(Math.sin(t)*5, 3 + Math.cos(t)*2, 2);
      materialRef.current.uniforms.uHover.value = hover ? 1.0 : 0.0;
    }
  });

  return (
    <mesh
      position={[-2, 1.2, 0]}
      material={material}
      onPointerEnter={(e) => { e.stopPropagation(); setHover(true); }}
      onPointerLeave={(e) => { e.stopPropagation(); setHover(false); }}
      castShadow
    >
      <sphereGeometry args={[1, 64, 64]} />
      {/* Overlay wireframe opcional */}
      <mesh>
        <sphereGeometry args={[1.001, 32, 32]} />
        <meshBasicMaterial wireframe opacity={0.25} transparent />
      </mesh>
    </mesh>
  );
}

function ProceduralBox() {
  const materialRef = useRef(null);
  const [hover, setHover] = useState(false);
  const [clicked, setClicked] = useState(false);

  const material = useMemo(() => new THREE.ShaderMaterial({
    vertexShader: vert_uv_dist,
    fragmentShader: frag_uv_dist,
    uniforms: {
      uTime: { value: 0 },
      uHover: { value: 0 },
      uClick: { value: 0 }
    },
    side: THREE.DoubleSide
  }), []);

  useEffect(() => {
    materialRef.current = material;
    return () => material.dispose();
  }, [material]);

  useFrame(({ clock }) => {
    if (materialRef.current) {
      materialRef.current.uniforms.uTime.value = clock.getElapsedTime();
      materialRef.current.uniforms.uHover.value = hover ? 1.0 : 0.0;
      materialRef.current.uniforms.uClick.value = clicked ? 1.0 : 0.0;
    }
  });

  return (
    <mesh
      position={[2, 1.2, 0]}
      material={material}
      onPointerEnter={(e) => { e.stopPropagation(); setHover(true); }}
      onPointerLeave={(e) => { e.stopPropagation(); setHover(false); }}
      onClick={(e) => { e.stopPropagation(); setClicked(v => !v); }}
      castShadow
    >
      <boxGeometry args={[1.6, 1.6, 1.6, 64, 64, 64]} />
    </mesh>
  );
}

// ---------------- App ----------------
export default function App() {
  return (
    <div style={{ width: '100vw', height: '100vh' }}>
      <Canvas camera={{ position: [0, 3, 8], fov: 50 }}>
        <ambientLight intensity={0.25} />
        <directionalLight position={[5, 10, 5]} intensity={0.6} />

        <Ground />
        <ToonSphere />
        <ProceduralBox />

        <OrbitControls enableDamping />
        <Stats />
      </Canvas>

      <div style={{
        position: 'absolute', left: 12, top: 12, color: '#fff',
        fontFamily: 'monospace', pointerEvents: 'none'
      }}>
        <h3 style={{ margin: 0 }}>Shaders + Interacción (Corregido)</h3>
        <small>Hover para iluminar • Click en la caja para invertir colores</small>
      </div>
    </div>
  );
}

if (typeof document !== 'undefined') {
  const root = document.getElementById('root') || (() => {
    const d = document.createElement('div'); d.id = 'root'; document.body.appendChild(d);
    return d;
  })();
  createRoot(root).render(<App />);
}
