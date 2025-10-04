# Ejercicio 3: Segmentando el Mundo - Binarización y Contornos

## Objetivo
Umbralización (fija y adaptativa) y detección de formas mediante implementación de diferentes algoritmos de segmentación de imágenes con OpenCV.

## Conceptos Aplicados
- **Umbralización fija** - Threshold binario simple
- **Umbralización adaptativa** - Media y Gaussiana para iluminación variable
- **Umbralización automática** - Método de Otsu
- **Detección de contornos** - findContours con diferentes aproximaciones
- **Análisis geométrico** - Área, perímetro, centroides, clasificación de formas
- **Visualización** - Dibujo de contornos, cajas delimitadoras, etiquetas

## Estructura del Ejercicio
```
03_segmentacion_umbral_contornos/
├── python/
│   ├── segmentacion_contornos.py    # Script principal
│   └── requirements.txt             # Dependencias
├── assets/
│   └── sample_image.jpg            # Imagen de prueba
├── resultados/                     # Resultados generados
└── README.md                       # Este archivo
```

## Instalación y Ejecución

### Requisitos
```bash
pip install -r python/requirements.txt
```

### Ejecución del Script Principal
```bash
cd python
python segmentacion_contornos.py
```

## Funcionalidades Implementadas

### 1. Métodos de Umbralización
- **Threshold Fijo**: Umbralización binaria simple con valor fijo (127)
- **Adaptativo (Media)**: Se adapta a la iluminación local usando media
- **Adaptativo (Gaussiano)**: Similar al anterior pero con peso gaussiano
- **Otsu**: Encuentra automáticamente el umbral óptimo

### 2. Detección de Contornos
- **findContours**: Detección de contornos externos
- **Aproximación de polígonos**: approxPolyDP para simplificar contornos
- **Clasificación de formas**: Triángulo, cuadrado, círculo basado en vértices

### 3. Análisis Geométrico
- **Área**: cv2.contourArea() para calcular área de cada contorno
- **Perímetro**: cv2.arcLength() para calcular perímetro
- **Centroide**: Cálculo usando momentos (cv2.moments())
- **Caja delimitadora**: cv2.boundingRect() para rectángulo envolvente

### 4. Visualización Avanzada
- **Dibujo de contornos**: Líneas verdes para contornos detectados
- **Centroides**: Puntos azules para centroides
- **Cajas delimitadoras**: Rectángulos rojos para bounding boxes
- **Etiquetas**: Información de forma y área sobre cada objeto

### 5. Generación de Contenido
- **Comparación visual**: Grid 2x3 mostrando todos los métodos
- **GIF animado**: Secuencia mostrando original → segmentado → contornos
- **Análisis cuantitativo**: Métricas comparativas entre métodos

## Resultados Esperados

### Visualización Comparativa
El script genera una imagen con 6 paneles mostrando:
1. **Threshold Fijo** - Con contornos y propiedades
2. **Adaptativo (Media)** - Con contornos y propiedades  
3. **Adaptativo (Gaussiano)** - Con contornos y propiedades
4. **Otsu** - Con contornos y propiedades
5. **Imagen Original** - Para referencia

### GIF Animado
Secuencia animada mostrando:
- Imagen original
- Cada método de umbralización con contornos detectados
- Transición suave entre métodos (1.5 segundos por frame)

### Análisis Cuantitativo
- Número de contornos detectados por método
- Área total y promedio de contornos
- Clasificación automática de formas (triángulo, cuadrado, círculo)
- Comparación de rendimiento entre métodos

## Características Técnicas

### Optimizaciones Implementadas
- Validación de momentos para evitar división por cero
- Filtrado de contornos por área mínima
- Aproximación de polígonos para clasificación de formas
- Manejo de errores en detección de contornos

### Clasificación de Formas
- **Triángulo**: 3 vértices
- **Cuadrado/Rectángulo**: 4 vértices
- **Círculo/Óvalo**: 8+ vértices
- **Polígono**: Otros números de vértices

## Aprendizajes Clave

1. **Diferencias entre métodos de umbralización**:
   - Fijo: Rápido pero no se adapta a iluminación
   - Adaptativo: Mejor para imágenes con variaciones de luz
   - Otsu: Automático pero puede fallar con iluminación compleja

2. **Detección de contornos**:
   - RETR_EXTERNAL: Solo contornos externos
   - CHAIN_APPROX_SIMPLE: Compresión de puntos redundantes
   - Aproximación de polígonos: Simplificación para clasificación

3. **Análisis geométrico**:
   - Momentos: Cálculo preciso de centroides
   - Área vs perímetro: Relación para clasificación de formas
   - Bounding boxes: Información espacial adicional

## Mejoras Futuras
- Implementación de watershed para segmentación avanzada
- Clasificación de formas más sofisticada (Hu moments)
- Filtrado de contornos por forma y tamaño
- Integración con machine learning para clasificación
- Análisis de texturas dentro de contornos
