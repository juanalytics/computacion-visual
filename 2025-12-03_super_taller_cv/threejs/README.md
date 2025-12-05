# Three.js + React Three Fiber

Este subproyecto usa **Vite + React + TypeScript** y monta una escena en **React Three Fiber** que se sincroniza con el broker WebSocket.

## Características actuales

- Escena con un cubo animado, luces y `MeshDistortMaterial`.
- Overlay HUD con estado de conexión al WS (`connecting`, `connected`, `error`).
- Overlay de detecciones: escucha mensajes `type: "detections"` y pinta bounding boxes en pantalla. Se espera que el payload incluya `frame: {width, height}` (ya enviado por `scripts/inference.py` o `scripts/mock_publisher.py`).
- Cliente WebSocket (`useWsCommands`) que escucha `type: "command"` o `type: "fusion_command"` y aplica:
  - `change_material`: cambia el color del cubo (usa color enviado o genera uno aleatorio).
  - `trigger_animation`: aplica un “pulse” temporal (escala animada).
  - `switch_camera`: placeholder listo para extender (p.ej. alternar posiciones de cámara).
- Dependencias clave: `@react-three/fiber`, `@react-three/drei`, `zustand` (para futuros estados compartidos), `three`.

## Scripts

```bash
npm install      # Una sola vez
npm run dev      # Servidor HMR en http://localhost:5173
npm run build    # Compila a dist/
npm run preview  # Vista previa de producción
npm run lint     # ESLint + TypeScript checks
```

## Configurar la URL del WebSocket

Por defecto se conecta a `ws://localhost:8000/ws`. Para apuntar a otro host/puerto:

```js
localStorage.setItem("threejs_ws_url", "ws://127.0.0.1:8000/ws");
location.reload();
```

## Próximos pasos

- Dibujar overlays de detecciones (HUD con bounding boxes coordinados).
- Consumir detecciones reales desde el pipeline de visión y validar la precisión visual. Mientras tanto, puedes usar `python python/detection/scripts/mock_publisher.py --ws-url ws://127.0.0.1:8000/ws` para simular detecciones.
- Añadir assets GLTF y animaciones más complejas.
- Integrar cambios de cámara/luz con los comandos de multimodalidad.
- Preparar modo AR/WebXR o integración con AR.js según la rúbrica.

Documenta métricas de FPS/latencia en `docs/METRICAS.md` y captura GIFs para `docs/EVIDENCIAS.md` cuando la escena esté lista para la demo.
