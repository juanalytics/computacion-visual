# Processing - Transformaciones 3D

## Instalación

1. Descargar e instalar [Processing](https://processing.org/download/)
2. Abrir el archivo `transformaciones_3d.pde` en Processing IDE

## Ejecución

1. Abrir Processing IDE
2. Cargar el sketch `transformaciones_3d.pde`
3. Presionar el botón "Play" o usar Ctrl+R

## Descripción

Este sketch implementa transformaciones geométricas básicas en 3D usando Processing:

### Transformaciones Implementadas

1. **Cubo Rojo - Traslación Senoidal**
   - Movimiento suave en trayectoria senoidal
   - Usa `sin()` y `cos()` para diferentes ejes

2. **Esfera Verde - Rotación Continua**
   - Rotación simultánea en X, Y, Z
   - Marcador rojo para visualizar la rotación

3. **Cilindro Azul - Escala Oscilante**
   - Cambio de tamaño usando función senoidal
   - Cilindro construido con `beginShape()/endShape()`

4. **Torus Amarillo - Transformación Compuesta**
   - Traslación circular + rotación + escala
   - Torus aproximado con múltiples cajas

### Características Técnicas

- **pushMatrix()/popMatrix()**: Aislamiento de transformaciones
- **Iluminación 3D**: Luz ambiental, direccional y puntual
- **Sistema de coordenadas**: Ejes X, Y, Z visibles
- **Grid de referencia**: Plano XZ con líneas guía
- **HUD informativo**: Información en tiempo real

### Controles Interactivos

- **Mouse + arrastrar**: Rotar cámara (ángulos X e Y)
- **Rueda del mouse**: Zoom in/out
- **Tecla 'R'**: Reiniciar animación y cámara
- **Tecla 'S'**: Guardar captura de pantalla
- **Barra espaciadora**: Pausar/reanudar animación

### Funciones Clave de Processing

- `translate()`: Traslación de objetos
- `rotate()`: Rotación en ejes específicos
- `scale()`: Escalado uniforme o no uniforme
- `frameCount` y tiempo personalizado para animaciones
- `P3D`: Renderer 3D de Processing
