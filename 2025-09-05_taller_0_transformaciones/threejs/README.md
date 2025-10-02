# Three.js - Transformaciones 3D con React Three Fiber

## Instalación

```bash
npm install
```

## Ejecución

```bash
npm run dev
```

El proyecto se ejecutará en `http://localhost:5173/`

## Descripción

Este proyecto implementa transformaciones geométricas básicas en 3D usando React Three Fiber:

### Transformaciones Implementadas

1. **Cubo Rojo - Traslación Senoidal**
   - Movimiento en trayectoria senoidal en los ejes X, Y, Z
   - Usa `Math.sin()` y `Math.cos()` para crear movimiento suave

2. **Esfera Verde - Rotación Continua**
   - Rotación simultánea en los tres ejes
   - Velocidades diferentes para crear movimiento complejo

3. **Cono Azul - Escala Oscilante**
   - Cambio de tamaño usando función senoidal
   - Escala uniforme en todos los ejes

4. **Torus Amarillo - Transformación Compuesta**
   - Combinación de traslación circular, rotación y escala
   - Demuestra la aplicación de múltiples transformaciones

### Características Técnicas

- **useFrame**: Hook para animaciones en tiempo real
- **OrbitControls**: Navegación interactiva de la cámara
- **Shadows**: Sombras realistas
- **Grid Helper**: Sistema de coordenadas visual
- **Responsive Design**: Interfaz adaptable

### Controles

- **Mouse**: Rotar cámara
- **Scroll**: Zoom in/out
- **Click derecho + arrastrar**: Pan de cámara

### Dependencias

- React Three Fiber: Renderer de Three.js para React
- React Three Drei: Utilidades y helpers
- Three.js: Biblioteca 3D principal
