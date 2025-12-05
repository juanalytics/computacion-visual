# Proyecto Unity

## Objetivos

- Implementar escena interactiva con cinemática directa (FK) e inversa (IK).
- Integrar partículas, colisiones y transiciones animadas controladas por comandos externos.
- Recibir mensajes del broker WebSocket para reaccionar en tiempo real.

## Escenario actual

- Se añadió `Assets/Scripts/WsCommandListener.cs`, un cliente basado en **NativeWebSocket** que escucha `type: "command"` del broker y ejecuta acciones sobre la escena (color, animación, cámara, luz).
- Al conectarse envía un mensaje `status` con `state: ready`.
- Se añadieron dos componentes extra para cumplir el requisito de IK/FX:
  - `IKRigController`: controla el IK de la mano derecha mediante `OnAnimatorIK`. Recibe la acción `set_ik_pose` con `params.pose` (`reach` o `idle`).
  - `FxController`: dispara un `ParticleSystem` + luz secundaria al recibir `fx_pulse` (`params.color`, `params.intensity`).
- Las acciones soportadas ahora:
  - `change_material` → cambia el color del material (HTML hex).
  - `trigger_animation` → lanza el trigger `react`.
  - `switch_camera` → alterna entre los Transform `Camera Near/Far`.
  - `toggle_light` → enciende/apaga la luz principal (usa `params.intensity`).
  - `set_ik_pose` → mueve la mano al target de IK (`reach`/`idle`).
  - `fx_pulse` → activa partículas + luz de acento con el color/intensidad recibidos.

## Cómo configurar el proyecto

1. **Crear proyecto Unity 2022 LTS (URP o 3D Core)** y copiar esta carpeta `unity/` dentro del repo.
2. **Instalar NativeWebSocket**: en el Package Manager usa `Add package from git URL…` e introduce `https://github.com/endel/NativeWebSocket.git#4.0.3`.
3. Copia `Assets/Scripts/WsCommandListener.cs` dentro del proyecto (ya está en la carpeta).
4. En la escena principal agrega un GameObject vacío (`WebSocketClient`) y adjunta el script.
5. Asigna referencias en el inspector:
   - `Target Renderer`: malla/material que cambiará de color.
   - `Target Animator` (opcional): debe tener un trigger llamado `react`.
   - `Scene Light`: luz direccional a manipular.
   - `Camera Rig`, `Camera Near`, `Camera Far`: transforms que definen las posiciones de cámara.
   - `IKRigController`: arrástralo si quieres IK (debe tener referencias a `rightHandTarget` y `rightHandHome`).
   - `FxController`: asigna un ParticleSystem y una luz secundaria.
6. Ajusta `Websocket Url` según el servidor (por defecto `ws://localhost:8000/ws`). Para producción usa la IP/puerto reales.
7. Ejecuta la escena; en consola deberías ver `[UnityWS] Connection opened`. Puedes probar con los pipelines de gestos/voz, enviando acciones como:
   - `trigger_animation`
   - `toggle_light`
   - `switch_camera`
   - `set_ik_pose` (`params.pose: "reach"`)
   - `fx_pulse` (`params.color: "#FF5500"`, `params.intensity: 3`)

## Próximos pasos

- Integrar Cinemachine y animaciones IK/FX que respondan a `trigger_animation`.
- Añadir partículas, post-procesado y optimización de GPU (Frame Debugger/Profiler).
- Implementar un emisor `status` periódico (ej. FPS actual) para el dashboard.
- Capturar GIFs y video del flujo completo para `docs/EVIDENCIAS.md`.

## Carpeta sugerida

```
unity/
├── Assets/
│   └── Scripts/
├── Packages/
├── ProjectSettings/
└── README.md
```

Mantén esta carpeta sincronizada (usa `.gitignore` de Unity y UnityYAMLMerge si aplica).

