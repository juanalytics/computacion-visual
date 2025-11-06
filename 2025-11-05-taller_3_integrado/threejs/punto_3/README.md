# Ejercicio 3: Shaders Personalizados GLSL con React Three Fiber

## Descripción

Este ejercicio implementa un playground de shaders personalizados utilizando React Three Fiber y GLSL, demostrando diferentes técnicas de shader programming y su integración con interacción del usuario. El objetivo es mostrar cómo crear efectos visuales avanzados mediante shaders personalizados escritos directamente en GLSL.

## Características Implementadas

![Escena Completa](./../../renders/punto3_escena_completa.gif)

### ✅ Shaders Procedurales

- **Shader con tiempo y mouse**: Efectos generados mediante funciones matemáticas que responden al tiempo y posición del mouse
- **Paleta de colores procedural**: Generación de colores mediante funciones trigonométricas
- **Efecto de glow interactivo**: Resplandor que sigue la posición del mouse

### ✅ Shader Toon

- **Iluminación estilizada**: Bandas de color discretas (cel shading)
- **Rim lighting**: Efecto de borde brillante
- **Luz animada**: Posición de luz que se mueve en círculo
- **Interacción con hover**: Efecto visual al pasar el mouse sobre el objeto

### ✅ Shader con Deformación y Ruido

- **Deformación de vértices**: Ondas sinusoidales que modifican la geometría en tiempo real
- **Ruido procedural**: Patrones generados mediante múltiples capas de funciones seno
- **Mezcla de colores dinámica**: Transición entre colores basada en posición y tiempo
- **Interacción con hover y click**: Efectos que responden a interacción del usuario

### ✅ Interacción Reactiva

- **Estados de hover**: Efectos visuales que responden al hover del mouse
- **Estados de click**: Inversión de colores al hacer click en objetos
- **Tracking de mouse global**: Posición del mouse afecta efectos de glow
- **Sincronización con React**: Uso de `useState` y `useFrame` para controlar shaders

## Uso

### Ejecución Local

1. Instalar dependencias:
```bash
npm install
```

2. Ejecutar servidor de desarrollo:
```bash
npm run dev
```

3. Abrir en navegador: `http://localhost:5173`

### Controles

- **Mouse**: Arrastrar para rotar la cámara (OrbitControls)
- **Hover**: Pasar el mouse sobre objetos para ver efectos de iluminación
- **Click**: Hacer click en la caja procedural para invertir colores
- **Mouse movement**: El movimiento del mouse afecta el efecto de glow en el ground

## Estructura del Código

```
punto_3/
├── src/
│   ├── App.jsx          # Componente principal con shaders y lógica
│   ├── main.jsx          # Punto de entrada
│   └── index.css        # Estilos
├── index.html           # HTML principal
├── package.json         # Dependencias
└── README.md           # Este archivo
```

## Detalles Técnicos

### Shader Procedural con Tiempo y Mouse

El shader del ground utiliza:
- Función `palette()` para generar colores mediante coseno
- Variables `uTime` y `uMouse` como uniforms
- Efecto de glow basado en distancia al mouse
- Patrones de rayas animadas

### Shader Toon

El shader de la esfera implementa:
- Cálculo de iluminación Lambert
- Cuantización de valores (bandas) para efecto toon
- Rim lighting mediante cálculo de dot product
- Uniform `uHover` para efecto de resplandor

### Shader con Deformación de Vértices

El shader del cubo incluye:
- Deformación en vertex shader mediante funciones seno
- Ruido procedural en fragment shader
- Mezcla de múltiples patrones de color
- Uniforms `uHover` y `uClick` para interacción

### Gestión de Recursos

- Uso de `useMemo` para crear materiales una sola vez
- `useEffect` para limpieza de materiales con `dispose()`
- `useFrame` para actualizar uniforms en cada frame
- Hook personalizado `useMouseGlobal` para tracking de mouse

## Tecnologías Utilizadas

- **React**: Framework UI
- **Vite**: Build tool y servidor de desarrollo
- **@react-three/fiber**: Renderizado de Three.js en React
- **@react-three/drei**: Utilidades (OrbitControls, Stats)
- **Three.js**: Motor 3D WebGL
- **GLSL**: Lenguaje de shaders

## Referencias

- [Three.js Documentation](https://threejs.org/docs/)
- [React Three Fiber](https://docs.pmnd.rs/react-three-fiber/getting-started/introduction)
- [The Book of Shaders](https://thebookofshaders.com/)
- [GLSL Reference](https://www.khronos.org/opengl/wiki/OpenGL_Shading_Language)
