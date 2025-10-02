# Taller: Materiales por Iluminación y Modelos de Color en un Mundo Virtual con Three.js

**Fecha:** 2025-10-01

## Objetivo del Taller
Diseñar y curar un mundo virtual donde los materiales respondan a la iluminación y al modelo de color, integrando modelos 3D, materiales PBR, shaders procedurales, cámaras (perspectiva/ortográfica) y animaciones básicas.

## Conceptos Aprendidos
- **Transformaciones geométricas** (escala, rotación, traslación)
- **Shaders y efectos visuales** (skybox con gradiente, partículas)
- **Modelos de color** (RGB/HSV, contraste perceptual CIELAB)
- **Materiales PBR** (albedo, roughness, metalness, normal maps)
- **Iluminación 3D** (key, fill, rim, ambient)
- **Animaciones** (camera path, object swaying, light movement)
- **Atmospheric effects** (fog, particles, sky systems)


## Herramientas y Entornos
- **Three.js** (proyecto local con Vite)
- **GUI:** lil-gui para controles interactivos
- **Animación:** GSAP para transiciones suaves
- **Modelos:** GLB/GLTF con GLTFLoader
- **Texturas:** PBR textures (diffuse, roughness, displacement, normal)

## Estructura del Proyecto
```
2025-10-01_taller_1_materiales_iluminacion_color/
├── threejs/                    # Proyecto Three.js principal
│   ├── src/main.js            # Código principal de la escena
│   ├── public/                # Assets públicos (GLB, texturas)
│   └── package.json           # Dependencias
├── glb_models/                # Modelos 3D originales
├── textures/                  # Texturas PBR originales
├── renders/                   # Capturas y videos finales
├── CAPTURE_GUIDE.md          # Guía para capturas
└── README.md                 # Este archivo
```

## Implementación

### Etapas Realizadas
1. **Preparación de escena base** con Three.js y Vite
2. **Configuración de cámaras** perspectiva y ortográfica con alternancia
3. **Sistema de iluminación** key/fill/rim + 3 presets (nuclear, wasteland, afternoon)
4. **Integración de modelos GLB** (5 cherry trees, 2 police cars, warehouse, grass)
5. **Materiales PBR** para el suelo con texturas completas
6. **Shaders procedurales** (skybox con gradiente, sistema de partículas)
7. **Animaciones** (camera path, swaying trees, light movement)
8. **Efectos atmosféricos** (fog, particles, sky system)

### Código Relevante

#### Sistema de Cámaras y Presets
```js
// Toggle de cámaras
function setCamera(type) {
  activeCamera = type === 'orthographic' ? orthographicCamera : perspectiveCamera
  activeCamera.lookAt(target)
}

// Presets de iluminación
const lightPresets = {
  nuclear: { ambient: { color: 0x4a2c00, intensity: 0.5 }, ... },
  wasteland: { ambient: { color: 0x2c1810, intensity: 0.2 }, ... },
  afternoon: { ambient: { color: 0xf5f5dc, intensity: 0.4 }, ... }
}
```

#### Skybox con Shader
```js
const skyMaterial = new THREE.ShaderMaterial({
  uniforms: {
    topColor: { value: new THREE.Color(0x87CEEB) },
    bottomColor: { value: new THREE.Color(0xFFE4B5) }
  },
  vertexShader: `...`,
  fragmentShader: `...`,
  side: THREE.BackSide
})
```

#### Sistema de Partículas
```js
const particleGeometry = new THREE.BufferGeometry()
const particleCount = 3000
const particleMaterial = new THREE.PointsMaterial({
  color: 0x8b4513, size: 1.0, transparent: true, opacity: 0.6
})
```


## Resultados Visuales

### Video de Demostración
🎬 **[Ver demostración completa en YouTube](https://youtu.be/WXDYKkvm5kc)**

### Capturas del Proyecto
Las capturas están disponibles en la carpeta `renders/`:

- **`01_post_apocalyptic.jpg`** - Nuclear lighting con fog y partículas
- **`02_afternoon_sky.jpg`** - Beautiful gradient skybox con nubes
- **`03_wasteland.jpg`** - Red-orange atmospheric lighting
- **`04_camera_path.jpg`** - Following automated camera path
- **`05_orthographic.jpg`** - Technical/architectural perspective

### Características Demostradas
- ✅ Demostración completa de todas las características
- ✅ Transiciones entre presets de iluminación
- ✅ Animación de cámara automática
- ✅ Toggle entre cámaras perspectiva/ortográfica
- ✅ Efectos atmosféricos dinámicos
- ✅ Sistema de partículas y fog
- ✅ Skybox con gradiente y nubes

## Paleta de Color y Modelos

### Tema Post-Apocalíptico
- **Colores principales:** Naranja nuclear (#ff6600), Marrón oxidado (#8b4513)
- **Contraste CIELAB:** Alto contraste para dramatismo
- **Atmósfera:** Fog denso, partículas de polvo, iluminación dramática

### Tema Afternoon
- **Colores principales:** Azul cielo (#87CEEB), Moccasin (#FFE4B5)
- **Contraste CIELAB:** Suave para ambiente relajado
- **Atmósfera:** Cielo despejado, nubes, sin fog

## Prompts Usados
- N/A (proyecto basado en especificaciones del taller)

## Reflexión Final

### Logros Principales
1. **Integración completa** de modelos GLB con materiales PBR
2. **Sistema de iluminación avanzado** con 3 presets atmosféricos
3. **Shaders procedurales** para skybox y efectos atmosféricos
4. **Animaciones fluidas** con GSAP y Three.js
5. **Interfaz interactiva** con lil-gui para control en tiempo real

### Desafíos Técnicos
- **Optimización de texturas** - Balance entre calidad y rendimiento
- **Sistema de partículas** - Gestión de 3000+ partículas con buen FPS
- **Skybox shader** - Creación de gradiente realista con GLSL
- **Camera path** - Animación suave con CatmullRomCurve3

### Aprendizajes Clave
- **PBR workflow** - Integración correcta de albedo, roughness, normal maps
- **Lighting design** - Key/fill/rim para diferentes atmósferas
- **Performance optimization** - LOD, culling, efficient rendering
- **User experience** - GUI intuitiva para exploración de la escena

## Checklist de Entrega ✅

### Estructura y Código
- ✅ Carpeta `2025-10-01_taller_1_materiales_iluminacion_color`
- ✅ Código funcional en `threejs/`
- ✅ Modelos GLB integrados (5+ modelos)
- ✅ Texturas PBR aplicadas
- ✅ Shaders procedurales implementados

### Funcionalidades
- ✅ Cámaras perspectiva y ortográfica con toggle
- ✅ Sistema de iluminación con 3 presets
- ✅ Animaciones (camera path, object swaying)
- ✅ Efectos atmosféricos (fog, particles, sky)
- ✅ GUI interactiva completa

### Documentación
- ✅ README técnico completo
- ✅ Guía de captura detallada
- ✅ Código comentado y organizado
- ✅ Commits descriptivos en inglés

### Completado ✅
- ✅ Capturas finales (disponibles en `renders/`)
- ✅ Video de demostración ([YouTube](https://youtu.be/WXDYKkvm5kc))
- ✅ Documentación técnica completa

## Contributions

### Individual Contributions:
- **Scene Architecture**: Designed complete Three.js scene structure with cameras, lighting, and animation systems
- **PBR Materials**: Implemented physically-based rendering materials with diffuse, roughness, and displacement maps
- **Procedural Shaders**: Created custom skybox gradient shader and particle system for atmospheric effects
- **Lighting System**: Developed 3-point lighting rig with 3 distinct presets (nuclear, wasteland, afternoon)
- **Animation Pipeline**: Implemented camera path animation, object swaying, and light movement using GSAP
- **GUI Integration**: Built comprehensive lil-gui interface for real-time scene control
- **Model Integration**: Loaded and positioned 5+ GLB models with proper scaling and shadow casting
- **Documentation**: Created complete technical documentation and capture guide
- **Code Organization**: Structured modular, commented code following Three.js best practices

### Technical Achievements:
- **Performance Optimization**: Managed 3000+ particles with smooth 60fps rendering
- **Shader Programming**: Custom GLSL shaders for realistic sky gradients
- **Asset Pipeline**: Efficient GLB loading with error handling and progress tracking
- **User Experience**: Intuitive controls for exploring different scene configurations

