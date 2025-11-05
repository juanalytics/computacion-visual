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
![luz ambiental + direccional, materiales estándar con sombras.](renders/punto_6-4.gif)
- ✅ **Interacción y colisiones**:
![fisicas realistas de objetos](renders/punto_6-1.gif)
![jugador mueve y choca con objetos](renders/punto_6-2.gif)
![clic en cajas cambia color y registra eventos](renders/punto_6-3.gif)

- ✅ **UI en la escena**:
![slider para gravedad](renders/punto_6-5.gif)
![slider para velocidad](renders/punto_6-6.gif)
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
