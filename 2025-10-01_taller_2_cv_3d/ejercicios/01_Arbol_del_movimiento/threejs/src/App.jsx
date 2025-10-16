import { Canvas } from '@react-three/fiber'
import { OrbitControls, Text } from '@react-three/drei'
import { useControls } from 'leva'
import './App.css'

// Componente para la escena abstracta (cubos/esferas/cilindros)
function AbstractHierarchy() {
  // Controles para el padre (nivel 1)
  const parentControls = useControls('Padre (Nivel 1)', {
    rotation: { value: [0, 0, 0], min: -Math.PI, max: Math.PI, step: 0.1 },
    position: { value: [0, 0, 0], min: -5, max: 5, step: 0.1 },
    scale: { value: 1, min: 0.5, max: 2, step: 0.1 }
  })

  // Controles para los hijos (nivel 2)
  const childControls = useControls('Hijos (Nivel 2)', {
    child1Rotation: { value: [0, 0, 0], min: -Math.PI, max: Math.PI, step: 0.1 },
    child1Position: { value: [2, 0, 0], min: -3, max: 3, step: 0.1 },
    child2Rotation: { value: [0, 0, 0], min: -Math.PI, max: Math.PI, step: 0.1 },
    child2Position: { value: [-2, 0, 0], min: -3, max: 3, step: 0.1 }
  })

  // Controles para los nietos (nivel 3)
  const grandchildControls = useControls('Nietos (Nivel 3)', {
    // Nieto 1 (del Hijo 1)
    grandchild1Rotation: { value: [0, 0, 0], min: -Math.PI, max: Math.PI, step: 0.1 },
    grandchild1Position: { value: [0.8, 0, 0], min: -2, max: 2, step: 0.1 },
    grandchild1Scale: { value: 1, min: 0.3, max: 2, step: 0.1 },
    // Nieto 2 (del Hijo 2)
    grandchild2Rotation: { value: [0, 0, 0], min: -Math.PI, max: Math.PI, step: 0.1 },
    grandchild2Position: { value: [-0.8, 0, 0], min: -2, max: 2, step: 0.1 },
    grandchild2Scale: { value: 1, min: 0.3, max: 2, step: 0.1 }
  })

  return (
    <>
      {/* Nivel 1: Grupo Padre */}
      <group 
        rotation={parentControls.rotation}
        position={parentControls.position}
        scale={parentControls.scale}
      >
        {/* Etiqueta del padre */}
        <Text
          position={[0, 3, 0]}
          fontSize={0.5}
          color="white"
          anchorX="center"
          anchorY="middle"
        >
          PADRE (Cubo Rojo)
        </Text>

        {/* Cubo padre */}
        <mesh position={[0, 0, 0]}>
          <boxGeometry args={[1, 1, 1]} />
          <meshStandardMaterial color="red" />
        </mesh>

        {/* Nivel 2: Hijos */}
        {/* Hijo 1 - Esfera */}
        <group 
          rotation={childControls.child1Rotation}
          position={childControls.child1Position}
        >
          <Text
            position={[0, 1.5, 0]}
            fontSize={0.3}
            color="lightblue"
            anchorX="center"
            anchorY="middle"
          >
            HIJO 1
          </Text>
          
          <mesh>
            <sphereGeometry args={[0.5, 16, 16]} />
            <meshStandardMaterial color="blue" />
          </mesh>

          {/* Nivel 3: Nietos del Hijo 1 */}
          <group 
            rotation={grandchildControls.grandchild1Rotation}
            position={grandchildControls.grandchild1Position}
            scale={grandchildControls.grandchild1Scale}
          >
            <mesh>
              <cylinderGeometry args={[0.2, 0.2, 0.8]} />
              <meshStandardMaterial color="lightblue" />
            </mesh>
            <Text
              position={[0, 0.8, 0]}
              fontSize={0.2}
              color="white"
              anchorX="center"
              anchorY="middle"
            >
              NIETO 1
            </Text>
          </group>
        </group>

        {/* Hijo 2 - Cilindro */}
        <group 
          rotation={childControls.child2Rotation}
          position={childControls.child2Position}
        >
          <Text
            position={[0, 1.5, 0]}
            fontSize={0.3}
            color="lightgreen"
            anchorX="center"
            anchorY="middle"
          >
            HIJO 2
          </Text>
          
          <mesh>
            <cylinderGeometry args={[0.4, 0.4, 1]} />
            <meshStandardMaterial color="green" />
          </mesh>

          {/* Nivel 3: Nietos del Hijo 2 */}
          <group 
            rotation={grandchildControls.grandchild2Rotation}
            position={grandchildControls.grandchild2Position}
            scale={grandchildControls.grandchild2Scale}
          >
            <mesh>
              <coneGeometry args={[0.25, 0.6]} />
              <meshStandardMaterial color="lightgreen" />
            </mesh>
            <Text
              position={[0, 0.6, 0]}
              fontSize={0.2}
              color="white"
              anchorX="center"
              anchorY="middle"
            >
              NIETO 2
            </Text>
          </group>
        </group>
      </group>

      {/* Ejes de referencia */}
      <axesHelper args={[5]} />
    </>
  )
}

function App() {
  return (
    <div style={{ width: '100vw', height: '100vh', position: 'relative' }}>
      {/* Canvas de Three.js */}
      <Canvas
        camera={{ position: [5, 5, 5], fov: 60 }}
        style={{ background: '#1a1a1a' }}
      >
        {/* Iluminación */}
        <ambientLight intensity={0.4} />
        <directionalLight position={[10, 10, 5]} intensity={1} />
        <pointLight position={[-10, -10, -5]} intensity={0.5} />

        {/* Controles de órbita */}
        <OrbitControls 
          enablePan={true}
          enableZoom={true}
          enableRotate={true}
        />

        {/* Renderizar escena abstracta */}
        <AbstractHierarchy />
      </Canvas>

      {/* Panel de información */}
      <div style={{
        position: 'absolute',
        top: '20px',
        left: '20px',
        background: 'rgba(0, 0, 0, 0.7)',
        color: 'white',
        padding: '20px',
        borderRadius: '10px',
        fontFamily: 'Arial, sans-serif',
        maxWidth: '300px'
      }}>
        <h2 style={{ margin: '0 0 10px 0', color: '#4CAF50' }}>
          Ejercicio 1: Jerarquías y Transformaciones
        </h2>
        <p style={{ margin: '0 0 10px 0', fontSize: '14px' }}>
          <strong>Objetivo:</strong> Comprender relaciones padre-hijo en escenas 3D
        </p>
        <p style={{ margin: '0 0 10px 0', fontSize: '14px' }}>
          <strong>Escena:</strong> Estructura Abstracta
        </p>
        <div style={{ fontSize: '12px', marginTop: '10px' }}>
          <p><strong>Nivel 1 (Padre):</strong> Controla toda la jerarquía</p>
          <p><strong>Nivel 2 (Hijos):</strong> Se transforman respecto al padre</p>
          <p><strong>Nivel 3 (Nietos):</strong> Heredan transformaciones de ambos niveles</p>
        </div>
      </div>

      {/* Instrucciones */}
      <div style={{
        position: 'absolute',
        bottom: '20px',
        left: '20px',
        background: 'rgba(0, 0, 0, 0.7)',
        color: 'white',
        padding: '15px',
        borderRadius: '10px',
        fontFamily: 'Arial, sans-serif',
        maxWidth: '400px'
      }}>
        <h3 style={{ margin: '0 0 10px 0', color: '#FF9800' }}>Instrucciones:</h3>
        <ul style={{ margin: '0', paddingLeft: '20px', fontSize: '12px' }}>
          <li>Usa los controles de Leva (panel derecho) para transformar objetos</li>
          <li><strong>Padre:</strong> Controla toda la jerarquía (Padre + Hijos + Nietos)</li>
          <li><strong>Hijos:</strong> Controla solo su rama (Hijo + Nieto)</li>
          <li><strong>Nietos:</strong> Controla solo el objeto individual</li>
          <li>Observa cómo las transformaciones se acumulan en la jerarquía</li>
          <li>Mueve la cámara con el mouse (arrastrar, rueda, clic derecho)</li>
        </ul>
      </div>
    </div>
  )
}

export default App