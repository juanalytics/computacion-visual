import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { RGBELoader } from 'three/addons/loaders/RGBELoader.js';

// ============================================
// COLOR UTILITIES - RGB, HSV, CIELAB
// ============================================

class ColorUtils {
    // Convert RGB to HSV
    static rgbToHsv(r, g, b) {
        r /= 255;
        g /= 255;
        b /= 255;
        
        const max = Math.max(r, g, b);
        const min = Math.min(r, g, b);
        const delta = max - min;
        
        let h = 0;
        if (delta !== 0) {
            if (max === r) {
                h = ((g - b) / delta) % 6;
            } else if (max === g) {
                h = (b - r) / delta + 2;
            } else {
                h = (r - g) / delta + 4;
            }
        }
        h = Math.round(h * 60);
        if (h < 0) h += 360;
        
        const s = max === 0 ? 0 : Math.round((delta / max) * 100);
        const v = Math.round(max * 100);
        
        return { h, s, v };
    }
    
    // Convert RGB to CIELAB
    static rgbToLab(r, g, b) {
        // First convert to XYZ
        r = r / 255;
        g = g / 255;
        b = b / 255;
        
        // Apply gamma correction
        r = r > 0.04045 ? Math.pow((r + 0.055) / 1.055, 2.4) : r / 12.92;
        g = g > 0.04045 ? Math.pow((g + 0.055) / 1.055, 2.4) : g / 12.92;
        b = b > 0.04045 ? Math.pow((b + 0.055) / 1.055, 2.4) : b / 12.92;
        
        // Convert to XYZ using sRGB matrix
        let x = (r * 0.4124 + g * 0.3576 + b * 0.1805) / 0.95047;
        let y = (r * 0.2126 + g * 0.7152 + b * 0.0722) / 1.00000;
        let z = (r * 0.0193 + g * 0.1192 + b * 0.9505) / 1.08883;
        
        // Convert XYZ to Lab
        const fx = x > 0.008856 ? Math.pow(x, 1/3) : (7.787 * x + 16/116);
        const fy = y > 0.008856 ? Math.pow(y, 1/3) : (7.787 * y + 16/116);
        const fz = z > 0.008856 ? Math.pow(z, 1/3) : (7.787 * z + 16/116);
        
        const L = Math.round((116 * fy - 16) * 10) / 10;
        const a = Math.round((500 * (fx - fy)) * 10) / 10;
        const b_lab = Math.round((200 * (fy - fz)) * 10) / 10;
        
        return { L, a, b: b_lab };
    }
    
    // Calculate contrast ratio (simplified for CIELAB)
    static calculateContrast(lab1, lab2) {
        // Using relative luminance difference
        const L1 = lab1.L;
        const L2 = lab2.L;
        const deltaL = Math.abs(L1 - L2);
        
        // Higher delta L = higher contrast
        const contrast = deltaL / 100;
        return contrast.toFixed(2);
    }
    
    // Hex to RGB
    static hexToRgb(hex) {
        const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
        return result ? {
            r: parseInt(result[1], 16),
            g: parseInt(result[2], 16),
            b: parseInt(result[3], 16)
        } : null;
    }
}

// ============================================
// MAIN APPLICATION
// ============================================

class PBRScene {
    constructor() {
        this.scene = new THREE.Scene();
        this.camera = null;
        this.perspectiveCamera = null;
        this.orthographicCamera = null;
        this.renderer = null;
        this.controls = null;
        this.animationId = null;
        this.isAnimating = false;
        
        // Lights
        this.keyLight = null;
        this.fillLight = null;
        this.rimLight = null;
        
        // Materials
        this.pbrMaterial = null;
        this.meshes = [];
        
        // Environment
        this.environmentMap = null;
        
        this.init();
    }
    
    init() {
        // Renderer
        const container = document.getElementById('canvas-container');
        this.renderer = new THREE.WebGLRenderer({ antialias: true });
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setPixelRatio(window.devicePixelRatio);
        this.renderer.outputColorSpace = THREE.SRGBColorSpace;
        this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
        this.renderer.toneMappingExposure = 1.0;
        container.appendChild(this.renderer.domElement);
        
        // Cameras
        const aspect = window.innerWidth / window.innerHeight;
        this.perspectiveCamera = new THREE.PerspectiveCamera(75, aspect, 0.1, 1000);
        this.perspectiveCamera.position.set(5, 5, 5);
        
        const size = 8;
        this.orthographicCamera = new THREE.OrthographicCamera(
            -size * aspect, size * aspect,
            size, -size,
            0.1, 1000
        );
        this.orthographicCamera.position.set(5, 5, 5);
        this.orthographicCamera.lookAt(0, 0, 0);
        
        // Start with perspective camera
        this.camera = this.perspectiveCamera;
        
        // Controls
        this.controls = new OrbitControls(this.camera, this.renderer.domElement);
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.05;
        
        // Scene setup - IMPORTANT: Environment must be created before materials
        this.setupScene();
        this.setupLights();
        this.setupEnvironment(); // Create environment map first
        this.setupMaterials(); // Then create materials with environment map
        this.setupGeometry();
        this.setupControls();
        
        // Animation loop
        this.animate();
        
        // Handle window resize
        window.addEventListener('resize', () => this.onWindowResize());
    }
    
    setupScene() {
        // Background
        this.scene.background = new THREE.Color(0x1a1a2e);
        this.scene.fog = new THREE.Fog(0x1a1a2e, 10, 50);
    }
    
    setupLights() {
        // Key Light (main light from front-right)
        this.keyLight = new THREE.DirectionalLight(0xffffff, 1.0);
        this.keyLight.position.set(5, 8, 5);
        this.keyLight.castShadow = true;
        this.keyLight.shadow.mapSize.width = 2048;
        this.keyLight.shadow.mapSize.height = 2048;
        this.scene.add(this.keyLight);
        
        // Fill Light (softer light from left)
        this.fillLight = new THREE.DirectionalLight(0x8db4ff, 0.5);
        this.fillLight.position.set(-5, 3, 2);
        this.scene.add(this.fillLight);
        
        // Rim Light (back light for edge definition)
        this.rimLight = new THREE.DirectionalLight(0xffd4a3, 0.8);
        this.rimLight.position.set(-3, 4, -8);
        this.scene.add(this.rimLight);
        
        // Ambient light
        const ambientLight = new THREE.AmbientLight(0x404040, 0.3);
        this.scene.add(ambientLight);
    }
    
    setupEnvironment() {
        // Create a procedural HDRI environment map
        const pmremGenerator = new THREE.PMREMGenerator(this.renderer);
        pmremGenerator.compileEquirectangularShader();
        
        // Create a more complex procedural environment scene
        const envScene = new THREE.Scene();
        envScene.background = new THREE.Color(0x87ceeb); // Sky blue background
        
        // Add multiple colored lights to create a rich environment
        // Simulate sky (top hemisphere)
        const skyLight = new THREE.DirectionalLight(0x87ceeb, 2.0);
        skyLight.position.set(0, 1, 0);
        envScene.add(skyLight);
        
        // Simulate sun (bright warm light)
        const sunLight = new THREE.DirectionalLight(0xffd700, 3.0);
        sunLight.position.set(0.5, 0.8, 0.3);
        envScene.add(sunLight);
        
        // Simulate ground reflection (warm light from below)
        const groundLight = new THREE.DirectionalLight(0xff6b35, 1.5);
        groundLight.position.set(0, -1, 0);
        envScene.add(groundLight);
        
        // Add colored ambient lights for more complex reflections
        const ambientEnv1 = new THREE.AmbientLight(0x4a90e2, 0.8);
        envScene.add(ambientEnv1);
        
        const ambientEnv2 = new THREE.AmbientLight(0xffcc99, 0.6);
        envScene.add(ambientEnv2);
        
        // Add some geometric objects to create interesting reflections
        // These will be visible in reflections on metallic surfaces
        const sphereGeo = new THREE.SphereGeometry(10, 32, 32);
        const sphereMat = new THREE.MeshBasicMaterial({ 
            color: 0xffffff,
            emissive: 0xffffff,
            emissiveIntensity: 0.5
        });
        const reflectionSphere = new THREE.Mesh(sphereGeo, sphereMat);
        reflectionSphere.position.set(15, 5, 10);
        envScene.add(reflectionSphere);
        
        // Generate the environment map with higher resolution
        const renderTarget = pmremGenerator.fromScene(envScene, 0.04);
        this.environmentMap = renderTarget.texture;
        
        // Assign to scene
        this.scene.environment = this.environmentMap;
        
        // Store pmremGenerator for later disposal
        this.pmremGenerator = pmremGenerator;
    }
    
    setupMaterials() {
        // Create PBR material with all required properties
        // Environment map should already be created by setupEnvironment()
        this.pbrMaterial = new THREE.MeshStandardMaterial({
            color: 0x808080,
            roughness: 0.5,
            metalness: 0.5,
            envMap: this.environmentMap, // Use the environment map created earlier
            envMapIntensity: 1.0
        });
        
        // Generate normal map procedurally
        this.generateNormalMap();
    }
    
    generateNormalMap() {
        // Create a procedural normal map
        const size = 512;
        const canvas = document.createElement('canvas');
        canvas.width = size;
        canvas.height = size;
        const ctx = canvas.getContext('2d');
        
        // Create a gradient pattern for the normal map
        const imageData = ctx.createImageData(size, size);
        const data = imageData.data;
        
        for (let y = 0; y < size; y++) {
            for (let x = 0; x < size; x++) {
                const index = (y * size + x) * 4;
                
                // Create a wave pattern for surface detail
                const fx = x / size;
                const fy = y / size;
                const noise = Math.sin(fx * Math.PI * 8) * Math.cos(fy * Math.PI * 8) * 0.5 + 0.5;
                
                // Normal map encoding: R = X, G = Y, B = Z
                data[index] = 128; // R
                data[index + 1] = 128; // G
                data[index + 2] = Math.floor(128 + noise * 127); // B (height)
                data[index + 3] = 255; // A
            }
        }
        
        ctx.putImageData(imageData, 0, 0);
        
        // Convert to texture
        const normalTexture = new THREE.CanvasTexture(canvas);
        normalTexture.wrapS = THREE.RepeatWrapping;
        normalTexture.wrapT = THREE.RepeatWrapping;
        normalTexture.repeat.set(4, 4);
        
        this.pbrMaterial.normalMap = normalTexture;
        this.pbrMaterial.normalScale = new THREE.Vector2(1, 1);
    }
    
    setupGeometry() {
        // Create multiple objects to showcase materials
        const geometries = [
            new THREE.SphereGeometry(1.5, 32, 32),
            new THREE.BoxGeometry(2, 2, 2),
            new THREE.TorusGeometry(1.2, 0.5, 16, 100),
            new THREE.ConeGeometry(1.2, 2.5, 32)
        ];
        
        const positions = [
            new THREE.Vector3(-3, 0, 0),
            new THREE.Vector3(3, 0, 0),
            new THREE.Vector3(0, 0, -3),
            new THREE.Vector3(0, 0, 3)
        ];
        
        geometries.forEach((geom, index) => {
            const clonedMaterial = this.pbrMaterial.clone();
            // Ensure cloned material has environment map
            clonedMaterial.envMap = this.environmentMap;
            clonedMaterial.needsUpdate = true;
            const mesh = new THREE.Mesh(geom, clonedMaterial);
            mesh.position.copy(positions[index]);
            mesh.castShadow = true;
            mesh.receiveShadow = true;
            this.scene.add(mesh);
            this.meshes.push(mesh);
        });
        
        // Ground plane
        const groundGeometry = new THREE.PlaneGeometry(20, 20);
        const groundMaterial = new THREE.MeshStandardMaterial({
            color: 0x2a2a2a,
            roughness: 0.8,
            metalness: 0.1
        });
        const ground = new THREE.Mesh(groundGeometry, groundMaterial);
        ground.rotation.x = -Math.PI / 2;
        ground.position.y = -2;
        ground.receiveShadow = true;
        this.scene.add(ground);
    }
    
    setupControls() {
        // Camera toggle
        const cameraTypeSelect = document.getElementById('camera-type');
        const toggleCameraBtn = document.getElementById('toggle-camera');
        
        toggleCameraBtn.addEventListener('click', () => {
            this.toggleCamera();
        });
        
        cameraTypeSelect.addEventListener('change', (e) => {
            if (e.target.value === 'perspective') {
                this.camera = this.perspectiveCamera;
            } else {
                this.camera = this.orthographicCamera;
            }
            this.controls.object = this.camera;
            this.controls.update();
        });
        
        // Material controls
        const albedoInput = document.getElementById('albedo-color');
        const roughnessInput = document.getElementById('roughness');
        const metalnessInput = document.getElementById('metalness');
        const normalInput = document.getElementById('normal-intensity');
        
        albedoInput.addEventListener('input', (e) => {
            const hexColor = e.target.value;
            const color = new THREE.Color(hexColor);
            this.meshes.forEach(mesh => {
                mesh.material.color.copy(color);
            });
            // Sincronizar con el selector de paleta
            document.getElementById('palette-color').value = hexColor;
            this.updateColorInfo(hexColor);
        });
        
        roughnessInput.addEventListener('input', (e) => {
            const value = parseFloat(e.target.value);
            document.getElementById('roughness-value').textContent = value.toFixed(2);
            this.meshes.forEach(mesh => {
                mesh.material.roughness = value;
            });
        });
        
        metalnessInput.addEventListener('input', (e) => {
            const value = parseFloat(e.target.value);
            document.getElementById('metalness-value').textContent = value.toFixed(2);
            this.meshes.forEach(mesh => {
                mesh.material.metalness = value;
            });
        });
        
        normalInput.addEventListener('input', (e) => {
            const value = parseFloat(e.target.value);
            document.getElementById('normal-value').textContent = value.toFixed(1);
            this.meshes.forEach(mesh => {
                mesh.material.normalScale.set(value, value);
            });
        });
        
        // Light controls
        const keyIntensityInput = document.getElementById('key-intensity');
        const fillIntensityInput = document.getElementById('fill-intensity');
        const rimIntensityInput = document.getElementById('rim-intensity');
        const hdriIntensityInput = document.getElementById('hdri-intensity');
        
        keyIntensityInput.addEventListener('input', (e) => {
            const value = parseFloat(e.target.value);
            document.getElementById('key-intensity-value').textContent = value.toFixed(1);
            this.keyLight.intensity = value;
        });
        
        fillIntensityInput.addEventListener('input', (e) => {
            const value = parseFloat(e.target.value);
            document.getElementById('fill-intensity-value').textContent = value.toFixed(1);
            this.fillLight.intensity = value;
        });
        
        rimIntensityInput.addEventListener('input', (e) => {
            const value = parseFloat(e.target.value);
            document.getElementById('rim-intensity-value').textContent = value.toFixed(1);
            this.rimLight.intensity = value;
        });
        
        hdriIntensityInput.addEventListener('input', (e) => {
            const value = parseFloat(e.target.value);
            document.getElementById('hdri-value').textContent = value.toFixed(1);
            // Update all mesh materials
            this.meshes.forEach(mesh => {
                mesh.material.envMapIntensity = value;
                mesh.material.needsUpdate = true;
            });
            // Also update the base material for future clones
            this.pbrMaterial.envMapIntensity = value;
        });
        
        // Palette color - debe aplicar el color a los objetos también
        const paletteInput = document.getElementById('palette-color');
        paletteInput.addEventListener('input', (e) => {
            const hexColor = e.target.value;
            const color = new THREE.Color(hexColor);
            // Aplicar el color a los objetos 3D
            this.meshes.forEach(mesh => {
                mesh.material.color.copy(color);
            });
            // Sincronizar con el selector de albedo
            document.getElementById('albedo-color').value = hexColor;
            // Actualizar información de color
            this.updateColorInfo(hexColor);
        });
        
        // Animation toggle
        const toggleAnimationBtn = document.getElementById('toggle-animation');
        toggleAnimationBtn.addEventListener('click', () => {
            this.isAnimating = !this.isAnimating;
            toggleAnimationBtn.textContent = this.isAnimating ? 'Detener Animación' : 'Iniciar Animación';
        });
        
        // Reset material
        const resetBtn = document.getElementById('reset-material');
        resetBtn.addEventListener('click', () => {
            this.resetMaterial();
        });
        
        // Initialize color info and sync both color pickers
        const initialColor = '#808080';
        document.getElementById('palette-color').value = initialColor;
        document.getElementById('albedo-color').value = initialColor;
        this.updateColorInfo(initialColor);
    }
    
    updateColorInfo(hexColor) {
        const rgb = ColorUtils.hexToRgb(hexColor);
        if (!rgb) return;
        
        const hsv = ColorUtils.rgbToHsv(rgb.r, rgb.g, rgb.b);
        const lab = ColorUtils.rgbToLab(rgb.r, rgb.g, rgb.b);
        
        // Calculate contrast with background (dark gray)
        const bgLab = ColorUtils.rgbToLab(42, 42, 46); // #2a2a2e
        const contrast = ColorUtils.calculateContrast(lab, bgLab);
        
        document.getElementById('rgb-values').textContent = `(${rgb.r}, ${rgb.g}, ${rgb.b})`;
        document.getElementById('hsv-values').textContent = `(${hsv.h}°, ${hsv.s}%, ${hsv.v}%)`;
        document.getElementById('lab-values').textContent = `(${lab.L}, ${lab.a}, ${lab.b})`;
        document.getElementById('contrast-value').textContent = contrast;
    }
    
    toggleCamera() {
        const currentPos = this.camera.position.clone();
        const currentTarget = this.controls.target.clone();
        
        if (this.camera === this.perspectiveCamera) {
            this.camera = this.orthographicCamera;
            document.getElementById('camera-type').value = 'orthographic';
        } else {
            this.camera = this.perspectiveCamera;
            document.getElementById('camera-type').value = 'perspective';
        }
        
        this.camera.position.copy(currentPos);
        this.controls.object = this.camera;
        this.controls.target.copy(currentTarget);
        this.controls.update();
    }
    
    resetMaterial() {
        const resetColor = '#808080';
        document.getElementById('albedo-color').value = resetColor;
        document.getElementById('palette-color').value = resetColor;
        document.getElementById('roughness').value = '0.5';
        document.getElementById('metalness').value = '0.5';
        document.getElementById('normal-intensity').value = '1.0';
        
        document.getElementById('roughness-value').textContent = '0.5';
        document.getElementById('metalness-value').textContent = '0.5';
        document.getElementById('normal-value').textContent = '1.0';
        
        this.meshes.forEach(mesh => {
            mesh.material.color.setHex(0x808080);
            mesh.material.roughness = 0.5;
            mesh.material.metalness = 0.5;
            mesh.material.normalScale.set(1, 1);
        });
        
        this.updateColorInfo(resetColor);
    }
    
    animate() {
        this.animationId = requestAnimationFrame(() => this.animate());
        
        // Update controls
        this.controls.update();
        
        // Rotate meshes
        this.meshes.forEach((mesh, index) => {
            mesh.rotation.y += 0.005;
            mesh.rotation.x += 0.003;
            
            // Animation mode: vary material properties
            if (this.isAnimating) {
                const time = Date.now() * 0.001;
                mesh.material.roughness = 0.3 + Math.sin(time + index) * 0.2;
                mesh.material.metalness = 0.3 + Math.cos(time * 0.8 + index) * 0.3;
                
                // Animate light intensity
                this.keyLight.intensity = 1.0 + Math.sin(time) * 0.5;
                this.fillLight.intensity = 0.5 + Math.cos(time * 1.2) * 0.3;
                this.rimLight.intensity = 0.8 + Math.sin(time * 0.9) * 0.4;
                
                // Update UI
                document.getElementById('key-intensity').value = this.keyLight.intensity;
                document.getElementById('key-intensity-value').textContent = this.keyLight.intensity.toFixed(1);
                document.getElementById('fill-intensity').value = this.fillLight.intensity;
                document.getElementById('fill-intensity-value').textContent = this.fillLight.intensity.toFixed(1);
                document.getElementById('rim-intensity').value = this.rimLight.intensity;
                document.getElementById('rim-intensity-value').textContent = this.rimLight.intensity.toFixed(1);
            }
        });
        
        // Render
        this.renderer.render(this.scene, this.camera);
    }
    
    onWindowResize() {
        const aspect = window.innerWidth / window.innerHeight;
        
        this.perspectiveCamera.aspect = aspect;
        this.perspectiveCamera.updateProjectionMatrix();
        
        const size = 8;
        this.orthographicCamera.left = -size * aspect;
        this.orthographicCamera.right = size * aspect;
        this.orthographicCamera.updateProjectionMatrix();
        
        this.renderer.setSize(window.innerWidth, window.innerHeight);
    }
}

// Initialize application
const app = new PBRScene();
