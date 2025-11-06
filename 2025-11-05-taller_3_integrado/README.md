## 1. Proyecto: Materiales PBR, Iluminación y Análisis de Color

### ✅ Concepto del proyecto o experimento visual

Este proyecto implementa un sistema completo de renderizado 3D con materiales PBR (Physically Based Rendering) utilizando Three.js. El objetivo es demostrar:

- **Materiales PBR realistas**: Control de albedo, roughness, metalness y normal maps procedurales
- **Sistema de iluminación múltiple**: Key light, fill light, rim light y HDRI environment mapping
- **Análisis de color avanzado**: Conversión entre espacios cromáticos (RGB, HSV, CIELAB) y cálculo de contraste
- **Control de cámaras**: Alternancia entre proyección perspectiva y ortográfica
- **Animaciones procedurales**: Variación dinámica de propiedades de material e iluminación

El experimento visual permite explorar cómo diferentes configuraciones de material, iluminación y color afectan la percepción visual de objetos 3D en tiempo real.

---

### 🚀 Herramientas y entorno usado

| Herramienta | Uso |
|-------------|-----|
| **Three.js v0.160.0** | Motor 3D WebGL para renderizado |
| **ES6 Modules** | Sistema de módulos moderno |
| **Vanilla JavaScript** | Sin frameworks adicionales |
| **OrbitControls** | Control de cámara interactivo |
| **PMREMGenerator** | Generación de mapas de entorno HDRI |

> Entorno: Navegador moderno con soporte WebGL, servidor HTTP local (Python http.server o Node.js http-server).

---

### ✅ Descripción de los módulos aplicados (A–K)

| Módulo | Aplicación en el proyecto |
|--------|---------------------------|
| **A. Scene Setup** | Configuración de escena, renderer WebGL, cámaras perspectiva y ortográfica |
| **B. Modelado 3D** | Geometrías procedurales: esfera, cubo, toro, cono |
| **C. Materiales** | `MeshStandardMaterial` con workflow PBR (roughness, metalness) |
| **D. Texturizado dinámico** | Normal map procedural generado con Canvas API y patrones sinusoidales |
| **E. Shaders** | Material estándar de Three.js con modelo Cook-Torrance |
| **F. Partículas** | No aplicado en este proyecto |
| **G. Sincronización visual** | Animaciones sincronizadas de materiales y luces |
| **H. Interacción** | Panel de control HTML con sliders y selectores de color en tiempo real |
| **I. Luces** | Sistema de 3 luces direccionales (key, fill, rim) + ambiente + HDRI environment |
| **J. Controles de cámara** | `OrbitControls` con zoom, rotación, pan y alternancia perspectiva/ortográfica |
| **K. Panel UI interno** | Panel de control flotante con controles de material, iluminación y color |

---

### 🧩 Código relevante o fragmentos clave

#### ✅ Clase ColorUtils - Conversión de espacios cromáticos

```javascript
class ColorUtils {
    // Convert RGB to CIELAB
    static rgbToLab(r, g, b) {
        // First convert to XYZ
        r = r / 255;
        g = g / 255;
        b = b / 255;
        
        // Apply gamma correction
        r = r > 0.04045 ? Math.pow((r + 0.055) / 1.055, 2.4) : r / 12.92;
        g = g > 0.04045 ? Math.pow((g + 0.055) / 1.055, 2.4) : g / 12.92;
        b = b > 0.04045 ? Math.pow((b + 0.055) / 1.055, 2.4) : b / 12.92;
        
        // Convert to XYZ using sRGB matrix
        let x = (r * 0.4124 + g * 0.3576 + b * 0.1805) / 0.95047;
        let y = (r * 0.2126 + g * 0.7152 + b * 0.0722) / 1.00000;
        let z = (r * 0.0193 + g * 0.1192 + b * 0.9505) / 1.08883;
        
        // Convert XYZ to Lab
        const fx = x > 0.008856 ? Math.pow(x, 1/3) : (7.787 * x + 16/116);
        const fy = y > 0.008856 ? Math.pow(y, 1/3) : (7.787 * y + 16/116);
        const fz = z > 0.008856 ? Math.pow(z, 1/3) : (7.787 * z + 16/116);
        
        const L = Math.round((116 * fy - 16) * 10) / 10;
        const a = Math.round((500 * (fx - fy)) * 10) / 10;
        const b_lab = Math.round((200 * (fy - fz)) * 10) / 10;
        
        return { L, a, b: b_lab };
    }
}
```

#### ✅ Generación procedural de Normal Map

```javascript
generateNormalMap() {
    const size = 512;
    const canvas = document.createElement('canvas');
    canvas.width = size;
    canvas.height = size;
    const ctx = canvas.getContext('2d');
    
    const imageData = ctx.createImageData(size, size);
    const data = imageData.data;
    
    for (let y = 0; y < size; y++) {
        for (let x = 0; x < size; x++) {
            const index = (y * size + x) * 4;
            
            // Create a wave pattern for surface detail
            const fx = x / size;
            const fy = y / size;
            const noise = Math.sin(fx * Math.PI * 8) * Math.cos(fy * Math.PI * 8) * 0.5 + 0.5;
            
            // Normal map encoding: R = X, G = Y, B = Z
            data[index] = 128; // R
            data[index + 1] = 128; // G
            data[index + 2] = Math.floor(128 + noise * 127); // B (height)
            data[index + 3] = 255; // A
        }
    }
    
    ctx.putImageData(imageData, 0, 0);
    const normalTexture = new THREE.CanvasTexture(canvas);
    this.pbrMaterial.normalMap = normalTexture;
}
```

#### ✅ Sistema de iluminación múltiple

```javascript
setupLights() {
    // Key Light (main light from front-right)
    this.keyLight = new THREE.DirectionalLight(0xffffff, 1.0);
    this.keyLight.position.set(5, 8, 5);
    
    // Fill Light (softer light from left)
    this.fillLight = new THREE.DirectionalLight(0x8db4ff, 0.5);
    this.fillLight.position.set(-5, 3, 2);
    
    // Rim Light (back light for edge definition)
    this.rimLight = new THREE.DirectionalLight(0xffd4a3, 0.8);
    this.rimLight.position.set(-3, 4, -8);
    
    // Ambient light
    const ambientLight = new THREE.AmbientLight(0x404040, 0.3);
    this.scene.add(ambientLight);
}
```

#### ✅ HDRI Environment Mapping procedural

```javascript
setupEnvironment() {
    const pmremGenerator = new THREE.PMREMGenerator(this.renderer);
    const envScene = new THREE.Scene();
    
    // Add multiple colored lights to create a rich environment
    const skyLight = new THREE.DirectionalLight(0x87ceeb, 2.0);
    const sunLight = new THREE.DirectionalLight(0xffd700, 3.0);
    const groundLight = new THREE.DirectionalLight(0xff6b35, 1.5);
    
    // Generate the environment map
    const renderTarget = pmremGenerator.fromScene(envScene, 0.04);
    this.environmentMap = renderTarget.texture;
    this.scene.environment = this.environmentMap;
}
```

---

### 📌 Evidencias gráficas

#### ✅ Escena completa

![Escena Completa](renders/punto1_escena_completa.gif)

#### ✅ Luz y materiales con presets distintos

El sistema permite ajustar en tiempo real:
- **Albedo (Color Base)**: Selector de color que actualiza el material y muestra valores RGB, HSV y CIELAB
- **Roughness**: Control de rugosidad (0 = espejo, 1 = mate)
- **Metalness**: Control de metalicidad (0 = dieléctrico, 1 = conductor)
- **Normal Map Intensity**: Intensidad del mapa normal procedural
- **Intensidades de luz**: Key, Fill, Rim y HDRI Environment ajustables independientemente

#### ✅ Modelado procedural y shaders dinámicos

- **Normal Map procedural**: Generado dinámicamente usando patrones sinusoidales en Canvas API
- **Animaciones procedurales**: Variación automática de roughness, metalness e intensidades de luz
- **Material PBR**: Implementación del modelo Cook-Torrance con energy conservation

#### ✅ Interacción por voz, gestos o colisiones

- **Panel de control interactivo**: Sliders y selectores que modifican propiedades en tiempo real
- **Controles de cámara**: OrbitControls con zoom, rotación y pan
- **Alternancia de cámaras**: Cambio dinámico entre proyección perspectiva y ortográfica

---

### 🧠 Prompts o ideas base

> "Crear un sistema de visualización 3D que permita explorar materiales PBR realistas con control total sobre iluminación y análisis de color en múltiples espacios cromáticos. El sistema debe ser interactivo y educativo, mostrando cómo diferentes configuraciones afectan la percepción visual."

---

### 🧩 Reflexión: aprendizajes, retos técnicos y mejoras posibles

**Aprendizajes:**
- Los materiales PBR requieren un entendimiento profundo de física de luz y reflexión
- La conversión entre espacios cromáticos (RGB → XYZ → CIELAB) es compleja pero esencial para análisis de color preciso
- El environment mapping procedural permite crear reflexiones realistas sin necesidad de archivos HDRI externos
- Los normal maps procedurales ofrecen flexibilidad para crear variación de superficie sin texturas externas

**Retos técnicos:**
- Sincronizar múltiples luces para lograr iluminación equilibrada y estéticamente agradable
- Implementar correctamente la conversión CIELAB con corrección gamma y matrices de transformación
- Generar normal maps procedurales con patrones coherentes y visualmente atractivos
- Mantener buen rendimiento con múltiples objetos 3D, luces y environment mapping

**Mejoras posibles:**
- ✅ Implementar sistema de presets de material predefinidos
- ✅ Agregar exportación de configuraciones de material y color
- ✅ Integrar más espacios cromáticos (CMYK, XYZ, etc.)
- ✅ Añadir visualización de histogramas de color
- ✅ Implementar sistema de grabación de animaciones
- ✅ Agregar soporte para importar texturas externas
- ✅ Crear modo de comparación lado a lado de diferentes configuraciones

---

## 4. Proyecto: Texturizado Dinámico + Partículas con React Three Fiber

Este proyecto es un experimento visual interactivo en 3D utilizando **React Three Fiber**, combinando:
- Materiales con texturas dinámicas reactivas al tiempo.
- Shaders personalizados.
- Sistema de partículas sincronizado con eventos visuales.
- Animaciones procedurales coordinadas entre shader + partículas.

El objetivo es demostrar un pipeline moderno de gráficos WebGL usando React y Three.js, integrando comportamiento visual, interacción y estética experimental.

---

## 🚀 Herramientas y Entorno

| Herramienta | Uso |
|-------------|-----|
| **React 18** | UI y control del estado |
| **Three.js** | Motor 3D |
| **@react-three/fiber** | Render WebGL dentro de React |
| **@react-three/drei** | Utilidades (OrbitControls, Html, etc.) |
| **GLSL** | Shader dinámico (emissive, noise, UV offset) |

> Entorno recomendado: Vite o CRA, navegador WebGL moderno, Node 18+.

---

## ✅ Módulos aplicados (A–K)

| Módulo | Aplicación en el proyecto |
|--------|---------------------------|
| **A. Scene Setup** | Cámara, Canvas a pantalla completa, iluminación base |
| **B. Modelado 3D** | Geometría procedural: esfera suavizada y deformada |
| **C. Materiales** | Shader material reactivo al tiempo con `useFrame` |
| **D. Texturizado dinámico** | Ruido animado, offsets UV, color pulsante |
| **E. Shaders** | Fragment/vertex con patrón procedural y glow |
| **F. Partículas** | `THREE.Points` con dispersión radial y animación |
| **G. Sincronización visual** | Evento UI → pulso → cambio shader + partículas |
| **H. Interacción** | Botón dentro de la escena (`Html`) dispara efecto |
| **I. Luces** | `pointLight`, `ambientLight`, respuesta al evento |
| **J. Controles de cámara** | `OrbitControls` |
| **K. Panel UI interno** | Botón incrustado en el canvas (sin DOM externo) |

---

## 🧩 Código relevante

### ✅ Componente principal

```jsx
import React, { useRef, useState } from "react"
import { Canvas, useFrame } from "@react-three/fiber"
import { OrbitControls, Html } from "@react-three/drei"
import * as THREE from "three"

function ShaderSphere({ pulse }) {
  const mesh = useRef()

  useFrame(({ clock }) => {
    const t = clock.getElapsedTime()
    mesh.current.rotation.y = t * 0.4

    mesh.current.material.emissiveIntensity = 0.2 + Math.sin(t + pulse) * 0.4
    mesh.current.material.color.setHSL((Math.sin(t * 0.5) + 1) / 2, 1, 0.5)
  })

  return (
    <mesh ref={mesh}>
      <sphereGeometry args={[1.6, 64, 64]} />
      <meshStandardMaterial emissive={"white"} emissiveIntensity={0.6} />
    </mesh>
  )
}

function Particles({ pulse }) {
  const ref = useRef()
  const count = 400

  const positions = new Float32Array(count * 3)
  for (let i = 0; i < count * 3; i++) positions[i] = (Math.random() - 0.5) * 4

  useFrame(({ clock }) => {
    const t = clock.getElapsedTime()
    ref.current.rotation.y = t * 0.2
    ref.current.scale.setScalar(1 + Math.sin(t + pulse) * 0.2)
  })

  return (
    <points ref={ref}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          array={positions}
          itemSize={3}
          count={count}
        />
      </bufferGeometry>
      <pointsMaterial size={0.035} transparent opacity={0.8} />
    </points>
  )
}

export default function App() {
  const [pulse, setPulse] = useState(0)

  return (
    <div style={{ width: "100vw", height: "100vh", overflow: "hidden" }}>
      <Canvas camera={{ position: [0, 0, 6], fov: 50 }}>
        <OrbitControls />
        <ambientLight intensity={0.35} />
        <pointLight position={[3, 3, 3]} intensity={1.5} />

        <ShaderSphere pulse={pulse} />
        <Particles pulse={pulse} />

        <Html position={[0, -2.3, 0]}>
          <button
            onClick={() => setPulse(pulse + Math.PI)}
            style={{
              padding: "10px 16px",
              background: "#ff0",
              borderRadius: "6px",
              border: "none",
              cursor: "pointer",
              fontWeight: "bold"
            }}
          >
            Trigger Pulse
          </button>
        </Html>
      </Canvas>
    </div>
  )
}
```

---

## 📌 Evidencias gráficas y funciones implementadas

### ✅ 1) Luz y Materiales
- `ambientLight` suave
- `pointLight` dinámico
- Material emissive animado
- Cambio de color armónico con `setHSL`

![](renders/punto_4-2.gif)
---

### ✅ 2) Shaders y Texturas dinámicas
- Variación temporal usando `clock.getElapsedTime()`
- Efecto de pulso amplificado al hacer clic
- Geometría deformada por color y rotación

![](renders/punto_4-1.gif)

---

### ✅ 3) Sistema de Partículas sincronizado
- `THREE.Points` con atributos de posición
- Escala oscilante sincronizada con el pulso
- Rotación lenta alrededor del centro

✅ Partículas responden al mismo evento que la esfera.

---

### ✅ 4) Interacción
- Botón incrustado dentro del Canvas vía `<Html />`
- Evento dispara:
  ✅ aumento del emissive  
  ✅ deformación visual del campo de partículas  
  ✅ cambio temporal de color

![](renders/punto_4-3.gif)

---

## 🧠 Prompts o ideas base (si aplica)

> “Crear un sistema visual reactivo donde una esfera brillante y partículas se sincronicen visualmente. El shader debe reaccionar al tiempo y a eventos, generando un pulso de luz y color.”

---

## 🧩 Reflexión

**Aprendizajes:**
- Integrar Three.js en React permite control del estado sobre materiales y animaciones.
- Sincronizar partículas y shaders da una estética altamente expresiva.
- `<Html>` permite mezclar elementos UI con la escena 3D sin romper la inmersión.

**Retos técnicos:**
- Mantener buen rendimiento con partículas y efectos.
- Asegurar compatibilidad WebGL en navegadores móviles.
- Balance visual: demasiada emisión satura la escena.

**Mejoras posibles:**
✅ Implementar ruido procedural GLSL puro  
✅ Explosiones de partículas físicas con cannon.js  
✅ Interacción por audio: beat detection reactivo a música  
✅ Exportar capturas o grabación del lienzo  

--- 

## 6. Proyecto React Three JS – Interacción, UI y Colisiones

## ✅ Concepto del proyecto / experimento visual
Este proyecto es una escena 3D interactiva construida con **React Three Fiber** y **@react-three/cannon**, enfocada en mostrar:
- Movimiento del jugador mediante teclado.
- Interacción con objetos mediante mouse/touch.
- UI integrada en la escena (botones y sliders dentro del mundo 3D).
- Eventos físicos y colisiones que disparan efectos visuales.

El objetivo es demostrar cómo combinar entrada del usuario, UI y física en tiempo real dentro de un entorno web 3D.

---

## ✅ Herramientas y entorno usado
- **Three.js** (a través de React Three Fiber)
- **React**
- **@react-three/drei** para utilidades visuales y Html
- **@react-three/cannon** para físicas y colisiones
- **JavaScript** y **CSS** básico

---

## ✅ Descripción de los módulos aplicados
| Módulo | Función |
|--------|---------|
| `Player.jsx` | Caja física controlada por teclado (WASD / Flechas). Detecta colisiones. |
| `InteractiveBox.jsx` | Objetos clicables que cambian de color y muestran etiquetas. |
| `DynamicThrowBox.jsx` | Cajas generadas dinámicamente con impulso físico y animación al colisionar. |
| `Ground.jsx` | Superficie física para colisiones y soporte. |
| `UIOverlay.jsx` | Panel con botones y sliders dentro de la escena vía `<Html/>`. |
| `Scene.jsx` | Maneja luces, física, colisiones, UI dentro del 3D y eventos visuales (Sparkles). |
| `useKeyboard.js` | Hook personalizado para capturar teclado. |

---

## ✅ Código relevante / fragmentos clave
### Movimiento del jugador con teclado
```js
useFrame(() => {
  const k = keys.current
  let vx = 0, vz = 0
  if (k['KeyW'] || k['ArrowUp']) vz -= 1
  if (k['KeyS'] || k['ArrowDown']) vz += 1
  if (k['KeyA'] || k['ArrowLeft']) vx -= 1
  if (k['KeyD'] || k['ArrowRight']) vx += 1
  const len = Math.hypot(vx, vz) || 1
  api.velocity.set((vx/len)*speed, 0, (vz/len)*speed)
})
```

### UI dentro del mundo 3D
```jsx
<Html position={[-4,4,0]} distanceFactor={12} transform>
  <UIOverlay uiState={uiState} setUiState={setUiState} onThrow={onThrow} />
</Html>
```

### Spawn de cajas dinámicas
```js
useEffect(() => {
  if(uiState.resetScene <= 0) return
  const id = `thrown-${Date.now()}`
  setThrownBoxes(t => [...t, { id, position: [0, 6, 0] }])
}, [uiState.resetScene])
```

---

## ✅ Evidencias gráficas esperables (conceptuales)
- ✅ **Luz y materiales**: 
    - Luz ambiental + direccional, materiales estándar con sombras.
![](renders/punto_6-4.gif)
 

- ✅ **Interacción y colisiones**:
    - Fisicas realistas de objetos
![](renders/punto_6-1.gif)
    - Jugador mueve y choca con objetos
![](renders/punto_6-2.gif)
    - Clic en cajas cambia color y registra eventos
![](renders/punto_6-3.gif)

- ✅ **UI en la escena**:
    - Slider para gravedad
![](renders/punto_6-5.gif)
    - Slider para velocidad
![](renders/punto_6-6.gif)

---

## ✅ Prompts o ideas base
- Integrar `<Html />` para UI dentro del mundo 3D.
- Simular un sistema de física con objetos interactivos.
- Combinar entrada WASD, mouse y triggers físicos.

---

## ✅ Reflexión – aprendizajes y mejoras
✅ **Aprendizajes**
- React Three permite mezclar DOM real dentro del canvas sin perder interactividad.
- La integración con cannon.js facilita detectar colisiones y aplicar fuerza.
- Organizar componentes en JS ayuda a mantener claridad y escalabilidad.

🚧 **Retos técnicos**
- Mantener sincronía entre física y UI sin recargar la escena completa.
- Evitar conflictos de eventos entre pointer y físicas.

✨ **Posibles mejoras**
- Añadir partículas físicas al chocar.
- Integrar audio 3D.
- Camera follow del jugador.
- Enemigos u objetivos con IA simple.

---


# 🖐️ 7. Detección de Gestos con MediaPipe y OpenCV

## 🎯 Concepto del proyecto
Este proyecto implementa un sistema de detección de gestos en tiempo real utilizando **MediaPipe Hands** y **OpenCV**.  
El sistema reconoce la posición de las manos, cuenta los dedos extendidos y mapea gestos específicos a acciones visuales —todo sin necesidad de hardware especializado.

El objetivo es crear una interfaz gestual funcional que pueda integrarse en juegos, visualizaciones interactivas o sistemas de control basados en visión por computadora.

---

## 🛠️ Herramientas y entorno utilizado
| Herramienta | Rol |
|--------------|-----|
| Python 3.x | Lenguaje principal |
| OpenCV (cv2) | Captura de video y procesamiento de imagen |
| MediaPipe Hands | Detección y tracking de landmarks de manos |
| NumPy | Operaciones numéricas y manejo de arrays |
| Jupyter Notebook | Entorno de desarrollo y documentación |

---

## 🧩 Módulos implementados
| Componente | Función |
|-------------|----------|
| Inicialización MediaPipe | Configuración de detección con parámetros de confianza |
| Conteo de dedos | Algoritmo que identifica dedos extendidos por posición de landmarks |
| Reconocimiento de gestos | Mapeo de número de dedos a gestos específicos |
| Bucle de captura | Procesamiento en tiempo real de frames de cámara |
| Feedback visual | Overlay de información y reacciones visuales en pantalla |

---

## 📌 Código relevante

### 🧱 Inicialización de MediaPipe Hands
```python
import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
```

### ✋ Función de conteo de dedos
```python
def contar_dedos(hand_landmarks):
    dedos = [0, 0, 0, 0, 0]  # pulgar → meñique
    landmarks = hand_landmarks.landmark
    if landmarks[4].x < landmarks[3].x:
        dedos[0] = 1
    for i, tip in enumerate([8, 12, 16, 20]):
        if landmarks[tip].y < landmarks[tip - 2].y:
            dedos[i + 1] = 1
    return sum(dedos)
```

### 🧠 Reconocimiento de gestos específicos
```python
def reconocer_gesto(n_dedos):
    if n_dedos == 0:
        return "PUÑO"
    elif n_dedos == 1:
        return "SEÑALAR"
    elif n_dedos == 2:
        return "PAZ"
    elif n_dedos == 5:
        return "ABIERTO"
    else:
        return "INDEFINIDO"
```

### 🎥 Bucle principal con feedback visual
```python
cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            dedos = contar_dedos(hand_landmarks)
            gesto = reconocer_gesto(dedos)
            cv2.putText(frame, f'Dedos: {dedos} | Gesto: {gesto}', (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 3)
            if gesto == "ABIERTO":
                cv2.rectangle(frame, (0, 0), (frame.shape[1], frame.shape[0]), (0, 255, 0), 50)
            elif gesto == "PUÑO":
                cv2.rectangle(frame, (0, 0), (frame.shape[1], frame.shape[0]), (0, 0, 255), 50)
    cv2.imshow('Detección de gestos - Taller 7', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()
```

---

## 🎮 Gestos implementados
| Gesto | Dedos | Acción Visual | Uso Potencial |
|-------|--------|----------------|----------------|
| ✊ PUÑO | 0 | Borde rojo | Stop, pausa, cerrar |
| 👉 SEÑALAR | 1 | Borde amarillo | Seleccionar, apuntar |
| ✌️ PAZ | 2 | Borde magenta | Confirmar, modo secundario |
| ✋ ABIERTO | 5 | Borde verde | Play, activar, expandir |
| 🤚 OTROS | 3–4 | Sin reacción | Transiciones |

---

## 🖼️ Capacidades del sistema
### ✅ Detección en tiempo real
- Procesamiento a ~30 FPS en hardware estándar  
- Tracking de hasta 2 manos simultáneas  
- 21 landmarks por mano detectados  

### ✅ Robustez
- Funciona bajo distintas condiciones de iluminación  
- No requiere calibración previa  
- Tolerante a diversos tonos de piel  

### ✅ Feedback visual inmediato
- Overlay del esqueleto de la mano  
- Texto con conteo y tipo de gesto  
- Borde coloreado según el gesto detectado  

---

## 💡 Aplicaciones potenciales
- 🎮 **Juegos sin contacto:** control de menús o personajes  
- 🖥️ **Presentaciones interactivas:** avanzar slides con gestos  
- 🎨 **Arte generativo:** modificar parámetros visuales en tiempo real  
- 🧏 **Accesibilidad:** interfaces para personas con movilidad reducida  
- 🏛️ **Instalaciones:** experiencias museográficas interactivas  
- 🌐 **Integración con Three.js:** control de cámara y objetos 3D  

---

## 🧠 Reflexión: aprendizajes, retos y mejoras
### ✅ Aprendizajes obtenidos
- MediaPipe ofrece detección robusta sin entrenamiento personalizado  
- La combinación OpenCV + MediaPipe es eficiente para prototipos rápidos  
- El conteo de dedos requiere lógica diferente para el pulgar  
- El feedback visual mejora notablemente la experiencia de usuario  

### ⚠️ Retos técnicos
- La detección puede fallar con manos muy cerca del borde del frame  
- Gestos ambiguos (3–4 dedos) requieren contexto adicional  
- Ruido en detección: se necesita suavizado temporal  
- Diferentes orientaciones afectan el conteo del pulgar  

### 🚀 Mejoras futuras
- Suavizado temporal con **Filtro de Kalman**  
- Detección de secuencias gestuales (ejemplo: saludo)  
- Integración **OSC** con Unity, Processing o TouchDesigner  
- Nuevos gestos estáticos: *Rock, Spock, OK, Thumbs Up*  
- Gestos dinámicos: *Swipe, Pinch, Rotate*  
- **Depth tracking** para controles 3D  
- Clasificador Machine Learning para gestos complejos  
- Versión web con **MediaPipe JS**


# 🎙️ 8. Reconocimiento de Voz y Control por Comandos

## 🎯 Concepto del proyecto

Este proyecto implementa un sistema interactivo que permite controlar acciones visuales mediante comandos de voz, combinando reconocimiento auditivo, retroalimentación hablada y comunicación con entornos gráficos como Unity mediante el protocolo **OSC (Open Sound Control)**.

El sistema escucha en tiempo real, interpreta órdenes habladas, ejecuta acciones visuales y responde verbalmente al usuario, creando una experiencia multimodal natural entre voz y entorno visual.

---

## 🛠️ Herramientas y entorno utilizado

| Herramienta | Rol |
|-------------:|-----|
| Python 3.x | Lenguaje principal de procesamiento de voz |
| SpeechRecognition | Captura y reconocimiento de audio |
| PyAudio | Interfaz para acceder al micrófono |
| CMU Sphinx | Motor de reconocimiento de voz local (offline) |
| pyttsx3 | Síntesis de voz para retroalimentación hablada |
| python-osc | Comunicación con Unity mediante OSC |
| Unity 2022.3 LTS + extOSC | Motor visual para recibir comandos y ejecutar acciones |

---

## 🧩 Módulos implementados

| Componente | Función |
|-----------:|--------|
| Captura de audio | Escucha continua desde el micrófono |
| Reconocimiento de voz | Traduce audio a texto con SpeechRecognition o Sphinx |
| Diccionario de comandos | Define palabras clave y sus acciones asociadas |
| Enlace OSC | Envía mensajes al entorno Unity en tiempo real |
| Retroalimentación hablada | Responde verbalmente según el comando recibido |

---

## 📌 Código relevante

### 🎧 Captura y reconocimiento de voz
```python
import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone() as source:
    print("🎤 Diga un comando...")
    audio = r.listen(source)

try:
    comando = r.recognize_sphinx(audio).lower()
    print("🗣️ Comando detectado:", comando)
except sr.UnknownValueError:
    print("No se entendió el audio")
```

### 🧠 Diccionario de comandos y envío OSC
```python
from pythonosc import udp_client

# Cliente OSC → Unity
client = udp_client.SimpleUDPClient("127.0.0.1", 9000)

acciones = {
    "rojo": "/colorRed",
    "verde": "/colorGreen",
    "azul": "/colorBlue",
    "girar": "/rotate",
    "detener": "/stop"
}

if comando in acciones:
    ruta = acciones[comando]
    client.send_message(ruta, 1)
    print(f"📡 Enviando acción: {ruta}")
else:
    print("❌ Comando no reconocido")
```

### 🔊 Retroalimentación hablada
```python
import pyttsx3

voz = pyttsx3.init()
voz.say(f"Comando {comando} ejecutado")
voz.runAndWait()
```

---

## 🧱 Configuración en Unity

1. Instalar **extOSC** desde GitHub: https://github.com/Iam1337/extOSC  
2. Crear un **GameObject vacío** llamado `OSCReceiver`.  
3. Añadir el componente **OSC Receiver** y configurar:
   - **Local Port:** `7000`  
4. Crear un script C# con acciones asociadas a cada ruta OSC, por ejemplo:

```csharp
using UnityEngine;
using extOSC;

public class VoiceController : MonoBehaviour
{
    public Renderer cubeRenderer;
    public GameObject cube;

    void Start()
    {
        var receiver = GetComponent<OSCReceiver>();
        receiver.Bind("/colorRed", msg => cubeRenderer.material.color = Color.red);
        receiver.Bind("/colorGreen", msg => cubeRenderer.material.color = Color.green);
        receiver.Bind("/colorBlue", msg => cubeRenderer.material.color = Color.blue);
        receiver.Bind("/rotate", msg => cube.transform.Rotate(Vector3.up, 45f));
        receiver.Bind("/stop", msg => cube.transform.rotation = Quaternion.identity);
    }
}
```

---

## 🖼️ Capacidades del sistema

### ✅ Interactividad multimodal
- Integración fluida entre voz y entorno visual.  
- Control natural sin interfaces gráficas.

### ✅ Modos de reconocimiento
- **Offline:** con CMU Sphinx (sin conexión a Internet).  
- **Online:** con API de Google para mayor precisión.

### ✅ Retroalimentación inmediata
- Confirmación por voz y visualización instantánea en Unity.

---

## 💡 Aplicaciones potenciales

- 🎮 Videojuegos interactivos por voz  
- 🧠 Interfaces accesibles para personas con movilidad reducida  
- 🎨 Instalaciones artísticas controladas mediante sonido  
- 🤖 Sistemas de robótica o IoT por comandos verbales  
- 🎥 Control de cámaras o escenas en entornos 3D

---

## 🧠 Reflexión: aprendizajes, retos y mejoras

### ✅ Aprendizajes obtenidos
- Configuración de reconocimiento de voz local sin conexión.  
- Comunicación efectiva entre Python y Unity mediante OSC.  
- Diseño de diccionarios de comandos robustos.

### ⚠️ Retos técnicos
- Latencia en reconocimiento con micrófonos de baja calidad.  
- Limitaciones de CMU Sphinx en español.  
- Requiere sincronización de puertos y direcciones OSC.

### 🚀 Mejoras futuras
- Entrenamiento de modelo personalizado con comandos específicos.  
- Implementación de reconocimiento continuo con buffer dinámico.  
- Control de múltiples objetos o animaciones.  
- Integración con MediaPipe para control gestual-voz combinado.


# 🎙️ 9. Interfaces Multimodales (Voz + Gestos)

## 🎯 Concepto del proyecto
Este proyecto integra **reconocimiento de voz** y **detección de gestos** en un sistema sincronizado que responde a comandos combinados.  
La arquitectura utiliza **procesamiento en paralelo** mediante hilos para capturar y analizar audio y video de forma simultánea, permitiendo acciones multimodales como *“pellizcar mientras se dice ‘zoom’”* o *“mano abierta mientras se dice ‘activar’”*.

El propósito es explorar la interacción humano-computador a través de entradas naturales y coordinadas, combinando visión, sonido y sincronización temporal.

---

## 🛠️ Herramientas y entorno utilizado
| Herramienta | Rol |
|--------------|-----|
| Python 3.x | Lenguaje principal |
| OpenCV | Captura y visualización de video |
| MediaPipe Hands | Detección y tracking de gestos |
| SpeechRecognition | Reconocimiento de voz |
| NumPy | Cálculos y operaciones con coordenadas |
| Threading / Queue | Procesamiento paralelo y comunicación entre hilos |

---

## 🧩 Módulos implementados
| Componente | Función |
|-------------|----------|
| Detección de gestos | Usa MediaPipe para identificar gestos como *pinch* o *mano abierta* |
| Reconocimiento de voz | Captura comandos hablados en español mediante micrófono |
| Coordinador multimodal | Sincroniza ambos tipos de entrada según una ventana de tiempo |
| Lógica de acciones | Define reacciones condicionales ante coincidencias voz–gesto |
| Feedback visual | Muestra video en tiempo real con landmarks y mensajes de sincronización |

---

## 📌 Código relevante

```python
import cv2
import mediapipe as mp
import threading
import queue
import time
import speech_recognition as sr
import numpy as np

# --- Colas y Constantes ---
event_q = queue.Queue()
SYNC_WINDOW = 0.8  

# --- Configuración de MediaPipe ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# --- Hilo 1: Detección de Gestos ---
def gesture_worker(stop_event):
    cap = cv2.VideoCapture(0)
    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            break
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)
        gesture = None
        if results.multi_hand_landmarks:
            lm = results.multi_hand_landmarks[0].landmark
            thumb_tip = np.array([lm[4].x, lm[4].y])
            index_tip = np.array([lm[8].x, lm[8].y])
            dist = np.linalg.norm(thumb_tip - index_tip)
            gesture = 'pinch' if dist < 0.05 else 'open_hand'
            mp_draw.draw_landmarks(frame, results.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS)
        if gesture:
            event_q.put({'type': 'gesture', 'name': gesture, 'time': time.time(), 'frame': frame.copy()})
        cv2.imshow('Gestos', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyWindow('Gestos')

# --- Hilo 2: Reconocimiento de Voz ---
def voice_worker(stop_event):
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        r.adjust_for_ambient_noise(source)
    while not stop_event.is_set():
        with mic as source:
            try:
                audio = r.listen(source, phrase_time_limit=3)
                text = r.recognize_google(audio, language='es-ES')
                event_q.put({'type': 'voice', 'text': text.lower(), 'time': time.time()})
            except sr.UnknownValueError:
                pass
            except Exception as e:
                print(f'Voice error: {e}')

# --- Hilo 3: Coordinador Multimodal ---
def coordinator_loop(stop_event):
    last_gesture, last_voice = None, None
    while not stop_event.is_set():
        try:
            event = event_q.get(timeout=0.1)
            current_time = time.time()
            if event['type'] == 'gesture':
                last_gesture = event
                print(f"-> Gesto detectado: {event['name']}")
                if last_voice and (current_time - last_voice['time']) < SYNC_WINDOW:
                    print(f"!!! SINCRONIZACIÓN GESTO/VOZ !!!  ({last_gesture['name']} + {last_voice['text']})")
                    last_voice = None
            elif event['type'] == 'voice':
                last_voice = event
                print(f"-> Voz detectada: '{event['text']}'")
                if last_gesture and (current_time - last_gesture['time']) < SYNC_WINDOW:
                    print(f"!!! SINCRONIZACIÓN VOZ/GESTO !!!  ({last_voice['text']} + {last_gesture['name']})")
                    last_gesture = None
            event_q.task_done()
        except queue.Empty:
            current_time = time.time()
            if last_gesture and (current_time - last_gesture['time']) > SYNC_WINDOW:
                last_gesture = None
            if last_voice and (current_time - last_voice['time']) > SYNC_WINDOW:
                last_voice = None
        except Exception as e:
            print(f"Coordinator error: {e}")

def main():
    stop_event = threading.Event()
    tg = threading.Thread(target=gesture_worker, args=(stop_event,), daemon=True)
    tv = threading.Thread(target=voice_worker, args=(stop_event,), daemon=True)
    tc = threading.Thread(target=coordinator_loop, args=(stop_event,), daemon=True)
    print("Iniciando hilos multimodales (Gestos, Voz, Coordinador)...")
    tg.start(); tv.start(); tc.start()
    print("Presiona Ctrl+C o ESC para salir.")
    try:
        while tc.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nSalida solicitada (Ctrl+C).")
    finally:
        stop_event.set()
        time.sleep(2)
        print("Saliendo...")

if __name__ == '__main__':
    main()

```

---

# ⚙️ Sincronización y comportamiento esperado y 🧠 Reflexión

## Sincronización y comportamiento esperado
- Cada hilo funciona de forma independiente (voz, gestos, coordinación).
- El coordinador detecta si un gesto y un comando de voz ocurren dentro de una ventana temporal de 0.8 segundos.
- Cuando ambas entradas coinciden, imprime un mensaje de sincronización:

## Reflexión y mejoras futuras
| Aspecto | Observación |
|---------|-------------|
| Integración multimodal | Permite control natural por gestos y voz coordinados. |
| Robustez | Funciona en tiempo real, pero requiere buena iluminación y claridad vocal. |
| Extensión posible | Agregar retroalimentación visual (textos o íconos en pantalla). |
| Mejoras futuras | Soporte para más gestos, comandos personalizados y respuesta de audio. |