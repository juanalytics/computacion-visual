# Proyecto Unity

## Objetivos

- Implementar escena interactiva con cinemática directa (FK) e inversa (IK).
- Integrar partículas, colisiones y transiciones animadas controladas por comandos externos.
- Recibir mensajes del broker WebSocket para reaccionar en tiempo real.

## Backlog inicial

1. Crear proyecto Unity 2022 LTS (URP).
2. Configurar paquetes: Input System, Cinemachine, Visual Effect Graph (opcional).
3. Implementar `WebSocketClient` (C#) que interprete mensajes `command`.
4. Controlador de personaje/rig con blend entre FK e IK.
5. Sistema de partículas/FX que responda a parámetros (`color`, `intensity`).
6. Perfilado de rendimiento (Frame Debugger, Profiler) y exporte de métricas.

## Integración

- Scripts deben exponer un `Status` enviado periódicamente (`type: status`).
- Las acciones recomendadas: `trigger_animation`, `set_light`, `set_particle_color`.
- Generar GIFs y video de esta escena para `docs/EVIDENCIAS.md`.

## Carpeta sugerida

```
unity/
├── Assets/
├── Packages/
├── ProjectSettings/
└── README.md
```

Mantén esta carpeta sincronizada (se recomienda `.gitignore` apropiado y uso de UnityYAMLMerge si aplica).

