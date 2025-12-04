import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// ============================================
// CONFIGURACIÓN DE ESCENA
// ============================================

// Escena
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x1a1a2e);

// Cámara
const camera = new THREE.PerspectiveCamera(
    75, // FOV
    window.innerWidth / window.innerHeight,
    0.1,
    1000
);

// Renderizador
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
document.getElementById('canvas-container').appendChild(renderer.domElement);

// OrbitControls
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.minDistance = 5;
controls.maxDistance = 50;

// ============================================
// CREACIÓN DE TEXTURAS PROGRAMÁTICAS
// ============================================

// Textura 1: Patrón de cuadrícula (para el piso)
function createGridTexture() {
    const canvas = document.createElement('canvas');
    canvas.width = 256;
    canvas.height = 256;
    const ctx = canvas.getContext('2d');
    
    // Fondo oscuro
    ctx.fillStyle = '#2a2a3e';
    ctx.fillRect(0, 0, 256, 256);
    
    // Líneas de cuadrícula
    ctx.strokeStyle = '#4fc3f7';
    ctx.lineWidth = 2;
    
    for (let i = 0; i <= 256; i += 32) {
        ctx.beginPath();
        ctx.moveTo(i, 0);
        ctx.lineTo(i, 256);
        ctx.stroke();
        
        ctx.beginPath();
        ctx.moveTo(0, i);
        ctx.lineTo(256, i);
        ctx.stroke();
    }
    
    const texture = new THREE.CanvasTexture(canvas);
    texture.wrapS = THREE.RepeatWrapping;
    texture.wrapT = THREE.RepeatWrapping;
    texture.repeat.set(4, 4);
    return texture;
}

// Textura 2: Patrón de círculos concéntricos (para objetos)
function createCircleTexture() {
    const canvas = document.createElement('canvas');
    canvas.width = 256;
    canvas.height = 256;
    const ctx = canvas.getContext('2d');
    
    // Fondo
    const gradient = ctx.createRadialGradient(128, 128, 0, 128, 128, 128);
    gradient.addColorStop(0, '#ff6b6b');
    gradient.addColorStop(0.5, '#4ecdc4');
    gradient.addColorStop(1, '#45b7d1');
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, 256, 256);
    
    // Círculos concéntricos
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 3;
    for (let r = 20; r < 128; r += 20) {
        ctx.beginPath();
        ctx.arc(128, 128, r, 0, Math.PI * 2);
        ctx.stroke();
    }
    
    const texture = new THREE.CanvasTexture(canvas);
    texture.wrapS = THREE.RepeatWrapping;
    texture.wrapT = THREE.RepeatWrapping;
    return texture;
}

const gridTexture = createGridTexture();
const circleTexture = createCircleTexture();

// ============================================
// CREACIÓN DE FORMAS GEOMÉTRICAS
// ============================================

const shapes = [];

// Plano del piso
const planeGeometry = new THREE.PlaneGeometry(20, 20);
const planeMaterial = new THREE.MeshStandardMaterial({
    map: gridTexture,
    roughness: 0.8,
    metalness: 0.2
});
const plane = new THREE.Mesh(planeGeometry, planeMaterial);
plane.rotation.x = -Math.PI / 2;
plane.position.y = -2;
plane.receiveShadow = true;
scene.add(plane);
shapes.push(plane);

// Cubo
const cubeGeometry = new THREE.BoxGeometry(2, 2, 2);
const cubeMaterial = new THREE.MeshStandardMaterial({
    map: circleTexture,
    roughness: 0.5,
    metalness: 0.3
});
const cube = new THREE.Mesh(cubeGeometry, cubeMaterial);
cube.position.set(-4, 0, 0);
cube.castShadow = true;
cube.receiveShadow = true;
scene.add(cube);
shapes.push(cube);

// Esfera
const sphereGeometry = new THREE.SphereGeometry(1.5, 32, 32);
const sphereMaterial = new THREE.MeshStandardMaterial({
    map: circleTexture,
    roughness: 0.4,
    metalness: 0.5
});
const sphere = new THREE.Mesh(sphereGeometry, sphereMaterial);
sphere.position.set(0, 0, 0);
sphere.castShadow = true;
sphere.receiveShadow = true;
scene.add(sphere);
shapes.push(sphere);

// Cilindro
const cylinderGeometry = new THREE.CylinderGeometry(1, 1, 3, 32);
const cylinderMaterial = new THREE.MeshStandardMaterial({
    map: circleTexture,
    roughness: 0.6,
    metalness: 0.2
});
const cylinder = new THREE.Mesh(cylinderGeometry, cylinderMaterial);
cylinder.position.set(4, 0.5, 0);
cylinder.castShadow = true;
cylinder.receiveShadow = true;
scene.add(cylinder);
shapes.push(cylinder);

// Cono
const coneGeometry = new THREE.ConeGeometry(1.5, 3, 32);
const coneMaterial = new THREE.MeshStandardMaterial({
    map: circleTexture,
    roughness: 0.5,
    metalness: 0.4
});
const cone = new THREE.Mesh(coneGeometry, coneMaterial);
cone.position.set(-2, 1.5, -3);
cone.castShadow = true;
cone.receiveShadow = true;
scene.add(cone);
shapes.push(cone);

// Torus (dona)
const torusGeometry = new THREE.TorusGeometry(1, 0.5, 16, 100);
const torusMaterial = new THREE.MeshStandardMaterial({
    map: circleTexture,
    roughness: 0.3,
    metalness: 0.7
});
const torus = new THREE.Mesh(torusGeometry, torusMaterial);
torus.position.set(2, 1, -3);
torus.castShadow = true;
torus.receiveShadow = true;
scene.add(torus);
shapes.push(torus);

// ============================================
// ILUMINACIÓN
// ============================================

// Luz direccional (luz principal - sol)
const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
directionalLight.position.set(5, 10, 5);
directionalLight.castShadow = true;
directionalLight.shadow.mapSize.width = 2048;
directionalLight.shadow.mapSize.height = 2048;
directionalLight.shadow.camera.near = 0.5;
directionalLight.shadow.camera.far = 50;
directionalLight.shadow.camera.left = -10;
directionalLight.shadow.camera.right = 10;
directionalLight.shadow.camera.top = 10;
directionalLight.shadow.camera.bottom = -10;
scene.add(directionalLight);

// Luz puntual (luz ambiente adicional)
const pointLight = new THREE.PointLight(0x4fc3f7, 0.8, 20);
pointLight.position.set(-5, 5, -5);
pointLight.castShadow = true;
scene.add(pointLight);

// Luz ambiente suave
const ambientLight = new THREE.AmbientLight(0x404040, 0.3);
scene.add(ambientLight);

// ============================================
// CONFIGURACIÓN DE CÁMARAS (PERSPECTIVAS)
// ============================================

let currentPerspective = 'frontal'; // 'frontal' o 'superior'

const perspectives = {
    frontal: {
        position: new THREE.Vector3(0, 5, 15),
        target: new THREE.Vector3(0, 0, 0)
    },
    superior: {
        position: new THREE.Vector3(0, 20, 0),
        target: new THREE.Vector3(0, 0, 0)
    }
};

function setPerspective(perspective) {
    const config = perspectives[perspective];
    camera.position.copy(config.position);
    controls.target.copy(config.target);
    controls.update();
    currentPerspective = perspective;
    
    // Actualizar UI
    const status = document.getElementById('camera-status');
    status.textContent = perspective === 'frontal' ? 'Frontal' : 'Superior';
}

// Inicializar con perspectiva frontal
setPerspective('frontal');

// Botón para cambiar perspectiva
document.getElementById('toggle-camera').addEventListener('click', () => {
    const newPerspective = currentPerspective === 'frontal' ? 'superior' : 'frontal';
    setPerspective(newPerspective);
});

// ============================================
// ANIMACIONES
// ============================================

// Variables para animaciones
let time = 0;

function animate() {
    requestAnimationFrame(animate);
    time += 0.01;
    
    // Rotación del cubo
    cube.rotation.x += 0.01;
    cube.rotation.y += 0.01;
    
    // Rotación de la esfera
    sphere.rotation.x += 0.005;
    sphere.rotation.z += 0.01;
    
    // Traslación vertical del cilindro (movimiento de subida/bajada)
    cylinder.position.y = 0.5 + Math.sin(time * 2) * 1.5;
    cylinder.rotation.y += 0.02;
    
    // Rotación y traslación del cono
    cone.rotation.y += 0.015;
    cone.position.x = -2 + Math.cos(time) * 1;
    
    // Rotación del torus
    torus.rotation.x += 0.01;
    torus.rotation.y += 0.015;
    torus.position.y = 1 + Math.sin(time * 1.5) * 0.5;
    
    // Actualizar controles
    controls.update();
    
    // Renderizar
    renderer.render(scene, camera);
}

// Manejar redimensionamiento de ventana
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

// Iniciar animación
animate();

