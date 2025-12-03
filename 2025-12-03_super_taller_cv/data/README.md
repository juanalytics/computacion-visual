# Gestión de datos

## Jerarquía sugerida

```
data/
├── raw/
├── processed/
├── models/
└── README.md
```

## Lineamientos

- Mantener datos sensibles fuera del repo; usar scripts de descarga.
- Documentar cada dataset en `data/raw/DATASET_NAME.md`.
- Versionar modelos con nombres `model_<modulo>_<fecha>.pth` y habilitar Git LFS si superan 100 MB.
- Sincronizar `prepare_data.py` con esta estructura para evitar confusiones.

Actualiza este archivo cada vez que se agregue un nuevo dataset o modelo relevante.

