# Unity - Transformaciones 3D con C#

## Instalación

1. Descargar e instalar [Unity Hub](https://unity3d.com/get-unity/download)
2. Instalar Unity LTS (recomendado: 2022.3 LTS o superior)
3. Crear nuevo proyecto 3D
4. Importar los scripts `TransformacionesBasicas.cs` y `ControladorEscena.cs`

## Configuración del Proyecto

### Escena Básica
1. Crear una escena vacía
2. Agregar un plano como suelo
3. Configurar iluminación básica (Directional Light)
4. Agregar el script `ControladorEscena.cs` a un GameObject vacío

### Scripts Incluidos

#### `TransformacionesBasicas.cs`
Script principal que aplica transformaciones a GameObjects individuales:

- **Traslación**: Movimiento senoidal o lineal
- **Rotación**: Rotación continua en ejes seleccionables
- **Escala**: Escalado oscilante
- **Compuesta**: Combinación de todas las transformaciones

#### `ControladorEscena.cs`
Controlador que maneja múltiples objetos con diferentes transformaciones:

- Crea automáticamente 4 objetos primitivos
- Asigna diferentes tipos de transformación a cada uno
- Proporciona controles globales

## Uso

### Configuración Manual
1. Crear un GameObject (Cubo, Esfera, etc.)
2. Agregar el componente `TransformacionesBasicas`
3. Configurar parámetros en el Inspector:
   - **Tipo de Transformación**: Traslación, Rotación, Escala, Compuesta
   - **Velocidades**: Controlan la rapidez de cada transformación
   - **Amplitud**: Controla la intensidad del movimiento
   - **Ejes**: Seleccionar en qué ejes aplicar las transformaciones

### Configuración Automática
1. Agregar `ControladorEscena.cs` a un GameObject vacío
2. El script creará automáticamente los objetos de demostración

## Controles

### En Tiempo de Ejecución
- **Tecla 'R'**: Reiniciar todas las transformaciones
- **Barra espaciadora**: Pausar/reanudar animaciones
- **UI Slider**: Controlar velocidad global (si está configurado)

### Inspector de Unity
- Todos los parámetros son editables en tiempo real
- Cambios se aplican inmediatamente durante Play Mode

## Características Técnicas

### Transformaciones Utilizadas
- `transform.Translate()`: Para traslación relativa
- `transform.Rotate()`: Para rotación incremental
- `transform.position`: Para posición absoluta
- `transform.localScale`: Para escalado
- `Time.deltaTime`: Para animaciones independientes del framerate

### Funciones Matemáticas
- `Mathf.Sin()` y `Mathf.Cos()`: Movimientos suaves y circulares
- `Mathf.PingPong()`: Movimientos lineales alternativos
- `Time.time`: Tiempo global para sincronización

### Optimizaciones
- Uso eficiente de `Time.deltaTime`
- Caching de valores iniciales
- Gizmos para debug visual
- Controles de UI opcionales

## Estructura de Archivos

```
unity/
├── TransformacionesBasicas.cs    # Script principal de transformaciones
├── ControladorEscena.cs          # Controlador de múltiples objetos
└── README.md                     # Esta documentación
```

## Extensiones Posibles

- Agregar más tipos de transformaciones
- Implementar curvas de animación personalizadas
- Añadir efectos de partículas
- Crear sistema de waypoints para trayectorias complejas
