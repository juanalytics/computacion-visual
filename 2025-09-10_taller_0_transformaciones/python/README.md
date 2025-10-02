# Python - Transformaciones 2D

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
python transformaciones_2d.py
```

## Descripción

Este script implementa transformaciones geométricas básicas en 2D:

- **Traslación**: Movimiento de la figura en el plano
- **Rotación**: Giro alrededor del origen
- **Escala**: Cambio de tamaño
- **Transformaciones compuestas**: Combinación de múltiples transformaciones

### Características

- Usa matrices de transformación homogéneas (3x3)
- Genera visualizaciones estáticas y animadas
- Exporta GIF animado usando imageio
- Muestra información de matrices en tiempo real

### Salidas

- `transformaciones_estaticas.png`: Imagen con todas las transformaciones
- `hola_mundo_transformaciones_python.gif`: Animación completa

## Resultado Visual

![Transformaciones Python](../resultados/hola_mundo_transformaciones_python.gif)

**Transformaciones 2D implementadas:**
- **Cubo rojo**: Traslación senoidal en X e Y
- **Esfera verde**: Rotación continua incremental  
- **Triángulo naranja**: Escala oscilante
- **Figura púrpura**: Transformación compuesta (traslación + rotación + escala)

La animación muestra matrices de transformación homogéneas aplicadas en tiempo real usando `numpy` y `matplotlib`.
