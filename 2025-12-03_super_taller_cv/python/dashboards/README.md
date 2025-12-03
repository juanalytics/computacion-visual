# Módulo de dashboards y observabilidad

## Objetivos

- Visualizar métricas en tiempo real (FPS, uso GPU/CPU, latencia, estado de comandos).
- Mostrar comparativas de modelos (CNN vs fine-tuning).
- Exponer logs y eventos relevantes para la demo.

## Tecnologías sugeridas

- Streamlit / Plotly Dash / Panel (por decidir).
- Conexión WebSocket (para tiempo real) + lectura de SQLite/CSV histórico.
- Librerías de gráficos: Plotly, ECharts, Altair.

## Backlog inicial

1. `app.py`: dashboard principal con secciones (Percepción, DL, Multimodal, Visualización).
2. `services/ws_client.py`: suscripción a broker WS.
3. `services/storage.py`: lectura de `metrics.db` o `results/*/metrics.json`.
4. Widgets para:
   - FPS/latencia (gauge).
   - Uso GPU/CPU (línea temporal).
   - Comparativa de accuracies.
   - Estado de comandos (últimos eventos).
5. Exportar snapshots (`png`/`html`) para `results/`.

## Integraciones

- Consume `python/websockets_api`.
- Produce capturas para `docs/EVIDENCIAS.md`.
- Puede emitir eventos simples (ej. `dashboard/snapshot`) si se requiere.

