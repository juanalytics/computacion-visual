import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// ============================================
// PROCEDURAL GEOMETRY GENERATORS
// ============================================

class ProceduralGeometry {
    // Generate procedural grid
    static createGrid(width, height, spacing) {
        const geometry = new THREE.BufferGeometry();
        const vertices = [];
        const indices = [];
        
        // Generate vertices
        for (let z = 0; z <= height; z++) {
            for (let x = 0; x <= width; x++) {
                vertices.push(
                    (x - width / 2) * spacing,
                    0,
                    (z - height / 2) * spacing
                );
            }
        }
        
        // Generate indices for quads
        for (let z = 0; z < height; z++) {
            for (let x = 0; x < width; x++) {
                const a = z * (width + 1) + x;
                const b = a + 1;
                const c = a + width + 1;
                const d = c + 1;
                
                // Two triangles per quad
                indices.push(a, c, b);
                indices.push(b, c, d);
            }
        }
        
        geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
        geometry.setIndex(indices);
        geometry.computeVertexNormals();
        
        return geometry;
    }
    
    // Generate 2D spiral
    static createSpiral2D(turns, radius, step) {
        const geometry = new THREE.BufferGeometry();
        const vertices = [];
        const indices = [];
        
        const totalAngle = turns * 2 * Math.PI;
        const points = Math.max(10, Math.floor(totalAngle / (step * Math.PI / 180)));
        
        for (let i = 0; i <= points; i++) {
            const angle = (i / points) * totalAngle;
            const currentRadius = (radius / turns) * (i / points) * turns;
            vertices.push(
                Math.cos(angle) * currentRadius,
                Math.sin(angle) * currentRadius,
                0
            );
        }
        
        // Create line indices
        for (let i = 0; i < points; i++) {
            indices.push(i, i + 1);
        }
        
        geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
        geometry.setIndex(indices);
        
        return geometry;
    }
    
    // Generate 3D spiral
    static createSpiral3D(turns, radius, step) {
        const geometry = new THREE.BufferGeometry();
        const vertices = [];
        const indices = [];
        
        const totalAngle = turns * 2 * Math.PI;
        const points = Math.max(10, Math.floor(totalAngle / (step * Math.PI / 180)));
        
        for (let i = 0; i <= points; i++) {
            const angle = (i / points) * totalAngle;
            const currentRadius = (radius / turns) * (i / points) * turns;
            const height = (i / points) * turns * 2 - turns;
            
            vertices.push(
                Math.cos(angle) * currentRadius,
                height,
                Math.sin(angle) * currentRadius
            );
        }
        
        // Create line indices
        for (let i = 0; i < points; i++) {
            indices.push(i, i + 1);
        }
        
        geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
        geometry.setIndex(indices);
        
        return geometry;
    }
    
    // Generate Sierpinski Triangle (fractal)
    static createSierpinskiTriangle(iterations, size) {
        const geometry = new THREE.BufferGeometry();
        const vertices = [];
        const indices = [];
        
        // Helper function to subdivide triangle
        function subdivideTriangle(p1, p2, p3, depth) {
            if (depth === 0) {
                // Base case: add triangle
                const startIndex = vertices.length / 3;
                vertices.push(p1.x, p1.y, p1.z);
                vertices.push(p2.x, p2.y, p2.z);
                vertices.push(p3.x, p3.y, p3.z);
                indices.push(startIndex, startIndex + 1, startIndex + 2);
                return;
            }
            
            // Calculate midpoints
            const m1 = new THREE.Vector3(
                (p1.x + p2.x) / 2,
                (p1.y + p2.y) / 2,
                (p1.z + p2.z) / 2
            );
            const m2 = new THREE.Vector3(
                (p2.x + p3.x) / 2,
                (p2.y + p3.y) / 2,
                (p2.z + p3.z) / 2
            );
            const m3 = new THREE.Vector3(
                (p1.x + p3.x) / 2,
                (p1.y + p3.y) / 2,
                (p1.z + p3.z) / 2
            );
            
            // Recursively subdivide the three new triangles
            subdivideTriangle(p1, m1, m3, depth - 1);
            subdivideTriangle(m1, p2, m2, depth - 1);
            subdivideTriangle(m3, m2, p3, depth - 1);
        }
        
        // Initial triangle
        const p1 = new THREE.Vector3(0, size, 0);
        const p2 = new THREE.Vector3(-size * Math.sqrt(3) / 2, -size / 2, 0);
        const p3 = new THREE.Vector3(size * Math.sqrt(3) / 2, -size / 2, 0);
        
        subdivideTriangle(p1, p2, p3, iterations);
        
        geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
        geometry.setIndex(indices);
        geometry.computeVertexNormals();
        
        return geometry;
    }
    
    // Generate Koch Snowflake (fractal)
    static createKochSnowflake(iterations, size) {
        const geometry = new THREE.BufferGeometry();
        const vertices = [];
        const indices = [];
        let vertexIndex = 0;
        
        // Helper function for Koch curve - returns array of points
        function kochCurve(p1, p2, depth) {
            if (depth === 0) {
                // Base case: return the two endpoints
                return [p1, p2];
            }
            
            const dx = p2.x - p1.x;
            const dy = p2.y - p1.y;
            const dist = Math.sqrt(dx * dx + dy * dy) / 3;
            
            // Calculate points
            const p3 = new THREE.Vector3(
                p1.x + dx / 3,
                p1.y + dy / 3,
                0
            );
            const p5 = new THREE.Vector3(
                p1.x + 2 * dx / 3,
                p1.y + 2 * dy / 3,
                0
            );
            
            // Calculate peak point
            const angle = Math.atan2(dy, dx) - Math.PI / 3;
            const p4 = new THREE.Vector3(
                p3.x + Math.cos(angle) * dist,
                p3.y + Math.sin(angle) * dist,
                0
            );
            
            // Recursively subdivide and combine points
            const points1 = kochCurve(p1, p3, depth - 1);
            const points2 = kochCurve(p3, p4, depth - 1);
            const points3 = kochCurve(p4, p5, depth - 1);
            const points4 = kochCurve(p5, p2, depth - 1);
            
            // Combine all points (avoid duplicates)
            const allPoints = [points1[0]];
            allPoints.push(...points1.slice(1));
            allPoints.push(...points2.slice(1));
            allPoints.push(...points3.slice(1));
            allPoints.push(...points4.slice(1));
            
            return allPoints;
        }
        
        // Create equilateral triangle
        const p1 = new THREE.Vector3(0, size, 0);
        const p2 = new THREE.Vector3(-size * Math.sqrt(3) / 2, -size / 2, 0);
        const p3 = new THREE.Vector3(size * Math.sqrt(3) / 2, -size / 2, 0);
        
        // Generate all three sides
        const side1 = kochCurve(p1, p2, iterations);
        const side2 = kochCurve(p2, p3, iterations);
        const side3 = kochCurve(p3, p1, iterations);
        
        // Add vertices and create line segments
        function addSegment(points) {
            for (let i = 0; i < points.length; i++) {
                vertices.push(points[i].x, points[i].y, points[i].z);
                if (i > 0) {
                    indices.push(vertexIndex - 1, vertexIndex);
                }
                vertexIndex++;
            }
        }
        
        addSegment(side1);
        addSegment(side2);
        addSegment(side3);
        
        // Close the loop by connecting last point to first
        if (vertices.length > 0) {
            indices.push(vertexIndex - 1, 0);
        }
        
        geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
        geometry.setIndex(indices);
        
        return geometry;
    }
    
    // Generate procedural terrain
    static createTerrain(resolution, maxHeight, frequency) {
        const geometry = new THREE.BufferGeometry();
        const vertices = [];
        const indices = [];
        const normals = [];
        
        // Generate height map using simple noise
        function noise(x, z) {
            return Math.sin(x * frequency) * Math.cos(z * frequency) * maxHeight;
        }
        
        // Generate vertices
        for (let z = 0; z <= resolution; z++) {
            for (let x = 0; x <= resolution; x++) {
                const fx = (x / resolution) * 10 - 5;
                const fz = (z / resolution) * 10 - 5;
                const y = noise(fx, fz);
                
                vertices.push(fx, y, fz);
            }
        }
        
        // Generate indices
        for (let z = 0; z < resolution; z++) {
            for (let x = 0; x < resolution; x++) {
                const a = z * (resolution + 1) + x;
                const b = a + 1;
                const c = a + resolution + 1;
                const d = c + 1;
                
                indices.push(a, c, b);
                indices.push(b, c, d);
            }
        }
        
        geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
        geometry.setIndex(indices);
        geometry.computeVertexNormals();
        
        return geometry;
    }
    
    // Generate wave surface
    static createWave(amplitude, frequency, time = 0) {
        const geometry = new THREE.BufferGeometry();
        const vertices = [];
        const indices = [];
        const resolution = 50;
        
        for (let z = 0; z <= resolution; z++) {
            for (let x = 0; x <= resolution; x++) {
                const fx = (x / resolution) * 10 - 5;
                const fz = (z / resolution) * 10 - 5;
                const y = Math.sin(fx * frequency + time) * Math.cos(fz * frequency + time) * amplitude;
                
                vertices.push(fx, y, fz);
            }
        }
        
        // Generate indices
        for (let z = 0; z < resolution; z++) {
            for (let x = 0; x < resolution; x++) {
                const a = z * (resolution + 1) + x;
                const b = a + 1;
                const c = a + resolution + 1;
                const d = c + 1;
                
                indices.push(a, c, b);
                indices.push(b, c, d);
            }
        }
        
        geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
        geometry.setIndex(indices);
        geometry.computeVertexNormals();
        
        return geometry;
    }
}

// ============================================
// VERTEX MODIFICATION
// ============================================

class VertexModifier {
    static applyNoise(geometry, intensity) {
        const positions = geometry.attributes.position;
        const originalPositions = positions.array.slice();
        
        for (let i = 0; i < positions.count; i++) {
            const i3 = i * 3;
            const noise = (Math.random() - 0.5) * 2 * intensity;
            positions.array[i3 + 1] = originalPositions[i3 + 1] + noise;
        }
        
        positions.needsUpdate = true;
        geometry.computeVertexNormals();
    }
    
    static applyWave(geometry, intensity, time) {
        const positions = geometry.attributes.position;
        
        for (let i = 0; i < positions.count; i++) {
            const i3 = i * 3;
            const x = positions.array[i3];
            const z = positions.array[i3 + 2];
            const wave = Math.sin(x * 2 + time) * Math.cos(z * 2 + time) * intensity;
            positions.array[i3 + 1] += wave;
        }
        
        positions.needsUpdate = true;
        geometry.computeVertexNormals();
    }
    
    static applyTwist(geometry, intensity) {
        const positions = geometry.attributes.position;
        
        for (let i = 0; i < positions.count; i++) {
            const i3 = i * 3;
            const x = positions.array[i3];
            const y = positions.array[i3 + 1];
            const z = positions.array[i3 + 2];
            
            const angle = y * intensity;
            const cos = Math.cos(angle);
            const sin = Math.sin(angle);
            
            const newX = x * cos - z * sin;
            const newZ = x * sin + z * cos;
            
            positions.array[i3] = newX;
            positions.array[i3 + 2] = newZ;
        }
        
        positions.needsUpdate = true;
        geometry.computeVertexNormals();
    }
    
    static applyBend(geometry, intensity) {
        const positions = geometry.attributes.position;
        
        for (let i = 0; i < positions.count; i++) {
            const i3 = i * 3;
            const x = positions.array[i3];
            const y = positions.array[i3 + 1];
            
            const bend = Math.sin(y * intensity) * intensity * 0.5;
            positions.array[i3] = x + bend;
        }
        
        positions.needsUpdate = true;
        geometry.computeVertexNormals();
    }
}

// ============================================
// MAIN APPLICATION
// ============================================

class ProceduralScene {
    constructor() {
        this.scene = new THREE.Scene();
        this.camera = null;
        this.renderer = null;
        this.controls = null;
        this.animationId = null;
        this.isAnimating = false;
        this.isAnimatingVertices = false;
        this.animationTime = 0;
        
        // Geometry
        this.currentGeometry = null;
        this.currentMesh = null;
        this.comparisonMesh = null;
        this.showComparison = false;
        
        // Parameters
        this.currentType = 'grid';
        this.modificationType = 'none';
        this.modificationIntensity = 1.0;
        
        this.init();
    }
    
    init() {
        // Renderer
        const container = document.getElementById('canvas-container');
        this.renderer = new THREE.WebGLRenderer({ antialias: true });
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setPixelRatio(window.devicePixelRatio);
        this.renderer.setClearColor(0x0a0a0a);
        container.appendChild(this.renderer.domElement);
        
        // Camera
        this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        this.camera.position.set(10, 10, 10);
        this.camera.lookAt(0, 0, 0);
        
        // Controls
        this.controls = new OrbitControls(this.camera, this.renderer.domElement);
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.05;
        
        // Scene setup
        this.setupScene();
        this.setupControls();
        this.generateGeometry('grid');
        
        // Animation loop
        this.animate();
        
        // Handle window resize
        window.addEventListener('resize', () => this.onWindowResize());
    }
    
    setupScene() {
        // Ambient light
        const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
        this.scene.add(ambientLight);
        
        // Directional light
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(5, 10, 5);
        this.scene.add(directionalLight);
        
        // Grid helper
        const gridHelper = new THREE.GridHelper(20, 20, 0x444444, 0x222222);
        this.scene.add(gridHelper);
        
        // Axes helper
        const axesHelper = new THREE.AxesHelper(5);
        this.scene.add(axesHelper);
    }
    
    generateGeometry(type) {
        // Update current type
        this.currentType = type;
        
        // Remove existing geometry
        if (this.currentMesh) {
            this.scene.remove(this.currentMesh);
            this.currentMesh.geometry.dispose();
            this.currentMesh.material.dispose();
        }
        if (this.comparisonMesh) {
            this.scene.remove(this.comparisonMesh);
            this.comparisonMesh.geometry.dispose();
            this.comparisonMesh.material.dispose();
            this.comparisonMesh = null;
        }
        
        let geometry;
        
        switch(type) {
            case 'grid':
                const width = parseInt(document.getElementById('grid-width').value);
                const height = parseInt(document.getElementById('grid-height').value);
                const spacing = parseFloat(document.getElementById('grid-spacing').value);
                geometry = ProceduralGeometry.createGrid(width, height, spacing);
                break;
                
            case 'spiral':
                const turns2D = parseFloat(document.getElementById('spiral-turns').value);
                const radius2D = parseFloat(document.getElementById('spiral-radius').value);
                const step2D = parseFloat(document.getElementById('spiral-step').value);
                geometry = ProceduralGeometry.createSpiral2D(turns2D, radius2D, step2D);
                break;
                
            case 'spiral3d':
                const turns3D = parseFloat(document.getElementById('spiral-turns').value);
                const radius3D = parseFloat(document.getElementById('spiral-radius').value);
                const step3D = parseFloat(document.getElementById('spiral-step').value);
                geometry = ProceduralGeometry.createSpiral3D(turns3D, radius3D, step3D);
                break;
                
            case 'sierpinski':
                const sierpinskiIterations = parseInt(document.getElementById('fractal-iterations').value);
                const sierpinskiSize = parseFloat(document.getElementById('fractal-size').value);
                geometry = ProceduralGeometry.createSierpinskiTriangle(sierpinskiIterations, sierpinskiSize);
                break;
                
            case 'koch':
                const kochIterations = parseInt(document.getElementById('fractal-iterations').value);
                const kochSize = parseFloat(document.getElementById('fractal-size').value);
                geometry = ProceduralGeometry.createKochSnowflake(kochIterations, kochSize);
                break;
                
            case 'terrain':
                const terrainRes = parseInt(document.getElementById('terrain-resolution').value);
                const terrainHeight = parseFloat(document.getElementById('terrain-height').value);
                const terrainFreq = parseFloat(document.getElementById('terrain-frequency').value);
                geometry = ProceduralGeometry.createTerrain(terrainRes, terrainHeight, terrainFreq);
                break;
                
            case 'wave':
                const waveAmp = parseFloat(document.getElementById('wave-amplitude').value);
                const waveFreq = parseFloat(document.getElementById('wave-frequency').value);
                geometry = ProceduralGeometry.createWave(waveAmp, waveFreq, 0);
                break;
        }
        
        // Determine if this is a line-based geometry
        const isLineGeometry = type === 'spiral' || type === 'spiral3d' || type === 'koch';
        
        let material;
        let mesh;
        
        if (isLineGeometry) {
            // Use LineBasicMaterial for line geometries
            material = new THREE.LineBasicMaterial({
                color: 0x4fc3f7,
                linewidth: 2
            });
            mesh = new THREE.LineSegments(geometry, material);
        } else {
            // Use MeshStandardMaterial for surface geometries
            material = new THREE.MeshStandardMaterial({
                color: 0x4fc3f7,
                wireframe: false,
                side: THREE.DoubleSide
            });
            mesh = new THREE.Mesh(geometry, material);
        }
        
        this.currentMesh = mesh;
        this.currentGeometry = geometry;
        this.scene.add(this.currentMesh);
        
        // Apply initial modification
        this.applyModification();
        
        // Show comparison if enabled
        if (this.showComparison) {
            this.showManualComparison(type);
        }
    }
    
    applyModification() {
        if (!this.currentMesh || this.modificationType === 'none') return;
        
        // Don't apply modifications to line geometries (they don't have normals)
        const isLineGeometry = this.currentType === 'spiral' || 
                               this.currentType === 'spiral3d' || 
                               this.currentType === 'koch';
        if (isLineGeometry) {
            // Skip modifications for line geometries
            return;
        }
        
        const intensity = parseFloat(document.getElementById('mod-intensity').value);
        
        switch(this.modificationType) {
            case 'noise':
                VertexModifier.applyNoise(this.currentGeometry, intensity);
                break;
            case 'wave':
                VertexModifier.applyWave(this.currentGeometry, intensity, this.animationTime);
                break;
            case 'twist':
                VertexModifier.applyTwist(this.currentGeometry, intensity);
                break;
            case 'bend':
                VertexModifier.applyBend(this.currentGeometry, intensity);
                break;
        }
    }
    
    showManualComparison(type) {
        if (this.comparisonMesh) {
            this.scene.remove(this.comparisonMesh);
            this.comparisonMesh.geometry.dispose();
            this.comparisonMesh.material.dispose();
        }
        
        let comparisonGeometry;
        
        // Create equivalent manual geometry
        switch(type) {
            case 'grid':
                comparisonGeometry = new THREE.PlaneGeometry(10, 10, 10, 10);
                break;
            case 'spiral':
            case 'spiral3d':
                comparisonGeometry = new THREE.ConeGeometry(2, 5, 32);
                break;
            case 'sierpinski':
            case 'koch':
                comparisonGeometry = new THREE.ConeGeometry(3, 5, 3);
                break;
            case 'terrain':
            case 'wave':
                comparisonGeometry = new THREE.PlaneGeometry(10, 10, 20, 20);
                break;
            default:
                comparisonGeometry = new THREE.BoxGeometry(2, 2, 2);
        }
        
        const comparisonMaterial = new THREE.MeshStandardMaterial({
            color: 0xff6b6b,
            wireframe: true,
            transparent: true,
            opacity: 0.5
        });
        
        this.comparisonMesh = new THREE.Mesh(comparisonGeometry, comparisonMaterial);
        this.comparisonMesh.position.set(0, 0, -15);
        this.scene.add(this.comparisonMesh);
    }
    
    setupControls() {
        // Geometry type selector
        const geometryTypeSelect = document.getElementById('geometry-type');
        geometryTypeSelect.addEventListener('change', (e) => {
            this.currentType = e.target.value;
            this.updateControlVisibility();
            this.generateGeometry(e.target.value);
        });
        
        // Grid controls
        ['grid-width', 'grid-height', 'grid-spacing'].forEach(id => {
            document.getElementById(id).addEventListener('input', (e) => {
                document.getElementById(id + '-value').textContent = e.target.value;
                if (this.currentType === 'grid') {
                    this.generateGeometry('grid');
                }
            });
        });
        
        // Spiral controls
        ['spiral-turns', 'spiral-radius', 'spiral-step'].forEach(id => {
            document.getElementById(id).addEventListener('input', (e) => {
                document.getElementById(id + '-value').textContent = e.target.value;
                if (this.currentType === 'spiral' || this.currentType === 'spiral3d') {
                    this.generateGeometry(this.currentType);
                }
            });
        });
        
        // Fractal controls
        ['fractal-iterations', 'fractal-size'].forEach(id => {
            document.getElementById(id).addEventListener('input', (e) => {
                document.getElementById(id + '-value').textContent = e.target.value;
                if (this.currentType === 'sierpinski' || this.currentType === 'koch') {
                    this.generateGeometry(this.currentType);
                }
            });
        });
        
        // Terrain controls
        ['terrain-resolution', 'terrain-height', 'terrain-frequency'].forEach(id => {
            document.getElementById(id).addEventListener('input', (e) => {
                document.getElementById(id + '-value').textContent = e.target.value;
                if (this.currentType === 'terrain') {
                    this.generateGeometry('terrain');
                }
            });
        });
        
        // Wave controls
        ['wave-amplitude', 'wave-frequency', 'wave-speed'].forEach(id => {
            document.getElementById(id).addEventListener('input', (e) => {
                document.getElementById(id + '-value').textContent = e.target.value;
                if (this.currentType === 'wave') {
                    this.generateGeometry('wave');
                }
            });
        });
        
        // Vertex modification
        document.getElementById('vertex-modification').addEventListener('change', (e) => {
            this.modificationType = e.target.value;
            this.generateGeometry(this.currentType);
        });
        
        document.getElementById('mod-intensity').addEventListener('input', (e) => {
            document.getElementById('mod-intensity-value').textContent = e.target.value;
            this.modificationIntensity = parseFloat(e.target.value);
            this.generateGeometry(this.currentType);
        });
        
        // Animation toggle
        document.getElementById('animate-vertices').addEventListener('click', () => {
            this.isAnimatingVertices = !this.isAnimatingVertices;
            document.getElementById('animate-vertices').textContent = 
                this.isAnimatingVertices ? 'Detener Animación' : 'Animar Vértices';
        });
        
        // Comparison toggle
        document.getElementById('toggle-comparison').addEventListener('click', () => {
            this.showComparison = !this.showComparison;
            const info = document.getElementById('comparison-info');
            info.style.display = this.showComparison ? 'block' : 'none';
            if (this.showComparison) {
                this.showManualComparison(this.currentType);
            } else if (this.comparisonMesh) {
                this.scene.remove(this.comparisonMesh);
                this.comparisonMesh.geometry.dispose();
                this.comparisonMesh.material.dispose();
                this.comparisonMesh = null;
            }
        });
        
        // Animation toggle
        document.getElementById('toggle-animation').addEventListener('click', () => {
            this.isAnimating = !this.isAnimating;
            document.getElementById('toggle-animation').textContent = 
                this.isAnimating ? 'Detener Animación' : 'Iniciar Animación';
        });
        
        // Reset
        document.getElementById('reset-geometry').addEventListener('click', () => {
            this.generateGeometry(this.currentType);
        });
        
        // Initialize control visibility
        this.updateControlVisibility();
    }
    
    updateControlVisibility() {
        // Hide all parameter groups
        document.getElementById('grid-controls').style.display = 'none';
        document.getElementById('spiral-controls').style.display = 'none';
        document.getElementById('fractal-controls').style.display = 'none';
        document.getElementById('terrain-controls').style.display = 'none';
        document.getElementById('wave-controls').style.display = 'none';
        
        // Show relevant group
        switch(this.currentType) {
            case 'grid':
                document.getElementById('grid-controls').style.display = 'block';
                break;
            case 'spiral':
            case 'spiral3d':
                document.getElementById('spiral-controls').style.display = 'block';
                break;
            case 'sierpinski':
            case 'koch':
                document.getElementById('fractal-controls').style.display = 'block';
                break;
            case 'terrain':
                document.getElementById('terrain-controls').style.display = 'block';
                break;
            case 'wave':
                document.getElementById('wave-controls').style.display = 'block';
                break;
        }
    }
    
    animate() {
        this.animationId = requestAnimationFrame(() => this.animate());
        
        this.controls.update();
        
        if (this.isAnimating) {
            if (this.currentMesh) {
                this.currentMesh.rotation.y += 0.01;
            }
        }
        
        // Animate vertices
        if (this.isAnimatingVertices && this.currentMesh && this.modificationType === 'wave') {
            this.animationTime += 0.05;
            this.generateGeometry(this.currentType);
        }
        
        // Animate wave geometry
        if (this.isAnimating && this.currentType === 'wave') {
            this.animationTime += parseFloat(document.getElementById('wave-speed').value) * 0.05;
            this.generateGeometry('wave');
        }
        
        this.renderer.render(this.scene, this.camera);
    }
    
    onWindowResize() {
        const aspect = window.innerWidth / window.innerHeight;
        this.camera.aspect = aspect;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(window.innerWidth, window.innerHeight);
    }
}

// Initialize application
const app = new ProceduralScene();

