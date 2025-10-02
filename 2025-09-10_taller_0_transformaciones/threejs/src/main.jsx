import React from 'react'
import ReactDOM from 'react-dom/client'
import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls } from '@react-three/drei'

// Cubo con traslación senoidal
function CuboTraslacion() {
  const meshRef = React.useRef()
  
  useFrame((state) => {
    if (meshRef.current) {
      const t = state.clock.elapsedTime
      meshRef.current.position.x = 2 * Math.sin(t)
      meshRef.current.position.y = Math.cos(t * 1.5)
      meshRef.current.position.z = 0.5 * Math.sin(t * 0.8)
    }
  })
  
  return (
    <mesh ref={meshRef} castShadow>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color="red" />
    </mesh>
  )
}

// Esfera con rotación continua
function EsferaRotacion() {
  const meshRef = React.useRef()
  
  useFrame((state) => {
    if (meshRef.current) {
      const t = state.clock.elapsedTime
      meshRef.current.rotation.x = t * 0.5
      meshRef.current.rotation.y = t * 0.8
      meshRef.current.rotation.z = t * 0.3
      meshRef.current.position.set(-3, 2, 0)
    }
  })
  
  return (
    <mesh ref={meshRef} castShadow>
      <sphereGeometry args={[0.8, 32, 32]} />
      <meshStandardMaterial color="green" />
    </mesh>
  )
}

// Cono con escala oscilante
function ConoEscala() {
  const meshRef = React.useRef()
  
  useFrame((state) => {
    if (meshRef.current) {
      const t = state.clock.elapsedTime
      const escala = 1 + 0.5 * Math.sin(t * 2)
      meshRef.current.scale.set(escala, escala, escala)
      meshRef.current.position.set(3, -2, 0)
    }
  })
  
  return (
    <mesh ref={meshRef} castShadow>
      <coneGeometry args={[0.8, 1.5, 8]} />
      <meshStandardMaterial color="blue" />
    </mesh>
  )
}

// Torus con transformación compuesta
function TorusCompuesto() {
  const meshRef = React.useRef()
  
  useFrame((state) => {
    if (meshRef.current) {
      const t = state.clock.elapsedTime
      
      // Traslación circular
      const radio = 2.5
      meshRef.current.position.x = radio * Math.cos(t * 0.5)
      meshRef.current.position.z = radio * Math.sin(t * 0.5)
      meshRef.current.position.y = Math.sin(t) * 0.5
      
      // Rotación múltiple
      meshRef.current.rotation.x = t * 1.2
      meshRef.current.rotation.y = t * 0.8
      
      // Escala variable
      const escala = 0.8 + 0.3 * Math.sin(t * 3)
      meshRef.current.scale.set(escala, escala, escala)
    }
  })
  
  return (
    <mesh ref={meshRef} castShadow>
      <torusGeometry args={[0.6, 0.3, 16, 32]} />
      <meshStandardMaterial color="yellow" />
    </mesh>
  )
}

// Plano de suelo
function Suelo() {
  return (
    <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -3, 0]} receiveShadow>
      <planeGeometry args={[20, 20]} />
      <meshStandardMaterial color="#444444" />
    </mesh>
  )
}

function App() {
  return (
    <div style={{ width: '100vw', height: '100vh', fontFamily: 'Arial, sans-serif' }}>
      {/* Header */}
      <div style={{
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        background: 'rgba(0,0,0,0.8)',
        color: 'white',
        padding: '1rem',
        zIndex: 100,
        textAlign: 'center'
      }}>
        <h1 style={{ margin: 0, fontSize: '1.5rem' }}>
          🎉 Taller 0 - Transformaciones Básicas en Three.js
        </h1>
        <p style={{ margin: '0.5rem 0 0 0', fontSize: '0.9rem' }}>
          Hola Mundo Visual con React Three Fiber
        </p>
      </div>
      
      {/* Canvas 3D */}
      <Canvas
        camera={{ position: [5, 5, 5], fov: 75 }}
        shadows
        style={{ background: 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)' }}
      >
        {/* Iluminación */}
        <ambientLight intensity={0.4} />
        <directionalLight 
          position={[10, 10, 5]} 
          intensity={1}
          castShadow
          shadow-mapSize={[2048, 2048]}
        />
        
        {/* Controles de órbita */}
        <OrbitControls 
          enablePan={true}
          enableZoom={true}
          enableRotate={true}
        />
        
        {/* Objetos con transformaciones */}
        <CuboTraslacion />
        <EsferaRotacion />
        <ConoEscala />
        <TorusCompuesto />
        
        {/* Suelo */}
        <Suelo />
        
        {/* Ejes de coordenadas */}
        <axesHelper args={[3]} />
      </Canvas>
      
      {/* Footer con información */}
      <div style={{
        position: 'absolute',
        bottom: 0,
        left: 0,
        right: 0,
        background: 'rgba(0,0,0,0.8)',
        color: 'white',
        padding: '1rem',
        display: 'grid',
        gridTemplateColumns: '1fr 1fr',
        gap: '2rem',
        fontSize: '0.8rem'
      }}>
        <div>
          <h3 style={{ margin: '0 0 0.5rem 0', color: '#4a90e2' }}>Controles:</h3>
          <ul style={{ margin: 0, paddingLeft: '1rem' }}>
            <li><strong>Mouse:</strong> Rotar cámara</li>
            <li><strong>Scroll:</strong> Zoom</li>
            <li><strong>Click derecho + arrastrar:</strong> Pan</li>
          </ul>
        </div>
        
        <div>
          <h3 style={{ margin: '0 0 0.5rem 0', color: '#4a90e2' }}>Transformaciones:</h3>
          <ul style={{ margin: 0, paddingLeft: '1rem' }}>
            <li><strong>Cubo Rojo:</strong> Traslación senoidal</li>
            <li><strong>Esfera Verde:</strong> Rotación continua</li>
            <li><strong>Cono Azul:</strong> Escala oscilante</li>
            <li><strong>Torus Amarillo:</strong> Transformación compuesta</li>
          </ul>
        </div>
      </div>
    </div>
  )
}

const root = ReactDOM.createRoot(document.getElementById('app'))
root.render(<App />)
