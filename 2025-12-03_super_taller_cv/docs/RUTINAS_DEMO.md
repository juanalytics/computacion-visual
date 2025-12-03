# Rutinas de demo

Guion para la presentación final y pruebas internas.

## 1. Preparación previa

1. Activar entorno Python: `conda activate super-taller` (o equivalente).
2. Iniciar servidor WebSocket: `python python/websockets_api/main.py`.
3. Lanzar dashboard: `python python/dashboards/app.py`.
4. Ejecutar escena Three.js: `npm run dev` dentro de `threejs/`.
5. Abrir proyecto Unity y presionar Play.
6. Verificar captura de pantalla/video (OBS o similar).

## 2. Secuencia sugerida (5–7 minutos)

| Paso | Módulo | Acción | Evidencia |
| --- | --- | --- | --- |
| 1 | Detección | Mostrar YOLO + segmentación activa | GIF-01 |
| 2 | Multimodal | Ejecutar gesto mano derecha → cambio material Three.js | GIF-02 |
| 3 | Voz | Comando voz “switch camera” → cámara Unity | GIF-02/05 |
| 4 | EEG simulado | Superar umbral → activar partículas Unity | GIF-05 |
| 5 | Dashboard | Enseñar métricas en tiempo real | GIF-03 |
| 6 | Comparativa DL | Mostrar gráficas CNN vs FT | GIF-06 |
| 7 | AR/3D | Mostrar overlay AR o animación compleja Three.js | GIF-04 |
| 8 | Resumen | Panel final con resultados y métricas clave | Capturas |

## 3. Checklist rápido antes de grabar

- [ ] Todos los servicios levantados y sincronizados.
- [ ] Modelos correctos cargados (versiones más recientes).
- [ ] Métricas visibles en dashboard.
- [ ] Escenas 3D y Unity suscritas al WebSocket.
- [ ] Iluminación/sonido adecuados para grabar.
- [ ] Scripts de fallback listos (presentar video pregrabado si algo falla).

## 4. Evidencias relacionadas

- Actualiza `docs/EVIDENCIAS.md` tras cada grabación.
- Guarda las grabaciones en `results/media/` con nombres `demo_<fecha>.mp4`.

## 5. Notas de mejora continua

Utiliza esta sección para registrar aprendizajes durante ensayos:

- _(pendiente)_

Mantén este guion alineado con el roadmap y ajusta el tiempo asignado a cada módulo según la complejidad real.

