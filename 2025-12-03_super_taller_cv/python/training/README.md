# Módulo de entrenamiento y fine-tuning

## Objetivos

- Entrenar una CNN desde cero como baseline.
- Aplicar fine-tuning a modelos preentrenados (ResNet50, MobileNetV3, etc.).
- Implementar validación cruzada y comparación de métricas.
- Versionar modelos y registrar experimentos.

## Backlog inicial

1. `requirements.txt` específico (PyTorch, torchvision, lightning opcional).
2. `scripts/data_module.py`: loaders estandarizados (CIFAR10 por defecto) con opción de submuestreo.
3. `scripts/train_scratch.py`: define arquitectura personalizada + entrenamiento (implementado).
4. `scripts/train_finetune.py`: carga ResNet18 preentrenada y ajusta las capas finales (implementado).
5. `evaluate.py`: genera reportes (`classification_report`, curvas ROC/PR).
6. Integración con `python/utils/metrics_export.py` para enviar métricas al dashboard.

## Estructura sugerida

```
training/
├── configs/
├── models/
├── scripts/
│   ├── train_scratch.py
│   ├── train_finetune.py
│   └── evaluate.py
└── experiments/
```

## Métricas y reportes

- Accuracy, F1 macro, ROC-AUC.
- Tiempo por epoch, uso de GPU.
- Comparativa clara entre baseline y fine-tuning (tabla + gráfica).

Los resultados deben sincronizarse con `docs/METRICAS.md` y publicarse en `results/training/<experimento>/`.

## Uso rápido (`scripts/train_scratch.py`)

```bash
python python/training/scripts/train_scratch.py \
  --config python/training/configs/cnn_scratch.yaml \
  --device cpu \
  --epochs 1
```

El archivo de configuración controla batch size, fracción de datos (`train_fraction`, `val_fraction`), LR y carpeta de salida (`results/training/cnn_scratch`). El entrenamiento genera `model_best.pt` y `metrics.json`.

## Uso rápido (`scripts/train_finetune.py`)

```bash
python python/training/scripts/train_finetune.py \
  --config python/training/configs/resnet_finetune.yaml \
  --device cpu \
  --epochs 1
```

`resnet_finetune.yaml` permite definir qué parte del backbone se congela (`freeze_backbone_until`), las fracciones del dataset y la carpeta de salida (`results/training/resnet18_finetune`). El script aplica augmentations tipo ImageNet y guarda métricas/weights.

