# Ejercicio 4: Imagen = Matriz - Canales, Slicing, Histogramas

## Objetivo
Manipular pixeles y regiones directamente mediante operaciones de matriz, separación de canales, slicing, y análisis de histogramas.

## Conceptos Aplicados
- **Separación de canales** - RGB y HSV individuales
- **Slicing de matrices** - Selección y edición de regiones específicas
- **Operaciones de píxeles** - Edición directa de valores de matriz
- **Histogramas de intensidad** - Análisis estadístico de distribución de colores
- **Brillo y contraste** - Transformaciones lineales de intensidad
- **Operaciones de matriz** - Inversión, rotación, operaciones bitwise

## Estructura del Ejercicio
```
04_imagen_matriz_pixeles/
├── python/
│   ├── imagen_matriz.py        # Script principal
│   └── requirements.txt        # Dependencias
├── assets/
│   └── sample_image.jpg       # Imagen de prueba
├── resultados/                # Resultados generados
└── README.md                  # Este archivo
```

## Instalación y Ejecución

### Requisitos
```bash
pip install -r python/requirements.txt
```

### Ejecución del Script Principal
```bash
cd python
python imagen_matriz.py
```

## Funcionalidades Implementadas

### 1. Separación de Canales
- **RGB**: Separación de canales Rojo, Verde, Azul
- **HSV**: Separación de canales Hue (matiz), Saturación, Valor
- **Visualización individual** de cada canal como imagen en escala de grises

### 2. Operaciones de Slicing
- **Selección de regiones**: `img[y1:y2, x1:x2]` para extraer regiones específicas
- **Edición directa**: Modificar píxeles por coordenadas exactas
- **Copia y pega**: Copiar regiones de una ubicación a otra
- **Aplicación de filtros**: Aplicar operaciones solo a regiones específicas

### 3. Operaciones de Matriz
- **Inversión de colores**: `255 - pixel` (operación elemento a elemento)
- **Escala de grises manual**: Promedio de canales RGB
- **Brillo y contraste**: Transformación lineal `alpha * pixel + beta`
- **Operaciones bitwise**: AND, OR, XOR a nivel de bits
- **Transformaciones geométricas**: Rotación usando matrices de transformación

### 4. Análisis de Histogramas
- **Histograma de escala de grises**: Distribución de intensidades
- **Histogramas RGB**: Distribución por canal de color
- **Histogramas HSV**: Distribución en espacio de color perceptual
- **Comparación antes/después**: Análisis de cambios en distribución

### 5. Operaciones de Región
- **Cambio de color**: Modificar color de regiones específicas
- **Aplicación de máscaras**: Operaciones condicionales por región
- **Filtros locales**: Aplicar efectos solo a áreas seleccionadas
- **Combinación de regiones**: Mezclar contenido de diferentes áreas

## Resultados Esperados

### Visualización Comparativa (4x4 grid)
El script genera una imagen con 16 paneles mostrando:
1. **Original** - Imagen base
2. **Canal Rojo** - Solo componente roja
3. **Canal Verde** - Solo componente verde
4. **Canal Azul** - Solo componente azul
5. **Canal Hue** - Matiz en HSV
6. **Canal Saturación** - Saturación en HSV
7. **Canal Valor** - Valor en HSV
8. **Región Roja** - Región editada en rojo
9. **Copia y Pega** - Región copiada a nueva ubicación
10. **Región con Blur** - Región con filtro aplicado
11. **Región Enmascarada** - Operación con máscara circular
12. **Brillo/Contraste** - Imagen mejorada
13. **Invertido** - Colores invertidos
14. **Gris Manual** - Escala de grises calculada manualmente
15. **Bitwise AND** - Operación bitwise
16. **Rotado 45°** - Rotación geométrica

### Análisis de Histogramas (2x2 grid)
- **Escala de Grises**: Distribución de intensidades
- **Canales RGB**: Comparación de distribuciones de color
- **Canales HSV**: Distribución en espacio perceptual
- **Antes vs Después**: Comparación de histogramas

## Características Técnicas

### Operaciones de Matriz
- **Slicing eficiente**: Acceso directo a regiones de memoria
- **Operaciones vectorizadas**: Aprovechamiento de NumPy para velocidad
- **Máscaras booleanas**: Selección condicional de píxeles
- **Transformaciones geométricas**: Matrices de rotación y traslación

### Análisis Estadístico
- **Cálculo de histogramas**: Distribución de frecuencias de intensidad
- **Estadísticas descriptivas**: Media, desviación estándar, rango
- **Comparación de distribuciones**: Análisis antes/después de operaciones

## Aprendizajes Clave

1. **Manipulación directa de píxeles**:
   - Acceso por coordenadas: `img[y, x]`
   - Slicing de regiones: `img[y1:y2, x1:x2]`
   - Operaciones elemento a elemento

2. **Separación de canales**:
   - RGB: Modelo aditivo de colores
   - HSV: Representación perceptual más intuitiva
   - Cada canal es una matriz 2D independiente

3. **Operaciones de matriz**:
   - Transformaciones lineales: `alpha * pixel + beta`
   - Operaciones bitwise: Manipulación a nivel de bits
   - Transformaciones geométricas: Rotación, escalado, traslación

4. **Análisis de histogramas**:
   - Distribución de intensidades
   - Identificación de características de imagen
   - Comparación cuantitativa de cambios

## Mejoras Futuras
- Implementación de operaciones de convolución personalizadas
- Análisis de texturas usando matrices de co-ocurrencia
- Segmentación basada en histogramas
- Operaciones morfológicas (erosión, dilatación)
- Análisis de gradientes y bordes usando operadores de matriz
