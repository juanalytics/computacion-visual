import React, { useRef, useMemo, useState } from "react"
import { Canvas, useFrame } from "@react-three/fiber"
import { OrbitControls, Html } from "@react-three/drei"
import * as THREE from "three"

// ----- Simple noise GLSL -----
const noiseGLSL = `
vec3 mod289(vec3 x){return x - floor(x * (1.0 / 289.0)) * 289.0;}
vec2 mod289(vec2 x){return x - floor(x * (1.0 / 289.0)) * 289.0;}
vec3 permute(vec3 x){return mod289(((x*34.0)+1.0)*x);}
float snoise(vec2 v){
  const vec4 C = vec4(0.211324865405187,
                      0.366025403784439,
                     -0.577350269189626,
                      0.024390243902439);
  vec2 i = floor(v + dot(v, C.yy));
  vec2 x0 = v - i + dot(i, C.xx);
  vec2 i1 = (x0.x > x0.y) ? vec2(1.0,0.0) : vec2(0.0,1.0);
  vec4 x12 = x0.xyxy + C.xxzz;
  x12.xy -= i1;
  i = mod289(i);
  vec3 p = permute(permute(
              vec3(i.y + vec3(0.0, i1.y, 1.0)))
              + i.x + vec3(0.0, i1.x, 1.0));
  vec3 m = max(0.5 - vec3(dot(x0,x0),
                          dot(x12.xy,x12.xy),
                          dot(x12.zw,x12.zw)), 0.0);
  m = m*m; m = m*m;
  vec3 x = 2.0 * fract(p * C.www) - 1.0;
  vec3 h = abs(x) - 0.5;
  vec3 ox = floor(x + 0.5);
  vec3 a0 = x - ox;
  m *= 1.79284291400159 -
       0.85373472095314 * (a0*a0 + h*h);
  vec3 g;
  g.x  = a0.x * x0.x + h.x * x0.y;
  g.yz = a0.yz * x12.xz + h.yz * x12.yw;
  return 130.0 * dot(m, g);
}
`

const vertexShader = `
varying vec2 vUv;
varying vec3 vNormal;
void main(){
  vUv = uv;
  vNormal = normal;
  gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0);
}
`

const fragmentShader = `
precision highp float;
varying vec2 vUv;
varying vec3 vNormal;
uniform float uTime;
uniform float uEvent;
${noiseGLSL}

void main(){
  vec2 uv = vUv;
  uv.x += sin(uTime*0.3 + uv.y*6.0)*0.05;
  uv.y += cos(uTime*0.2 + uv.x*6.0)*0.03;
  float n = snoise(uv*3.0 + uTime*0.4);

  vec3 base = vec3(0.05,0.1,0.25);
  vec3 emissive = vec3(0.2,0.6,1.0) * pow(abs(n),1.8);

  float pulse = exp(-3.0*abs(sin(uEvent*3.1415)));
  emissive += vec3(1.0,0.6,0.2)*pulse;

  vec3 color = base + emissive;
  color = color/(color+vec3(1.0)); // tone map
  gl_FragColor = vec4(color,1.0);
}
`

function DynamicSurface({ eventValue }) {
  const mat = useRef()
  useFrame(({ clock }) => {
    if (mat.current) {
      mat.current.uniforms.uTime.value = clock.getElapsedTime()
      mat.current.uniforms.uEvent.value = eventValue
    }
  })

  const shaderMat = useMemo(() => new THREE.ShaderMaterial({
    vertexShader,
    fragmentShader,
    uniforms: {
      uTime: { value: 0 },
      uEvent: { value: 0 },
    }
  }), [])

  return (
    <mesh>
      <sphereGeometry args={[1.4, 128, 128]} />
      <primitive object={shaderMat} ref={mat} attach="material" />
    </mesh>
  )
}

function Particles({ trigger }) {
  const ref = useRef()
  const count = 1500

  const positions = useMemo(() => {
    const arr = new Float32Array(count * 3)
    for (let i = 0; i < count; i++) {
      const r = Math.random() * 3
      const a = Math.random() * Math.PI * 2
      const b = Math.acos(Math.random()*2 - 1)
      arr[i*3]   = Math.sin(b)*Math.cos(a)*r
      arr[i*3+1] = Math.sin(b)*Math.sin(a)*r
      arr[i*3+2] = Math.cos(b)*r
    }
    return arr
  }, [])

  useFrame(() => {
    if (trigger.current && ref.current) {
      const pos = ref.current.geometry.attributes.position.array
      for (let i = 0; i < count; i++) {
        pos[i*3]   *= 1.02
        pos[i*3+1] *= 1.02
        pos[i*3+2] *= 1.02
      }
      ref.current.geometry.attributes.position.needsUpdate = true
      trigger.current = false
    }
  })

  return (
    <points ref={ref}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          array={positions}
          count={positions.length/3}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial size={0.02} color="#ffffff" depthWrite={false} />
    </points>
  )
}

function Scene() {
  const [event, setEvent] = useState(0)
  const burst = useRef(false)

  const fire = () => {
    setEvent(e => e + 1)
    burst.current = true
  }

  return (
    <>
      <ambientLight intensity={0.3} />
      <directionalLight position={[5,5,5]} />
      <DynamicSurface eventValue={event} />
      <Particles trigger={burst} />
      <OrbitControls enableZoom={true} enablePan={true} enableRotate={true} />

      {/* Botón flotante en pantalla */}
      <Html position={[0, -2, 0]}>
        <button
          style={{ 
            padding: '10px 20px', 
            cursor: 'pointer', 
            background: '#111', 
            color: '#fff', 
            border: '1px solid #fff',
            borderRadius: '5px'
          }}
          onClick={fire}>
          Disparar Evento
        </button>
      </Html>
    </>
  )
}

export default function App(){
  return (
    <div style={{
      width: "100vw",
      height: "100vh",
      margin: 0,
      padding: 0,
      overflow: "hidden",
      background: "#090f1e"
    }}>
      <Canvas camera={{ position:[0,0,6], fov:50 }}>
        <Scene />
      </Canvas>
    </div>
  )
}