# Utilidades compartidas

Funciones y scripts reutilizables para todo el proyecto.

## Scripts previstos

- `prepare_data.py`: descarga y preprocesa datasets, genera `data/processed`.
- `metrics_export.py`: consolida métricas de cada módulo y las envía al dashboard/SQLite.
- `media_tools.py`: helpers para generar GIFs y videos con ffmpeg.
- `config_loader.py`: utilitario para leer archivos YAML/JSON compartidos.

## Buenas prácticas

- Mantener dependencias ligeras (standard library + paquetes críticos).
- Documentar cada script con `argparse` y ejemplos de uso.
- Evitar dependencias cíclicas; otros módulos deben importar desde `python.utils`.

Actualiza este README cuando se añadan nuevas utilidades.

