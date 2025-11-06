/**
 * Visualizador 360° - Taller 3 Computación Visual
 * 
 * Implementa:
 * - Esfera invertida para imágenes equirectangulares
 * - Video 360° como textura dinámica
 * - Conmutación entre panoramas/escenas
 * - Controles de cámara (orbit, input, giroscopio)
 */

import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

class Viewer360 {
    constructor() {
        // Configuración inicial
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.controls = null;
        this.sphere = null;
        this.currentTexture = null;
        this.currentVideo = null;
        this.isVideoMode = false;
        this.isGyroEnabled = false;
        this.gyroQuaternion = new THREE.Quaternion();
        
        // Caché de videos por escena
        // Almacena videos cargados para evitar recargarlos
        this.videoCache = {
            // Formato: { sceneKey: { video, texture, videoUrl, isLocal, currentTime, wasPlaying } }
        };
        
        // Caché de imágenes por escena
        // Almacena imágenes cargadas para evitar recargarlas
        this.imageCache = {
            // Formato: { sceneKey: { texture, imageUrl, isLocal, fileName } }
        };
        
        // Escenas disponibles
        // Nota: Las escenas ahora funcionan como contenedores
        // Los usuarios deben cargar sus propias imágenes/videos desde local
        // Las rutas aquí son solo referencias que mostrarán fallback si no existen
        this.scenes = {
            default: {
                image: null, // Se cargará desde archivo local
                video: null  // Se cargará desde archivo local
            },
            scene2: {
                image: null,
                video: null
            },
            scene3: {
                image: null,
                video: null
            }
        };

        this.currentSceneKey = 'default';
        
        this.init();
        this.setupEventListeners();
        this.animate();
    }

    init() {
        // Crear escena
        this.scene = new THREE.Scene();

        // Crear cámara (perspectiva para 360°)
        this.camera = new THREE.PerspectiveCamera(
            75, // FOV
            window.innerWidth / window.innerHeight,
            0.1,
            1000
        );
        this.camera.position.set(0, 0, 0.1);

        // Crear renderer
        this.renderer = new THREE.WebGLRenderer({ antialias: true });
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setPixelRatio(window.devicePixelRatio);
        document.getElementById('canvas-container').appendChild(this.renderer.domElement);

        // Crear esfera invertida (skybox)
        this.createSphere();

        // Crear controles de órbita
        this.controls = new OrbitControls(this.camera, this.renderer.domElement);
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.05;
        this.controls.enableZoom = true;
        this.controls.minDistance = 0.1;
        this.controls.maxDistance = 2;
        this.controls.rotateSpeed = -0.5; // Invertir para movimiento natural

        // Manejar redimensionamiento
        window.addEventListener('resize', () => this.onWindowResize(), false);

        // Cargar escena inicial
        this.loadScene('default', false);
    }

    createSphere() {
        // Crear geometría de esfera (invertida para skybox)
        const geometry = new THREE.SphereGeometry(500, 60, 40);
        // Invertir las caras para que la textura se vea desde dentro
        geometry.scale(-1, 1, 1);

        // Material inicial (se actualizará con texturas)
        const material = new THREE.MeshBasicMaterial({
            side: THREE.DoubleSide
        });

        this.sphere = new THREE.Mesh(geometry, material);
        this.scene.add(this.sphere);
    }

    async loadScene(sceneKey, isVideoMode = null) {
        const sceneData = this.scenes[sceneKey];
        if (!sceneData) {
            console.error(`Escena ${sceneKey} no encontrada`);
            return;
        }

        // Guardar contenido actual antes de cambiar de escena
        if (this.isVideoMode) {
            this.saveCurrentVideoToCache();
        } else {
            this.saveCurrentImageToCache();
        }

        this.currentSceneKey = sceneKey;
        const shouldUseVideo = isVideoMode !== null ? isVideoMode : this.isVideoMode;

        // Mostrar loading solo si no hay contenido en caché
        const hasCachedContent = (this.videoCache[sceneKey] && shouldUseVideo) || 
                                  (this.imageCache[sceneKey] && !shouldUseVideo);
        if (!hasCachedContent) {
            document.getElementById('loading').style.display = 'block';
        }

        try {
            if (shouldUseVideo) {
                // Verificar si hay video en caché para esta escena
                if (this.videoCache[sceneKey]) {
                    console.log(`Cargando video desde caché para escena ${sceneKey}`);
                    this.restoreVideoFromCache(sceneKey);
                } else if (sceneData.video) {
                    // Solo intentar cargar si hay una ruta definida
                    await this.loadVideo(sceneData.video);
                } else {
                    // No hay video predefinido, mostrar fallback
                    this.createFallbackTexture();
                    document.getElementById('loading').style.display = 'none';
                }
            } else {
                // Verificar si hay imagen en caché para esta escena
                if (this.imageCache[sceneKey]) {
                    console.log(`Cargando imagen desde caché para escena ${sceneKey}`);
                    this.restoreImageFromCache(sceneKey);
                } else if (sceneData.image) {
                    // Solo intentar cargar si hay una ruta definida
                    await this.loadImage(sceneData.image);
                } else {
                    // No hay imagen predefinida, mostrar fallback
                    this.createFallbackTexture();
                    document.getElementById('loading').style.display = 'none';
                }
            }
            this.isVideoMode = shouldUseVideo;
            this.updateUI();
            document.getElementById('loading').style.display = 'none';
        } catch (error) {
            console.error('Error cargando escena:', error);
            document.getElementById('loading').textContent = 'Error cargando escena';
            
            // Crear textura de fallback (gradiente)
            this.createFallbackTexture();
            document.getElementById('loading').style.display = 'none';
        }
    }

    loadImage(imagePath) {
        return new Promise((resolve, reject) => {
            // Detener video si está reproduciéndose
            if (this.currentVideo) {
                this.currentVideo.pause();
                // Revocar URL del objeto si existe
                if (this.currentVideo._objectUrl) {
                    URL.revokeObjectURL(this.currentVideo._objectUrl);
                }
                this.currentVideo.remove();
                this.currentVideo = null;
            }
            
            // Limpiar información de archivo si no es una carga desde caché
            if (!this.imageCache[this.currentSceneKey]) {
                document.getElementById('file-info').textContent = '';
            }

            const loader = new THREE.TextureLoader();
            loader.load(
                imagePath,
                (texture) => {
                    // Configurar textura equirectangular
                    texture.mapping = THREE.EquirectangularReflectionMapping;
                    texture.minFilter = THREE.LinearFilter;
                    texture.magFilter = THREE.LinearFilter;
                    
                    // Liberar textura anterior solo si no está en caché
                    if (this.sphere.material.map) {
                        const isCached = Object.values(this.imageCache).some(c => c.texture === this.sphere.material.map) ||
                                        Object.values(this.videoCache).some(c => c.texture === this.sphere.material.map);
                        if (!isCached) {
                            this.sphere.material.map.dispose();
                        }
                    }
                    
                    this.sphere.material.map = texture;
                    this.sphere.material.needsUpdate = true;
                    this.currentTexture = texture;
                    
                    // Guardar en caché inmediatamente después de cargar
                    this.saveCurrentImageToCache();
                    
                    resolve();
                },
                undefined,
                (error) => {
                    console.warn(`No se pudo cargar ${imagePath}, usando textura de fallback`);
                    this.createFallbackTexture();
                    resolve();
                }
            );
        });
    }

    saveCurrentImageToCache() {
        // Guardar la imagen actual en caché antes de cambiar de escena
        if (this.currentTexture && !this.isVideoMode && this.currentSceneKey && !this.currentVideo) {
            const fileInfoText = document.getElementById('file-info').textContent;
            const hasLocalFile = fileInfoText.includes('✓');
            
            this.imageCache[this.currentSceneKey] = {
                texture: this.currentTexture,
                imageUrl: null, // Para imágenes locales, se maneja diferente
                isLocal: hasLocalFile,
                fileName: hasLocalFile ? fileInfoText : null
            };
            
            console.log(`Imagen guardada en caché para escena ${this.currentSceneKey}`, {
                isLocal: hasLocalFile,
                fileName: hasLocalFile ? fileInfoText : 'imagen predefinida'
            });
        }
    }

    restoreImageFromCache(sceneKey) {
        const cached = this.imageCache[sceneKey];
        if (!cached) {
            console.warn(`No hay imagen en caché para escena ${sceneKey}`);
            return;
        }

        // Detener video si está reproduciéndose
        if (this.currentVideo) {
            this.currentVideo.pause();
            this.currentVideo = null;
        }

        // Restaurar imagen desde caché
        this.currentTexture = cached.texture;
        
        // Aplicar textura a la esfera
        if (this.sphere.material.map !== cached.texture) {
            if (this.sphere.material.map) {
                // No disponer la textura si está en caché
                const isCached = Object.values(this.imageCache).some(c => c.texture === this.sphere.material.map) ||
                                Object.values(this.videoCache).some(c => c.texture === this.sphere.material.map);
                if (!isCached) {
                    this.sphere.material.map.dispose();
                }
            }
            this.sphere.material.map = cached.texture;
            this.sphere.material.needsUpdate = true;
        }

        // Actualizar información de archivo si era local
        if (cached.fileName) {
            document.getElementById('file-info').textContent = cached.fileName;
        } else {
            document.getElementById('file-info').textContent = '';
        }
        
        console.log(`Imagen restaurada desde caché para escena ${sceneKey}`, {
            isLocal: cached.isLocal
        });
    }

    saveCurrentVideoToCache() {
        // Guardar el video actual en caché antes de cambiar de escena
        if (this.currentVideo && this.isVideoMode && this.currentSceneKey) {
            const wasPlaying = !this.currentVideo.paused;
            const currentTime = this.currentVideo.currentTime;
            
            this.videoCache[this.currentSceneKey] = {
                video: this.currentVideo,
                texture: this.currentTexture,
                videoUrl: this.currentVideo._objectUrl || this.currentVideo.src,
                isLocal: !!this.currentVideo._objectUrl,
                currentTime: currentTime,
                wasPlaying: wasPlaying,
                fileName: document.getElementById('file-info').textContent.includes('✓') 
                    ? document.getElementById('file-info').textContent 
                    : null
            };
            
            console.log(`Video guardado en caché para escena ${this.currentSceneKey}`, {
                wasPlaying,
                currentTime: currentTime.toFixed(2)
            });
        }
    }

    restoreVideoFromCache(sceneKey) {
        const cached = this.videoCache[sceneKey];
        if (!cached) {
            console.warn(`No hay video en caché para escena ${sceneKey}`);
            return;
        }

        // Detener video actual si existe
        if (this.currentVideo && this.currentVideo !== cached.video) {
            this.currentVideo.pause();
        }

        // Restaurar video desde caché
        this.currentVideo = cached.video;
        this.currentTexture = cached.texture;
        
        // Aplicar textura a la esfera
        if (this.sphere.material.map !== cached.texture) {
            if (this.sphere.material.map) {
                // No disponer la textura si está en caché
            }
            this.sphere.material.map = cached.texture;
            this.sphere.material.needsUpdate = true;
        }

        // Restaurar tiempo de reproducción
        this.currentVideo.currentTime = cached.currentTime;

        // Actualizar información de archivo si era local
        if (cached.fileName) {
            document.getElementById('file-info').textContent = cached.fileName;
        } else {
            document.getElementById('file-info').textContent = '';
        }

        // Restaurar estado de reproducción
        if (cached.wasPlaying) {
            this.playVideo();
        } else {
            this.currentVideo.pause();
            document.getElementById('play-pause').textContent = '▶ Play';
        }

        // Actualizar textura
        cached.texture.needsUpdate = true;
        
        console.log(`Video restaurado desde caché para escena ${sceneKey}`, {
            currentTime: cached.currentTime.toFixed(2),
            wasPlaying: cached.wasPlaying
        });
    }

    loadVideo(videoPath) {
        return new Promise((resolve, reject) => {
            // Detener video anterior si existe (pero no si está en caché)
            if (this.currentVideo) {
                // Solo pausar si no es el video que vamos a cargar
                this.currentVideo.pause();
            }
            
            // Limpiar información de archivo si no es una carga desde caché
            if (!this.videoCache[this.currentSceneKey]) {
                document.getElementById('file-info').textContent = '';
            }

            const video = document.createElement('video');
            video.src = videoPath;
            video.crossOrigin = 'anonymous';
            video.loop = true;
            video.muted = false;
            video.autoplay = false;
            video.playsInline = true;

            video.addEventListener('loadeddata', () => {
                const texture = new THREE.VideoTexture(video);
                texture.mapping = THREE.EquirectangularReflectionMapping;
                texture.minFilter = THREE.LinearFilter;
                texture.magFilter = THREE.LinearFilter;

                if (this.sphere.material.map && this.sphere.material.map !== this.currentTexture) {
                    // No disponer si está en caché
                    const isCached = Object.values(this.videoCache).some(c => c.texture === this.sphere.material.map);
                    if (!isCached) {
                        this.sphere.material.map.dispose();
                    }
                }

                this.sphere.material.map = texture;
                this.sphere.material.needsUpdate = true;
                this.currentTexture = texture;
                this.currentVideo = video;
                
                // Actualizar textura en cada frame
                texture.needsUpdate = true;
                
                // Guardar en caché inmediatamente después de cargar
                this.saveCurrentVideoToCache();
                
                // Intentar reproducir automáticamente
                this.playVideo();
                
                resolve();
            });

            video.addEventListener('error', (e) => {
                console.warn(`No se pudo cargar video ${videoPath}, usando textura de fallback`);
                this.createFallbackTexture();
                resolve();
            });

            // Intentar cargar
            video.load();
        });
    }

    loadImageFromFile(file) {
        // Guardar imagen actual en caché antes de cargar una nueva
        this.saveCurrentImageToCache();

        // Mostrar loading
        document.getElementById('loading').style.display = 'block';
        document.getElementById('file-info').textContent = `Cargando: ${file.name}`;

        // Detener video si está reproduciéndose
        if (this.currentVideo) {
            this.currentVideo.pause();
            // Revocar URL del objeto si existe
            if (this.currentVideo._objectUrl) {
                URL.revokeObjectURL(this.currentVideo._objectUrl);
            }
            this.currentVideo.remove();
            this.currentVideo = null;
        }

        // Verificar si ya hay una imagen cargada para esta escena
        if (this.imageCache[this.currentSceneKey] && this.imageCache[this.currentSceneKey].isLocal) {
            const cached = this.imageCache[this.currentSceneKey];
            // Si ya hay una imagen local para esta escena, podría ser la misma o diferente
            // Por ahora, siempre cargamos la nueva para permitir reemplazar
            // Pero primero verificamos si es realmente la misma comparando el nombre
            const fileInfoText = document.getElementById('file-info').textContent;
            if (cached.fileName && cached.fileName.includes(file.name)) {
                // Es la misma imagen, restaurarla desde caché
                console.log('Restaurando imagen local desde caché');
                this.restoreImageFromCache(this.currentSceneKey);
                document.getElementById('loading').style.display = 'none';
                return;
            }
        }

        // Crear URL del objeto para la imagen
        const imageUrl = URL.createObjectURL(file);
        
        const loader = new THREE.TextureLoader();
        loader.load(
            imageUrl,
            (texture) => {
                // Configurar textura equirectangular
                texture.mapping = THREE.EquirectangularReflectionMapping;
                texture.minFilter = THREE.LinearFilter;
                texture.magFilter = THREE.LinearFilter;
                
                // Liberar textura anterior solo si no está en caché
                if (this.sphere.material.map) {
                    const isCached = Object.values(this.imageCache).some(c => c.texture === this.sphere.material.map) ||
                                    Object.values(this.videoCache).some(c => c.texture === this.sphere.material.map);
                    if (!isCached) {
                        this.sphere.material.map.dispose();
                    }
                }
                
                this.sphere.material.map = texture;
                this.sphere.material.needsUpdate = true;
                this.currentTexture = texture;
                
                // Actualizar UI
                this.isVideoMode = false;
                this.updateUI();
                document.getElementById('loading').style.display = 'none';
                const fileInfo = `✓ Imagen cargada: ${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)`;
                document.getElementById('file-info').textContent = fileInfo;
                
                // Guardar en caché inmediatamente después de cargar
                this.saveCurrentImageToCache();
                
                // Liberar URL del objeto después de cargar (la textura ya la tiene cargada)
                // Nota: Para imágenes, la textura ya carga los datos, así que podemos revocar
                URL.revokeObjectURL(imageUrl);
            },
            undefined,
            (error) => {
                console.error('Error cargando imagen:', error);
                document.getElementById('loading').textContent = 'Error cargando imagen';
                document.getElementById('file-info').textContent = `✗ Error al cargar: ${file.name}`;
                this.createFallbackTexture();
                document.getElementById('loading').style.display = 'none';
                URL.revokeObjectURL(imageUrl);
            }
        );
    }

    loadVideoFromFile(file) {
        // Guardar video actual en caché antes de cargar uno nuevo
        this.saveCurrentVideoToCache();

        // Mostrar loading
        document.getElementById('loading').style.display = 'block';
        document.getElementById('file-info').textContent = `Cargando: ${file.name}`;

        // Detener video anterior si existe (pero no remover si está en caché)
        if (this.currentVideo) {
            this.currentVideo.pause();
            // Solo remover si no está guardado en caché
            const isCached = Object.values(this.videoCache).some(c => c.video === this.currentVideo);
            if (!isCached) {
                if (this.currentVideo._objectUrl) {
                    URL.revokeObjectURL(this.currentVideo._objectUrl);
                }
                this.currentVideo.remove();
            }
        }

        // Si ya hay un video local en caché para esta escena, limpiarlo primero
        // (esto permite reemplazar el video anterior con uno nuevo)
        if (this.videoCache[this.currentSceneKey] && this.videoCache[this.currentSceneKey].isLocal) {
            const oldCached = this.videoCache[this.currentSceneKey];
            // Solo limpiar si es diferente al video actual
            if (oldCached.video !== this.currentVideo && oldCached.video._objectUrl) {
                URL.revokeObjectURL(oldCached.video._objectUrl);
                oldCached.video.remove();
            }
        }

        // Crear URL del objeto para el video
        const videoUrl = URL.createObjectURL(file);

        const video = document.createElement('video');
        video.src = videoUrl;
        video.crossOrigin = 'anonymous';
        video.loop = true;
        video.muted = false;
        video.autoplay = false;
        video.playsInline = true;
        
        // Almacenar la URL para poder revocarla después
        video._objectUrl = videoUrl;

        video.addEventListener('loadeddata', () => {
            const texture = new THREE.VideoTexture(video);
            texture.mapping = THREE.EquirectangularReflectionMapping;
            texture.minFilter = THREE.LinearFilter;
            texture.magFilter = THREE.LinearFilter;

            // Liberar textura anterior solo si no está en caché
            if (this.sphere.material.map) {
                const isCached = Object.values(this.videoCache).some(c => c.texture === this.sphere.material.map);
                if (!isCached) {
                    this.sphere.material.map.dispose();
                }
            }

            this.sphere.material.map = texture;
            this.sphere.material.needsUpdate = true;
            this.currentTexture = texture;
            this.currentVideo = video;
            
            // Actualizar textura en cada frame
            texture.needsUpdate = true;
            
            // Actualizar UI
            this.isVideoMode = true;
            this.updateUI();
            document.getElementById('loading').style.display = 'none';
            const fileInfo = `✓ Video cargado: ${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)`;
            document.getElementById('file-info').textContent = fileInfo;
            
            // Guardar en caché inmediatamente después de cargar
            this.saveCurrentVideoToCache();
            
            // Intentar reproducir automáticamente
            this.playVideo();
        });

        video.addEventListener('error', (e) => {
            console.error('Error cargando video:', e);
            document.getElementById('loading').textContent = 'Error cargando video';
            document.getElementById('file-info').textContent = `✗ Error al cargar: ${file.name}`;
            this.createFallbackTexture();
            document.getElementById('loading').style.display = 'none';
            URL.revokeObjectURL(videoUrl);
        });
        
        // Intentar cargar
        video.load();
    }

    createFallbackTexture() {
        // Crear textura procedural de fallback
        const canvas = document.createElement('canvas');
        canvas.width = 2048;
        canvas.height = 1024;
        const ctx = canvas.getContext('2d');

        // Gradiente circular
        const gradient = ctx.createRadialGradient(
            canvas.width / 2, canvas.height / 2, 0,
            canvas.width / 2, canvas.height / 2, canvas.width / 2
        );
        gradient.addColorStop(0, '#4CAF50');
        gradient.addColorStop(0.5, '#2196F3');
        gradient.addColorStop(1, '#1a1a1a');

        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Agregar texto
        ctx.fillStyle = 'white';
        ctx.font = '48px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('360° Viewer', canvas.width / 2, canvas.height / 2 - 50);
        ctx.fillText('Carga una imagen equirectangular', canvas.width / 2, canvas.height / 2 + 50);

        const texture = new THREE.CanvasTexture(canvas);
        texture.mapping = THREE.EquirectangularReflectionMapping;
        
        if (this.sphere.material.map) {
            this.sphere.material.map.dispose();
        }
        
        this.sphere.material.map = texture;
        this.sphere.material.needsUpdate = true;
        this.currentTexture = texture;
    }

    setupEventListeners() {
        // Toggle modo imagen/video
        document.getElementById('toggle-mode').addEventListener('click', () => {
            // Si hay un archivo local cargado, no cambiar a escenas predefinidas
            const hasLocalFile = document.getElementById('file-info').textContent.includes('✓');
            if (hasLocalFile && this.isVideoMode) {
                // Si ya estamos en modo video con archivo local, cambiar a imagen desde escena
                this.isVideoMode = false;
                this.loadScene(this.currentSceneKey, false);
            } else if (hasLocalFile && !this.isVideoMode) {
                // Si estamos en modo imagen con archivo local, cambiar a video desde escena
                this.isVideoMode = true;
                this.loadScene(this.currentSceneKey, true);
            } else {
                // Cambiar entre modo imagen/video de escenas predefinidas
                this.isVideoMode = !this.isVideoMode;
                this.loadScene(this.currentSceneKey, this.isVideoMode);
            }
        });

        // Selector de escena
        document.getElementById('scene-selector').addEventListener('change', (e) => {
            // Guardar video actual antes de cambiar (si está en modo video)
            // No limpiar file-info porque se restaurará si hay caché
            // Cargar la escena manteniendo el modo actual (video o imagen)
            this.loadScene(e.target.value, null);
        });

        // Reset cámara
        document.getElementById('reset-camera').addEventListener('click', () => {
            this.resetCamera();
        });

        // Toggle giroscopio
        document.getElementById('toggle-gyro').addEventListener('click', () => {
            this.toggleGyroscope();
        });

        // Controles de video
        document.getElementById('play-pause').addEventListener('click', () => {
            this.togglePlayPause();
        });

        document.getElementById('mute-unmute').addEventListener('click', () => {
            this.toggleMute();
        });

        // Cargar archivos desde local
        const fileInputImage = document.getElementById('file-input-image');
        const fileInputVideo = document.getElementById('file-input-video');
        const loadImageBtn = document.getElementById('load-image-btn');
        const loadVideoBtn = document.getElementById('load-video-btn');

        loadImageBtn.addEventListener('click', () => {
            fileInputImage.click();
        });

        loadVideoBtn.addEventListener('click', () => {
            fileInputVideo.click();
        });

        fileInputImage.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                this.loadImageFromFile(file);
            }
        });

        fileInputVideo.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                this.loadVideoFromFile(file);
            }
        });

        // Controles de teclado
        document.addEventListener('keydown', (e) => this.handleKeyDown(e));
    }

    resetCamera() {
        this.camera.position.set(0, 0, 0.1);
        this.controls.reset();
        this.gyroQuaternion.set(0, 0, 0, 1);
    }

    async toggleGyroscope() {
        if (!this.isGyroEnabled) {
            if (typeof DeviceOrientationEvent !== 'undefined' && 
                typeof DeviceOrientationEvent.requestPermission === 'function') {
                // iOS 13+ requiere permiso
                const permission = await DeviceOrientationEvent.requestPermission();
                if (permission !== 'granted') {
                    alert('Permiso de orientación denegado');
                    return;
                }
            }

            window.addEventListener('deviceorientation', (e) => this.handleDeviceOrientation(e));
            this.isGyroEnabled = true;
            document.getElementById('toggle-gyro').textContent = 'Giroscopio: ON';
        } else {
            window.removeEventListener('deviceorientation', this.handleDeviceOrientation);
            this.isGyroEnabled = false;
            document.getElementById('toggle-gyro').textContent = 'Giroscopio: OFF';
        }
    }

    handleDeviceOrientation(event) {
        if (!this.isGyroEnabled) return;

        // Convertir orientación del dispositivo a quaternion
        const euler = new THREE.Euler(
            THREE.MathUtils.degToRad(event.beta || 0),   // pitch
            THREE.MathUtils.degToRad(event.alpha || 0),  // yaw
            -THREE.MathUtils.degToRad(event.gamma || 0), // roll
            'YXZ'
        );

        this.gyroQuaternion.setFromEuler(euler);
        
        // Aplicar rotación a la cámara
        this.camera.quaternion.copy(this.gyroQuaternion);
        this.controls.update();
    }

    playVideo() {
        // Intentar reproducir el video automáticamente
        if (this.currentVideo) {
            const playPromise = this.currentVideo.play();
            
            // Manejar promesa de play (puede fallar por políticas del navegador)
            if (playPromise !== undefined) {
                playPromise
                    .then(() => {
                        // Reproducción iniciada exitosamente
                        document.getElementById('play-pause').textContent = '⏸ Pause';
                    })
                    .catch(error => {
                        // Error al reproducir (normalmente requiere interacción del usuario)
                        console.log('El video requiere interacción del usuario para reproducir:', error);
                        document.getElementById('play-pause').textContent = '▶ Play';
                    });
            }
        }
    }

    togglePlayPause() {
        if (this.currentVideo) {
            if (this.currentVideo.paused) {
                this.currentVideo.play().then(() => {
                    document.getElementById('play-pause').textContent = '⏸ Pause';
                }).catch(error => {
                    console.log('Error al reproducir:', error);
                });
            } else {
                this.currentVideo.pause();
                document.getElementById('play-pause').textContent = '▶ Play';
            }
        }
    }

    toggleMute() {
        if (this.currentVideo) {
            this.currentVideo.muted = !this.currentVideo.muted;
            document.getElementById('mute-unmute').textContent = 
                this.currentVideo.muted ? '🔇 Silenciado' : '🔊 Sonido';
        }
    }

    handleKeyDown(event) {
        const moveSpeed = 0.01;
        const rotationSpeed = 0.02;

        switch(event.key.toLowerCase()) {
            case 'w':
            case 'arrowup':
                // Rotar hacia arriba
                this.camera.rotation.x -= rotationSpeed;
                break;
            case 's':
            case 'arrowdown':
                // Rotar hacia abajo
                this.camera.rotation.x += rotationSpeed;
                break;
            case 'a':
            case 'arrowleft':
                // Rotar izquierda
                this.camera.rotation.y += rotationSpeed;
                break;
            case 'd':
            case 'arrowright':
                // Rotar derecha
                this.camera.rotation.y -= rotationSpeed;
                break;
            case 'r':
                // Reset cámara
                this.resetCamera();
                break;
            case ' ':
                // Play/Pause video
                event.preventDefault();
                this.togglePlayPause();
                break;
        }
        this.controls.update();
    }

    updateUI() {
        // Actualizar botón de modo
        const modeButton = document.getElementById('toggle-mode');
        modeButton.textContent = this.isVideoMode ? 'Video' : 'Imagen';
        modeButton.className = this.isVideoMode ? 'active' : '';

        // Mostrar/ocultar controles de video
        const videoControls = document.getElementById('play-pause').parentElement;
        videoControls.style.display = this.isVideoMode ? 'block' : 'none';
        
        // Actualizar estado del botón play/pause si hay video
        if (this.isVideoMode && this.currentVideo) {
            document.getElementById('play-pause').textContent = 
                this.currentVideo.paused ? '▶ Play' : '⏸ Pause';
        }
    }

    onWindowResize() {
        this.camera.aspect = window.innerWidth / window.innerHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(window.innerWidth, window.innerHeight);
    }

    animate() {
        requestAnimationFrame(() => this.animate());

        // Actualizar controles
        this.controls.update();

        // Actualizar textura de video si está activo
        if (this.currentVideo && this.currentTexture) {
            this.currentTexture.needsUpdate = true;
        }

        // Renderizar
        this.renderer.render(this.scene, this.camera);
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    new Viewer360();
});

