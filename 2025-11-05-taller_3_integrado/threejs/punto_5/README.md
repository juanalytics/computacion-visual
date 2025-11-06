# Visualizador 360° - Punto 5 del Taller

## Descripción

Implementación completa de un visualizador 360° que cumple con todos los requisitos del punto 5 del taller:

- ✅ **Esfera invertida o skybox para equirectangulares**: Esfera con geometría invertida para visualizar imágenes panorámicas desde el interior
- ✅ **Video 360° como textura dinámica**: Soporte para video 360° que se actualiza en tiempo real
- ✅ **Conmutación entre panoramas/escenas**: Cambio dinámico entre diferentes escenas 360°
- ✅ **Controles de cámara**: Orbit controls, input por teclado, y soporte para giroscopio en dispositivos móviles

## Características

### Visualización
- Esfera invertida con textura equirectangular
- Soporte para imágenes estáticas (JPG, PNG)
- Soporte para video 360° (MP4, WebM)
- Textura procedural de fallback si no se encuentran archivos

### Controles de Cámara
- **Orbit Controls**: Arrastrar con mouse para rotar la vista
- **Zoom**: Rueda del mouse para acercar/alejar
- **Teclado**: Flechas o WASD para navegar
- **Giroscopio**: Soporte para dispositivos móviles (requiere permiso)

### Interfaz
- Panel de controles flotante
- **Carga de archivos locales**: Botones para cargar imágenes y videos 360° desde el sistema de archivos
- Selector de escenas
- Toggle entre modo imagen y video
- Controles de reproducción de video (play/pause, mute)
- Reset de cámara
- Activar/desactivar giroscopio
- Información del archivo cargado (nombre y tamaño)

## Estructura de Archivos

```
threejs/punto_5/
├── index.html          # Interfaz principal
├── viewer.js           # Lógica del visualizador
├── README.md           # Esta documentación
├── INSTRUCCIONES.md    # Guía rápida
└── package.json        # Configuración del proyecto
```

**Nota**: Las imágenes y videos se cargan desde archivos locales usando los botones de carga. No se requieren carpetas de medios predefinidas.

## Requisitos

- Navegador moderno con soporte WebGL
- Servidor web local (para cargar archivos CORS)
- Imágenes/videos 360° en formato equirectangular (se cargan desde archivos locales)

## Instalación y Uso

### Opción 1: Servidor HTTP Simple (Python)

```bash
# Python 3 - Ejecutar desde la raíz del proyecto
python -m http.server 8000

# Abrir en navegador: http://localhost:8000/threejs/punto_5/
```

### Opción 2: Servidor HTTP Simple (Node.js)

```bash
# Instalar http-server globalmente (opcional)
npm install -g http-server

# Ejecutar desde la raíz del proyecto
npx http-server -p 8000

# Abrir en navegador: http://localhost:8000/threejs/punto_5/
```

### Opción 3: VS Code Live Server

1. Instalar extensión "Live Server" en VS Code
2. Navegar a `threejs/punto_5/index.html`
3. Click derecho → "Open with Live Server"

## Formato de Imágenes y Videos

### Imágenes 360°
- **Formato**: Equirectangular (proyección cilíndrica)
- **Relación de aspecto**: 2:1 (por ejemplo, 4096x2048, 2048x1024)
- **Formatos soportados**: JPG, PNG
- **Ejemplo**: Una foto tomada con una cámara 360° o renderizada desde un software 3D

### Videos 360°
- **Formato**: Equirectangular
- **Relación de aspecto**: 2:1
- **Formatos soportados**: MP4, WebM
- **Codec recomendado**: H.264 para máxima compatibilidad

### Dónde obtener contenido 360°

1. **Cámaras 360°**: Insta360, GoPro Max, Ricoh Theta
2. **Renderizado 3D**: Blender, Unity, Unreal Engine con formato equirectangular
3. **Stock gratuito**: 
   - [Poly Haven](https://polyhaven.com/hdris)
   - [HDRI Haven](https://hdrihaven.com/)
   - [Flickr 360°](https://www.flickr.com/groups/equirectangular/)

**Carga de archivos**: Usa los botones "📷 Cargar Imagen 360°" y "🎥 Cargar Video 360°" para cargar tus archivos directamente desde tu computadora.

## Uso

### Controles Básicos

1. **Arrastrar**: Rotar la vista 360°
2. **Rueda del mouse**: Zoom in/out
3. **Flechas/WASD**: Navegación por teclado
4. **R**: Reset de cámara
5. **Espacio**: Play/Pause video (si está en modo video)

### Cargar Archivos desde Local

**Nueva funcionalidad**: Puedes cargar tus propias imágenes y videos 360° directamente desde tu computadora sin necesidad de colocarlos en las carpetas del proyecto.

1. **Cargar Imagen 360°**:
   - Click en el botón "📷 Cargar Imagen 360°"
   - Selecciona una imagen equirectangular desde tu computadora
   - La imagen se cargará y mostrará automáticamente
   - Se mostrará el nombre del archivo y su tamaño

2. **Cargar Video 360°**:
   - Click en el botón "🎥 Cargar Video 360°"
   - Selecciona un video 360° desde tu computadora
   - El video se cargará y podrás reproducirlo con los controles
   - Se mostrará el nombre del archivo y su tamaño
   - **El video se guarda automáticamente en caché para la escena actual**

**Sistema de Caché de Imágenes y Videos**:
- **Imágenes y videos** se guardan automáticamente en memoria por escena
- Cuando cargas una imagen/video en la Escena 1, luego cambias a la Escena 2 y cargas otro archivo, al regresar a la Escena 1, el archivo anterior se restaurará automáticamente
- Los videos conservan su posición de reproducción y estado (play/pause)
- Las imágenes se restauran instantáneamente sin necesidad de recargarlas
- Esto funciona tanto para archivos cargados desde local como para archivos de escenas predefinidas

**Nota**: Los archivos cargados desde local se cargan en memoria y no se guardan en el servidor. Si recargas la página, deberás volver a cargarlos. Sin embargo, mientras la página esté abierta, las imágenes y videos se mantendrán en caché.

### Cambiar Escena

1. Usar el selector "Escena/Panorama" en el panel de controles
2. Seleccionar entre las escenas disponibles
3. La escena se cargará automáticamente
4. **Sistema de Caché**:
   - Si estabas viendo una imagen o video, se guarda automáticamente en la escena anterior
   - Al regresar a una escena donde cargaste una imagen o video, se restaurará automáticamente
   - Los videos conservan su posición de reproducción y estado (play/pause)
   - Las imágenes se restauran instantáneamente
   - Esto funciona para archivos locales y archivos de escenas predefinidas

### Modo Video

1. **Cambiar a modo video desde escenas predefinidas**:
   - Click en "Modo de Visualización" para cambiar a video
   - El video de la escena actual se cargará automáticamente
   - El video se reproducirá automáticamente en loop (si el navegador lo permite)
   - Si el navegador bloquea la reproducción automática, usa el botón "▶ Play"

2. **Cambiar entre escenas en modo video**:
   - Selecciona una escena diferente en el selector "Escena/Panorama"
   - El video de la nueva escena se cargará y reproducirá automáticamente

3. **Controles de video**:
   - **Play/Pause**: Reproducir o pausar el video
   - **Sonido**: Activar o desactivar el audio
   - Los videos se reproducen en loop automáticamente

4. **Cargar video local**:
   - Usa el botón "🎥 Cargar Video 360°" para cargar un video desde tu computadora
   - El video se reproducirá automáticamente al cargarse

### Giroscopio (Móvil)

1. Click en "Giroscopio: OFF" para activar
2. Dar permiso si el navegador lo solicita
3. Mover el dispositivo para rotar la vista
4. Click nuevamente para desactivar

## Implementación Técnica

### Esfera Invertida

```javascript
// Geometría de esfera invertida
const geometry = new THREE.SphereGeometry(500, 60, 40);
geometry.scale(-1, 1, 1); // Invertir para vista desde dentro

const material = new THREE.MeshBasicMaterial({
    side: THREE.DoubleSide,
    map: texture // Textura equirectangular
});
```

### Video como Textura Dinámica

```javascript
const video = document.createElement('video');
const texture = new THREE.VideoTexture(video);
texture.mapping = THREE.EquirectangularReflectionMapping;

// Actualizar en cada frame
texture.needsUpdate = true;
```

### Orbit Controls

```javascript
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.rotateSpeed = -0.5; // Invertido para movimiento natural
```

### Giroscopio

```javascript
// Manejar orientación del dispositivo
window.addEventListener('deviceorientation', (e) => {
    const euler = new THREE.Euler(
        THREE.MathUtils.degToRad(e.beta),
        THREE.MathUtils.degToRad(e.alpha),
        -THREE.MathUtils.degToRad(e.gamma),
        'YXZ'
    );
    camera.quaternion.setFromEuler(euler);
});
```

### Carga de Archivos Locales

```javascript
// Cargar imagen desde archivo local
loadImageFromFile(file) {
    const imageUrl = URL.createObjectURL(file);
    const loader = new THREE.TextureLoader();
    loader.load(imageUrl, (texture) => {
        texture.mapping = THREE.EquirectangularReflectionMapping;
        this.sphere.material.map = texture;
        URL.revokeObjectURL(imageUrl); // Liberar memoria
    });
}

// Cargar video desde archivo local
loadVideoFromFile(file) {
    const videoUrl = URL.createObjectURL(file);
    const video = document.createElement('video');
    video.src = videoUrl;
    const texture = new THREE.VideoTexture(video);
    texture.mapping = THREE.EquirectangularReflectionMapping;
    this.sphere.material.map = texture;
    // La URL se revoca cuando se carga un nuevo archivo
}
```

## Personalización

### Agregar Nuevas Escenas

Editar `viewer.js` y agregar en el objeto `scenes`:

```javascript
this.scenes = {
    // ... escenas existentes
    nuevaEscena: {
        image: null,  // Se cargará desde archivo local
        video: null   // Se cargará desde archivo local
    }
};
```

Luego agregar la opción en `index.html`:

```html
<option value="nuevaEscena">Nueva Escena</option>
```

**Nota**: Las escenas ahora funcionan como contenedores. Los usuarios cargan sus propios archivos usando los botones de carga. No se requieren archivos predefinidos en carpetas.

### Modificar Configuración

- **FOV de cámara**: Cambiar `75` en `new THREE.PerspectiveCamera(75, ...)`
- **Tamaño de esfera**: Cambiar `500` en `new THREE.SphereGeometry(500, ...)`
- **Velocidad de rotación**: Modificar `rotateSpeed` en OrbitControls

## Solución de Problemas

### No se ven las imágenes/videos
- Verificar que los archivos estén en las rutas correctas
- Usar un servidor HTTP (no abrir directamente el archivo HTML)
- Verificar la consola del navegador para errores CORS

### Giroscopio no funciona
- Verificar que el dispositivo tenga giroscopio
- Dar permisos cuando el navegador lo solicite
- Algunos navegadores requieren HTTPS para giroscopio

### Video no se reproduce
- Verificar formato del video (MP4 H.264 recomendado)
- Verificar que el video tenga audio si se intenta desmutar
- Algunos navegadores requieren interacción del usuario antes de reproducir

## Código Relevante

### Clase Principal
- `Viewer360`: Clase principal que maneja toda la lógica
- `init()`: Inicialización de Three.js
- `createSphere()`: Creación de esfera invertida
- `loadScene()`: Carga de escenas
- `loadImage()` / `loadVideo()`: Carga de medios desde rutas
- `loadImageFromFile()` / `loadVideoFromFile()`: Carga de medios desde archivos locales
- `saveCurrentImageToCache()` / `saveCurrentVideoToCache()`: Guardar contenido en caché
- `restoreImageFromCache()` / `restoreVideoFromCache()`: Restaurar contenido desde caché
- `animate()`: Loop de renderizado

### Funciones Clave
- `handleDeviceOrientation()`: Manejo de giroscopio
- `handleKeyDown()`: Manejo de teclado
- `resetCamera()`: Reset de cámara
- `toggleGyroscope()`: Activar/desactivar giroscopio
- `loadImageFromFile()`: Carga imagen desde File object usando URL.createObjectURL()
- `loadVideoFromFile()`: Carga video desde File object usando URL.createObjectURL()

## Tecnologías Utilizadas

- **Three.js**: Librería 3D para WebGL
- **OrbitControls**: Controles de cámara interactivos
- **WebGL**: Renderizado acelerado por GPU
- **DeviceOrientation API**: Acceso a giroscopio
- **File API**: Lectura de archivos desde el sistema local
- **URL.createObjectURL()**: Creación de URLs temporales para archivos locales

## Referencias

- [Three.js Documentation](https://threejs.org/docs/)
- [Equirectangular Projection](https://en.wikipedia.org/wiki/Equirectangular_projection)
- [WebGL Best Practices](https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/WebGL_best_practices)
- [DeviceOrientation API](https://developer.mozilla.org/en-US/docs/Web/API/DeviceOrientationEvent)

## Autor

Implementado para el Taller Integral de Computación Visual - Punto 5

