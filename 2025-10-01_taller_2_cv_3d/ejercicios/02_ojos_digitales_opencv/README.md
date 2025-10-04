# Ejercicio 2: Ojos Digitales - Filtros y Bordes con OpenCV

## Objetivo
Entender el flujo básico de percepción: escala de grises, filtros y bordes mediante implementación de diferentes algoritmos de procesamiento de imágenes con OpenCV.

## Conceptos Aplicados
- **Conversión a escala de grises** - Reducción de dimensionalidad de color
- **Filtros de desenfoque** - Gaussiano, promedio, bilateral
- **Filtros de enfoque** - Kernel de enfoque, unsharp masking
- **Detección de bordes** - Sobel X/Y, Laplaciano, Canny
- **Análisis comparativo** - Métricas de rendimiento y visualización

## Estructura del Ejercicio
```
02_ojos_digitales_opencv/
├── python/
│   ├── ojos_digitales.py              # Script principal
│   ├── ojos_digitales_interactive.ipynb # Notebook interactivo
│   └── requirements.txt               # Dependencias
├── assets/
│   └── sample_image.jpg              # Imagen de prueba
├── resultados/                       # Resultados generados
└── README.md                        # Este archivo
```

## Instalación y Ejecución

### Requisitos
```bash
pip install -r python/requirements.txt
```

### Ejecución del Script Principal
```bash
cd python
python ojos_digitales.py
```

### Ejecución del Notebook Interactivo
```bash
cd python
jupyter notebook ojos_digitales_interactive.ipynb
```

## Funcionalidades Implementadas

### 1. Conversión a Escala de Grises
- Conversión BGR → RGB para visualización
- Conversión BGR → Grayscale para procesamiento

### 2. Filtros de Desenfoque
- **Gaussiano**: Suavizado uniforme con kernel configurable
- **Promedio**: Filtro de promedio simple
- **Bilateral**: Preserva bordes mientras suaviza

### 3. Filtros de Enfoque
- **Kernel de enfoque**: Realza bordes con kernel personalizable
- **Unsharp Masking**: Enfoque más natural y controlado

### 4. Detección de Bordes
- **Sobel X**: Detecta bordes verticales
- **Sobel Y**: Detecta bordes horizontales
- **Sobel Combinado**: Detección omnidireccional
- **Laplaciano**: Detecta cambios bruscos de intensidad
- **Canny**: Algoritmo robusto con supresión de no-máximos

### 5. Análisis Comparativo
- Métricas cuantitativas (píxeles de borde, intensidad promedio)
- Visualización comparativa lado a lado
- Histogramas de intensidad
- Superposición de resultados

## Resultados Esperados

### Collage Comparativo
El script genera un collage con 12 imágenes mostrando:
1. Imagen original
2. Escala de grises
3. Blur gaussiano
4. Blur bilateral
5. Enfoque
6. Unsharp masking
7. Sobel X
8. Sobel Y
9. Sobel combinado
10. Laplaciano
11. Canny
12. Blur promedio

### Análisis de Diferencias
- **Filtros de desenfoque**: Comparación de suavizado vs preservación de bordes
- **Filtros de enfoque**: Análisis de realce vs artefactos
- **Detección de bordes**: Rendimiento y robustez de cada método

## Características Técnicas

### Optimizaciones Implementadas
- Validación de kernels impares para filtros
- Normalización de intensidades para visualización
- Manejo de errores en carga de imágenes
- Guardado automático de resultados

### Widgets Interactivos (Notebook)
- Sliders para ajustar parámetros en tiempo real
- Visualización inmediata de cambios
- Comparación dinámica de métodos

## Aprendizajes Clave

1. **Diferencias entre filtros de desenfoque**:
   - Gaussiano: Suave y uniforme
   - Bilateral: Preserva bordes importantes
   - Promedio: Simple pero puede crear artefactos

2. **Métodos de detección de bordes**:
   - Sobel: Rápido, bueno para bordes simples
   - Laplaciano: Sensible al ruido, detecta detalles finos
   - Canny: Más robusto, mejor para aplicaciones reales

3. **Parámetros críticos**:
   - Tamaño de kernel afecta suavizado
   - Umbrales de Canny determinan sensibilidad
   - Fuerza de enfoque puede crear halos

## Mejoras Futuras
- Implementación de filtros personalizados
- Análisis de frecuencia con FFT
- Detección de bordes adaptativa
- Integración con webcam en tiempo real
- Métricas de calidad de imagen (PSNR, SSIM)
