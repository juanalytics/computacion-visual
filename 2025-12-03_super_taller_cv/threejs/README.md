# Escena Three.js / React Three Fiber

## Objetivos

- Construir escena principal en WebGL con React Three Fiber (R3F).
- Incluir overlays dinámicos (HUD para detecciones) y modo AR (AR.js o WebXR).
- Escuchar comandos del broker WebSocket para modificar materiales, luces, cámaras y animaciones.

## Backlog inicial

1. Inicializar proyecto (Vite + React + TypeScript recomendado).
2. Configurar R3F + Drei + Zustand para manejo de estado.
3. Implementar `wsClient.ts` que procese mensajes `command` y `detections`.
4. Crear componentes:
   - `DetectionOverlay`: proyecta bounding boxes en pantalla.
   - `SceneController`: aplica cambios de materiales/cámaras.
   - `ARMarkerScene`: modo AR opcional.
5. Optimización visual: LOD, compresión de texturas, control de sombras.

## Métricas de performance

- FPS objetivo ≥ 60 (desktop), ≥ 30 (mobile).
- Peso total de assets < 20 MB.
- Latencia de reacción < 150 ms desde comando recibido.

Registrar pruebas en `docs/METRICAS.md` y generar GIFs (`docs/EVIDENCIAS.md`).

