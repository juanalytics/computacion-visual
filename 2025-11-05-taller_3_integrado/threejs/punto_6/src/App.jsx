/**
 * App.jsx
 * React Three Fiber demo: keyboard/mouse/touch input + HTML UI + physics collisions + synced visual effects
 *
 * Dependencias (instalar con npm/yarn):
 *   react, react-dom
 *   three
 *   @react-three/fiber
 *   @react-three/drei
 *   @react-three/cannon
 *   tailwindcss (opcional para estilos)
 *
 * Ejemplo de instalación:
 *   npm install react react-dom three @react-three/fiber @react-three/drei @react-three/cannon
 *
 * Ejecutar: importa este componente en tu entry (index.jsx) y renderiza <App />.
 */

import React, { useRef, useState, useEffect, useCallback } from 'react'
import { Canvas, useFrame, useThree } from '@react-three/fiber'
import { OrbitControls, Html, Text, Sparkles } from '@react-three/drei'
import { Physics, useBox, usePlane } from '@react-three/cannon'

// --------------------------
// Helper: simple keyboard hook
// --------------------------
function useKeyboard() {
  const keys = useRef({})
  useEffect(() => {
    const down = (e) => { keys.current[e.code] = true }
    const up = (e) => { keys.current[e.code] = false }
    window.addEventListener('keydown', down)
    window.addEventListener('keyup', up)
    return () => {
      window.removeEventListener('keydown', down)
      window.removeEventListener('keyup', up)
    }
  }, [])
  return keys
}

// --------------------------
// Ground (static plane)
// --------------------------
function Ground(props) {
  const [ref] = usePlane(() => ({ rotation: [-Math.PI / 2, 0, 0], ...props }))
  return (
    <mesh ref={ref} receiveShadow>
      <planeGeometry args={[50, 50]} />
      <meshStandardMaterial color="#777" />
    </mesh>
  )
}

// --------------------------
// Player (a physics box controlled by keyboard)
// --------------------------
function Player({ speed = 5, onTrigger }) {
  const keys = useKeyboard()
  // create a dynamic box body
  const [ref, api] = useBox(() => ({ mass: 1, position: [0, 1, 0], args: [1, 1, 1] }))

  // keyboard movement -> apply velocity
  useFrame((_, dt) => {
    const k = keys.current
    let vx = 0
    let vz = 0
    if (k['KeyW'] || k['ArrowUp']) vz -= 1
    if (k['KeyS'] || k['ArrowDown']) vz += 1
    if (k['KeyA'] || k['ArrowLeft']) vx -= 1
    if (k['KeyD'] || k['ArrowRight']) vx += 1
    // normalize
    const len = Math.hypot(vx, vz) || 1
    api.velocity.set((vx / len) * speed, 0, (vz / len) * speed)
  })

  // collision listener: call onTrigger when colliding
  useEffect(() => {
    const obj = ref.current
    if (!obj) return
    const handler = (e) => {
      // e.body is the other body
      if (onTrigger) onTrigger(e)
    }
    obj.addEventListener('collide', handler)
    return () => obj.removeEventListener('collide', handler)
  }, [ref, onTrigger])

  return (
    <mesh ref={ref} castShadow>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color="#1e90ff" />
    </mesh>
  )
}

// --------------------------
// InteractiveBox: clickable / touchable and physics-enabled
// --------------------------
function InteractiveBox({ position = [2, 1, 0], id = 'box', onActivate }) {
  const [hovered, setHovered] = useState(false)
  const [active, setActive] = useState(false)
  const [ref] = useBox(() => ({ mass: 0, position, args: [1, 1, 1] })) // static trigger

  // collision handler will be attached by parent player as 'collide' event
  // pointer events for mouse/touch
  return (
    <mesh
      ref={ref}
      onPointerOver={(e) => { e.stopPropagation(); setHovered(true) }}
      onPointerOut={(e) => { e.stopPropagation(); setHovered(false) }}
      onPointerDown={(e) => { e.stopPropagation(); setActive(a => !a); if (onActivate) onActivate(id) }}
      castShadow
    >
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color={active ? '#ff6b6b' : hovered ? '#ffd43b' : '#4caf50'} />
      {/* Small HTML label */}
      <Html distanceFactor={8} center>
        <div style={{ padding: 6, background: 'rgba(255,255,255,0.9)', borderRadius: 6, fontSize: 12 }}>
          {id}
        </div>
      </Html>
    </mesh>
  )
}

// --------------------------
// Simple visual effect: explosion / sparkles
// --------------------------
function HitEffect({ position, show }) {
  // Using drei's Sparkles for a quick effect when show=true
  if (!show) return null
  return (
    <group position={position}>
      <Sparkles count={60} scale={2} />
    </group>
  )
}

// --------------------------
// Main Scene
// --------------------------
function Scene({ uiState, onBoxActivate }) {
  const [hit, setHit] = useState(null)

  // When player collides with any object, we get the event here and trigger effect
  const handlePlayerTrigger = useCallback((e) => {
    // position of contact
    const contact = e.contact
    const pos = contact ? [contact.ri.x + contact.rj.x, contact.ri.y + contact.rj.y, contact.ri.z + contact.rj.z] : [0, 1, 0]
    // we simply store where to show the effect
    setHit({ pos: e.contact.rj ? [e.contact.rj.x, e.contact.rj.y, e.contact.rj.z] : [0, 1, 0], time: Date.now() })
  }, [])

  // auto-hide effect after some time
  useEffect(() => {
    if (!hit) return
    const t = setTimeout(() => setHit(null), 900)
    return () => clearTimeout(t)
  }, [hit])

  return (
    <>
      <ambientLight intensity={0.6} />
      <directionalLight position={[5, 10, 5]} intensity={0.8} castShadow />

      <Physics gravity={[0, -9.81 * uiState.gravityScale, 0]}>
        <Ground />

        <Player speed={uiState.playerSpeed} onTrigger={handlePlayerTrigger} />

        {/* Some interactive boxes that can be clicked or trigger collisions */}
        <InteractiveBox id={'Box-A'} position={[2, 1, -2]} onActivate={onBoxActivate} />
        <InteractiveBox id={'Box-B'} position={[-2, 1, -2]} onActivate={onBoxActivate} />

        {/* A heavier dynamic box to show collision physics */}
        <DynamicThrowBox position={[0, 6, -4]} />
      </Physics>

      {/* visual effect */}
      {hit && <HitEffect position={hit.pos} show={true} />}

      <OrbitControls />
    </>
  )
}

// --------------------------
// A dynamic box that falls and collides — demonstrates collision listeners too
// --------------------------
function DynamicThrowBox({ position = [0, 6, 0] }) {
  const [ref, api] = useBox(() => ({ mass: 2, position, args: [1.2, 1.2, 1.2] }))
  // rotate for visual interest
  useFrame((state, dt) => {
    api.angularVelocity.set(0.2, 0.5, 0.1)
  })
  // local collide reaction that briefly scales the box using a small animation
  useEffect(() => {
    const obj = ref.current
    if (!obj) return
    const onCollide = (e) => {
      // visual feedback: flash material (we'll modify its scale as cheap feedback)
      const mesh = obj.children && obj.children[0]
      if (!mesh) return
      const orig = mesh.scale.clone()
      let t = 0
      const id = setInterval(() => {
        t += 0.05
        mesh.scale.setScalar(1 + 0.2 * Math.sin(t * Math.PI * 2))
        if (t > 0.6) {
          mesh.scale.copy(orig)
          clearInterval(id)
        }
      }, 16)
    }
    obj.addEventListener('collide', onCollide)
    return () => obj.removeEventListener('collide', onCollide)
  }, [ref])

  return (
    <mesh ref={ref} castShadow>
      <boxGeometry args={[1.2, 1.2, 1.2]} />
      <meshStandardMaterial color="#8a2be2" />
    </mesh>
  )
}

// --------------------------
// HTML UI overlay (buttons + sliders)
// --------------------------
function UIOverlay({ uiState, setUiState, onThrow }) {
  return (
    <div className="absolute top-4 left-4 w-80 p-3 bg-white/80 rounded shadow-lg backdrop-blur-sm" style={{ fontFamily: 'Inter, system-ui' }}>
      <h3 className="text-lg font-semibold">Controls</h3>

      <div className="mt-2">
        <label className="block text-sm">Player speed: {uiState.playerSpeed.toFixed(1)}</label>
        <input type="range" min="0" max="12" step="0.1" value={uiState.playerSpeed} onChange={(e) => setUiState(s => ({ ...s, playerSpeed: parseFloat(e.target.value) }))} />
      </div>

      <div className="mt-2">
        <label className="block text-sm">Gravity scale: {uiState.gravityScale.toFixed(2)}</label>
        <input type="range" min="0" max="2" step="0.01" value={uiState.gravityScale} onChange={(e) => setUiState(s => ({ ...s, gravityScale: parseFloat(e.target.value) }))} />
      </div>

      <div className="mt-3 flex gap-2">
        <button onClick={() => setUiState(s => ({ ...s, resetScene: s.resetScene + 1 }))} className="px-3 py-1 rounded bg-blue-600 text-white">Reset</button>
        <button onClick={onThrow} className="px-3 py-1 rounded bg-red-500 text-white">Throw Box</button>
      </div>

      <div className="mt-3 text-xs text-gray-700">Input: WASD / Arrow keys to move. Click or touch boxes to toggle.</div>
    </div>
  )
}

// --------------------------
// App: wiring everything together
// --------------------------
export default function App() {
  const [uiState, setUiState] = useState({ playerSpeed: 5, gravityScale: 1.0, resetScene: 0 })
  const [lastActivated, setLastActivated] = useState(null)

  // handle box activation from InteractiveBox
  const handleBoxActivate = useCallback((id) => {
    setLastActivated({ id, time: Date.now() })
  }, [])

  // throw a new dynamic box into the scene by toggling resetScene counter
  const handleThrow = useCallback(() => {
    // The simplest way without global physics api: toggle resetScene so scene can respond.
    setUiState(s => ({ ...s, resetScene: s.resetScene + 1 }))
  }, [])

  return (
    <div style={{ width: '100vw', height: '100vh' }}>
      <Canvas shadows camera={{ position: [5, 5, 8], fov: 50 }}>
        <Scene uiState={uiState} onBoxActivate={handleBoxActivate} />
      </Canvas>

      {/* HTML UI overlay */}
      <UIOverlay uiState={uiState} setUiState={setUiState} onThrow={handleThrow} />

      {/* Small HUD at bottom-right showing recent events */}
      <div style={{ position: 'absolute', right: 12, bottom: 12, background: 'rgba(0,0,0,0.6)', color: 'white', padding: '8px 12px', borderRadius: 8, fontSize: 13 }}>
        <div style={{ fontWeight: 600 }}>Event Log</div>
        <div style={{ marginTop: 6 }}>
          {lastActivated ? <div>Box clicked: {lastActivated.id}</div> : <div>No recent clicks</div>}
        </div>
      </div>
    </div>
  )
}
