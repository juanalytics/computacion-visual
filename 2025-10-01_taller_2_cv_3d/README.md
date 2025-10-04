# Taller 2: Computación Visual & 3D - Jerarquías, Proyección, Raster, Visión por Computador y Generación Paramétrica

**Fecha:** 2025-10-01

## Objetivo del Taller
Integrar en un solo taller (multi-módulo) los temas de gráficos 3D y visión por computador: jerarquías y transformaciones, proyecciones de cámara, rasterización clásica, visión artificial (filtros, bordes, segmentación, análisis geométrico), modelos de color, conversión e inspección de formatos 3D, escenas paramétricas desde datos, filtros por convolución personalizada, y control por gestos con webcam.

## Ejercicios Realizados

### Ejercicio 2 — Ojos Digitales (Filtros y Bordes con OpenCV) ✅
**Meta:** Comprender el flujo básico de percepción: escala de grises, filtros y bordes.

**Implementación:**
- Conversión a escala de grises
- Filtros de desenfoque (Gaussiano, promedio, bilateral)
- Filtros de enfoque (kernel personalizado, unsharp masking)
- Detección de bordes (Sobel X/Y, Laplaciano, Canny)
- Análisis comparativo con métricas cuantitativas
- Notebook interactivo con widgets para exploración en tiempo real

**Evidencia:** Collage comparativo con 12 imágenes mostrando diferentes filtros y métodos de detección de bordes.

**Resultados Clave:**
- **Filtros de Suavizado**: Gaussian (σ=1.0), Average (5x5), Bilateral (preserva bordes)
- **Filtros de Enfoque**: Kernel personalizado, Unsharp Masking (α=1.5, σ=1.0)
- **Detección de Bordes**: Sobel X/Y/Combinado, Laplacian, Canny (50-150)
- **Métricas Cuantitativas**: Picos detectados, área de bordes, intensidad promedio

**Código:** [Ver implementación](./ejercicios/02_ojos_digitales_opencv/)

**Comentarios personales:** 
- Aprendizaje sobre las diferencias entre métodos de filtrado
- Desafío en la optimización de parámetros para diferentes tipos de imágenes
- Mejora futura: implementar filtros adaptativos basados en contenido

### Ejercicio 3 — Segmentando el Mundo (Binarización y Contornos) ✅
**Meta:** Umbralización (fija y adaptativa) y detección de formas.

**Implementación:**
- 4 métodos de umbralización (Fixed, Adaptive Mean, Adaptive Gaussian, Otsu)
- Detección de contornos con análisis geométrico
- Cálculo de propiedades (área, perímetro, centroides)
- Clasificación automática de formas (triángulo, cuadrado, círculo)
- Visualización con contornos, centroides y cajas delimitadoras
- GIF animado mostrando el proceso de segmentación

**Evidencia:** Comparación visual 2x3 + GIF animado mostrando original → segmentado → contornos/centroides.

**Resultados Clave:**
- **4 Métodos de Umbralización**: Fixed (127), Adaptive Mean (11x11), Adaptive Gaussian (11x11), Otsu
- **Detección de Contornos**: Análisis geométrico con propiedades (área, perímetro, centroides)
- **Clasificación de Formas**: Triángulo, cuadrado, círculo automática basada en vértices
- **Visualización**: Contornos verdes, centroides rojos, cajas delimitadoras azules

**Código:** [Ver implementación](./ejercicios/03_segmentacion_umbral_contornos/)

**Comentarios personales:**
- Aprendizaje sobre diferentes métodos de umbralización y sus aplicaciones
- Desafío en la optimización de parámetros para detección de contornos
- Mejora futura: implementar segmentación basada en watershed

### Ejercicio 4 — Imagen = Matriz (Canales, Slicing, Histogramas) ✅
**Meta:** Manipular pixeles y regiones directamente.

**Implementación:**
- Separación de canales RGB y HSV individuales
- Operaciones de slicing y edición de regiones específicas
- Análisis de histogramas de intensidades
- Operaciones de brillo y contraste
- Transformaciones de matriz (inversión, rotación, bitwise)
- Visualización comparativa 4x4 con 16 operaciones diferentes

**Evidencia:** Comparación visual 4x4 + análisis de histogramas 2x2 mostrando todas las operaciones de matriz.

**Resultados Clave:**
- **Separación de Canales**: RGB (Rojo, Verde, Azul) + HSV (Hue, Saturación, Valor)
- **Operaciones de Slicing**: Región roja (100:200, 150:300), copia/pega, blur selectivo, máscara circular
- **Operaciones de Matriz**: Inversión (255-pixel), brillo/contraste (α=1.5, β=50), rotación 45°, bitwise AND
- **Análisis de Histogramas**: Distribución de intensidades, comparación RGB/HSV, estadísticas (μ=38.4, σ=70.3)

**Código:** [Ver implementación](./ejercicios/04_imagen_matriz_pixeles/)

**Comentarios personales:**
- Aprendizaje sobre manipulación directa de píxeles y matrices
- Desafío en la optimización de operaciones vectorizadas con NumPy
- Mejora futura: implementar operaciones de convolución personalizadas

## Herramientas y Entornos
- **Python** (opencv-python, numpy, matplotlib, jupyter)
- **OpenCV** para procesamiento de imágenes
- **Jupyter Notebook** para exploración interactiva
- **Matplotlib** para visualización

## Estructura del Proyecto
```
2025-10-01_taller_2_cv_3d/
├── ejercicios/
│   ├── 02_ojos_digitales_opencv/     # ✅ Completado
│   ├── 03_segmentacion_umbral_contornos/  # ✅ Completado
│   └── 04_imagen_matriz_pixeles/     # ✅ Completado
├── assets/                           # Imágenes de entrada, modelos 3D
├── resultados/                       # Evidencias animadas por ejercicio
└── README.md                         # Este archivo
```

## Dependencias y Cómo Ejecutar

### Python (OpenCV/NumPy/etc.)
```bash
# Instalar dependencias
pip install opencv-python numpy matplotlib jupyter ipywidgets

# Ejecutar ejercicio 2
cd ejercicios/02_ojos_digitales_opencv/python
python ojos_digitales.py

# O ejecutar notebook interactivo
jupyter notebook ojos_digitales_interactive.ipynb
```

## Resumen de Evaluación

### Criterios de Evaluación Cumplidos ✅

#### **Ejercicio 2 - Ojos Digitales**
- ✅ **Implementación completa**: 12 filtros diferentes (blur, sharpen, edge detection)
- ✅ **Análisis cuantitativo**: Métricas de detección de bordes
- ✅ **Visualización profesional**: Collage 3x4 con etiquetas claras
- ✅ **Código documentado**: Funciones bien estructuradas y comentadas
- ✅ **Notebook interactivo**: Exploración en tiempo real con widgets

#### **Ejercicio 3 - Segmentando el Mundo**
- ✅ **4 métodos de umbralización**: Fixed, Adaptive Mean, Adaptive Gaussian, Otsu
- ✅ **Detección de contornos**: Análisis geométrico completo
- ✅ **Clasificación de formas**: Automática (triángulo, cuadrado, círculo)
- ✅ **GIF animado**: Proceso de segmentación paso a paso
- ✅ **Visualización avanzada**: Contornos, centroides, cajas delimitadoras

#### **Ejercicio 4 - Imagen = Matriz**
- ✅ **Separación de canales**: RGB y HSV individuales
- ✅ **Operaciones de slicing**: 4 tipos diferentes de manipulación de regiones
- ✅ **Análisis de histogramas**: Estadísticas completas de distribución
- ✅ **Operaciones de matriz**: Inversión, rotación, bitwise, transformaciones
- ✅ **Visualización 4x4**: 16 operaciones diferentes en una sola imagen

### Archivos de Evidencia Generados
- **Ejercicio 2**: `comparison_collage.png` + 12 imágenes individuales
- **Ejercicio 3**: `comparison_segmentation.png` + `segmentacion_proceso.gif`
- **Ejercicio 4**: `comparison_matrix_operations.png` + `histograms_analysis.png` + 16 imágenes individuales

### Métricas Técnicas Logradas
- **Filtros implementados**: 12 diferentes con parámetros optimizados
- **Métodos de umbralización**: 4 con análisis comparativo
- **Operaciones de matriz**: 16 diferentes incluyendo slicing y transformaciones
- **Análisis estadístico**: Histogramas, métricas cuantitativas, clasificación automática

## Créditos/Referencias
- OpenCV Documentation: https://docs.opencv.org/
- NumPy Documentation: https://numpy.org/doc/
- Matplotlib Documentation: https://matplotlib.org/stable/
