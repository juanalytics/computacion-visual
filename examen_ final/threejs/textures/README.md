# Texturas

Las texturas utilizadas en este proyecto se generan **programáticamente** en el código JavaScript (`main.js`), por lo que no se requieren archivos de textura externos.

## Texturas Implementadas

1. **Textura de Cuadrícula** (`createGridTexture()`):
   - Patrón de cuadrícula azul sobre fondo oscuro
   - Aplicada al plano del piso
   - Se repite 4x4 veces

2. **Textura de Círculos Concéntricos** (`createCircleTexture()`):
   - Gradiente radial con círculos concéntricos blancos
   - Colores: rojo → turquesa → azul
   - Aplicada a todas las formas geométricas 3D

Estas texturas se generan usando el Canvas API de HTML5, creando patrones visuales atractivos sin necesidad de archivos externos.

