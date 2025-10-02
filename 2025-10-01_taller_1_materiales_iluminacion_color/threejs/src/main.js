import './style.css'
import * as THREE from 'three'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js'
import { GUI } from 'lil-gui'
import gsap from 'gsap'

const root = document.querySelector('#app')
root.innerHTML = ''

// Scene - Post-apocalyptic atmosphere
const scene = new THREE.Scene()
scene.background = new THREE.Color(0x2c1810) // Dark orange-brown sky
scene.fog = new THREE.Fog(0x2c1810, 5, 30) // Dense atmospheric fog

// Renderer
const renderer = new THREE.WebGLRenderer({ antialias: true })
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
renderer.setSize(window.innerWidth, window.innerHeight)
renderer.outputColorSpace = THREE.SRGBColorSpace
renderer.toneMapping = THREE.ACESFilmicToneMapping
renderer.toneMappingExposure = 1.0
root.appendChild(renderer.domElement)

// Cameras: Perspective + Orthographic
const aspect = window.innerWidth / window.innerHeight
const perspectiveCamera = new THREE.PerspectiveCamera(60, aspect, 0.1, 200)
perspectiveCamera.position.set(6, 4, 8)

const frustumSize = 10
const orthographicCamera = new THREE.OrthographicCamera(
  (frustumSize * aspect) / -2,
  (frustumSize * aspect) / 2,
  frustumSize / 2,
  frustumSize / -2,
  0.1,
  200
)
orthographicCamera.position.set(6, 4, 8)

let activeCamera = perspectiveCamera

// Simple controls via pointer drag (minimal, no OrbitControls to keep template simple)
let isPointerDown = false
let lastX = 0
let lastY = 0
const target = new THREE.Vector3(0, 1, 0)

function onPointerDown(e) {
  isPointerDown = true
  lastX = e.clientX
  lastY = e.clientY
}

function onPointerUp() {
  isPointerDown = false
}

function onPointerMove(e) {
  if (!isPointerDown) return
  const dx = (e.clientX - lastX) * 0.005
  const dy = (e.clientY - lastY) * 0.005
  lastX = e.clientX
  lastY = e.clientY

  const cam = activeCamera
  const offset = new THREE.Vector3().copy(cam.position).sub(target)
  const spherical = new THREE.Spherical().setFromVector3(offset)
  spherical.theta -= dx
  spherical.phi -= dy
  const EPS = 0.000001
  spherical.phi = Math.max(EPS, Math.min(Math.PI - EPS, spherical.phi))
  offset.setFromSpherical(spherical)
  cam.position.copy(target).add(offset)
  cam.lookAt(target)
}

renderer.domElement.addEventListener('pointerdown', onPointerDown)
renderer.domElement.addEventListener('pointerup', onPointerUp)
renderer.domElement.addEventListener('pointerleave', onPointerUp)
renderer.domElement.addEventListener('pointermove', onPointerMove)

// Resize
window.addEventListener('resize', () => {
  const w = window.innerWidth
  const h = window.innerHeight
  renderer.setSize(w, h)
  const a = w / h
  perspectiveCamera.aspect = a
  perspectiveCamera.updateProjectionMatrix()
  orthographicCamera.left = (-frustumSize * a) / 2
  orthographicCamera.right = (frustumSize * a) / 2
  orthographicCamera.top = frustumSize / 2
  orthographicCamera.bottom = -frustumSize / 2
  orthographicCamera.updateProjectionMatrix()
})

// Forest floor ground with complete PBR texture set - extended for horizon
const groundGeometry = new THREE.PlaneGeometry(200, 200, 32, 32) // Much larger for horizon effect

// Load all textures
const textureLoader = new THREE.TextureLoader()
const diffuseMap = textureLoader.load('/forrest_ground_01_diff_2k.jpg')
const displacementMap = textureLoader.load('/forrest_ground_01_disp_2k.png')
const roughnessMap = textureLoader.load('/forrest_ground_01_rough_2k.jpg')

// Configure all textures
diffuseMap.wrapS = diffuseMap.wrapT = THREE.RepeatWrapping
diffuseMap.repeat.set(8, 8) // Much smaller details
displacementMap.wrapS = displacementMap.wrapT = THREE.RepeatWrapping
displacementMap.repeat.set(8, 8)
roughnessMap.wrapS = roughnessMap.wrapT = THREE.RepeatWrapping
roughnessMap.repeat.set(8, 8)

const groundMaterial = new THREE.MeshStandardMaterial({ 
  map: diffuseMap, // Diffuse/albedo texture
  displacementMap: displacementMap, // Height displacement
  roughnessMap: roughnessMap, // Roughness variation
  displacementScale: 1.5, // Reduced displacement
  color: 0x2d5016, // Darker base color to make it less light
  side: THREE.DoubleSide
})

const ground = new THREE.Mesh(groundGeometry, groundMaterial)
ground.rotation.x = -Math.PI * 0.5
ground.position.y = 0
ground.receiveShadow = true
scene.add(ground)

// GLB Models
const loader = new GLTFLoader()
const models = {
  warehouse: null,
  submarine: null,
  policeCar: null,
  policeCar2: null,
  cherryTree: null,
  cherryTree2: null,
  cherryTree3: null,
  cherryTree4: null,
  cherryTree5: null,
  grass1: null,
  grass2: null,
  grass3: null,
  grass4: null
}

// Demo object removed - using real GLB models only

// Neutral materials - let models keep their original appearance

// Initial tree removed - keeping only cherry tree

loader.load('/atlantic_explorer_submarineglb.glb', 
  (gltf) => {
    console.log('Submarine loaded successfully')
    models.warehouse = gltf.scene
    models.warehouse.position.set(4, 0.5, -16) // Raised to align with textured ground
    models.warehouse.scale.setScalar(1.2)
    models.warehouse.castShadow = true
    
    // Keep original materials
    
    scene.add(models.warehouse)
  },
  (progress) => {
    console.log('Submarine loading progress:', progress)
  },
  (error) => {
    console.error('Error loading submarine:', error)
  }
)

// Train car removed

loader.load('/free_burned_police_cars.glb', 
  (gltf) => {
    console.log('Police car loaded successfully')
    models.policeCar = gltf.scene
    models.policeCar.position.set(10, 0.5, 4)
    models.policeCar.scale.setScalar(0.015) // Dramatically scaled down
    models.policeCar.castShadow = true
    scene.add(models.policeCar)
  },
  (progress) => console.log('Police car loading progress:', progress),
  (error) => console.error('Error loading police car:', error)
)

// Load additional police car
loader.load('/free_burned_police_cars.glb', 
  (gltf) => {
    console.log('Police car 2 loaded successfully')
    models.policeCar2 = gltf.scene
    models.policeCar2.position.set(-15, 0.5, 10)
    models.policeCar2.scale.setScalar(0.015) // Same scale as first one
    models.policeCar2.castShadow = true
    scene.add(models.policeCar2)


    
  },
  (progress) => console.log('Police car 2 loading progress:', progress),
  (error) => console.error('Error loading police car 2:', error)
)

// Red car removed

// Load cherry trees at different heights
loader.load('/stylized_low_poly_tree_-_game-ready.glb', 
  (gltf) => {
    console.log('Stylized tree 1 loaded successfully')
    models.cherryTree = gltf.scene
    models.cherryTree.position.set(4, 1, 12)
    models.cherryTree.scale.setScalar(1.5)
    models.cherryTree.castShadow = true
    scene.add(models.cherryTree)
  },
  (progress) => console.log('Stylized tree 1 loading progress:', progress),
  (error) => console.error('Error loading cherry tree 1:', error)
)

loader.load('/stylized_low_poly_tree_-_game-ready.glb', 
  (gltf) => {
    console.log('Stylized tree 2 loaded successfully')
    models.cherryTree2 = gltf.scene
    models.cherryTree2.position.set(-6, 0.5, 8) // Lower height
    models.cherryTree2.scale.setScalar(1.2)
    models.cherryTree2.castShadow = true
    scene.add(models.cherryTree2)
  },
  (progress) => console.log('Stylized tree 2 loading progress:', progress),
  (error) => console.error('Error loading cherry tree 2:', error)
)

loader.load('/stylized_low_poly_tree_-_game-ready.glb', 
  (gltf) => {
    console.log('Stylized tree 3 loaded successfully')
    models.cherryTree3 = gltf.scene
    models.cherryTree3.position.set(8, 0.3, -5) // Even lower height
    models.cherryTree3.scale.setScalar(1.0)
    models.cherryTree3.castShadow = true
    scene.add(models.cherryTree3)
  },
  (progress) => console.log('Stylized tree 3 loading progress:', progress),
  (error) => console.error('Error loading cherry tree 3:', error)
)

// Load additional cherry trees
loader.load('/stylized_low_poly_tree_-_game-ready.glb', 
  (gltf) => {
    console.log('Stylized tree 4 loaded successfully')
    models.cherryTree4 = gltf.scene
    models.cherryTree4.position.set(-10, 0.2, -8) // Lower height
    models.cherryTree4.scale.setScalar(0.8)
    models.cherryTree4.castShadow = true
    scene.add(models.cherryTree4)
  },
  (progress) => console.log('Stylized tree 4 loading progress:', progress),
  (error) => console.error('Error loading cherry tree 4:', error)
)

loader.load('/stylized_low_poly_tree_-_game-ready.glb', 
  (gltf) => {
    console.log('Stylized tree 5 loaded successfully')
    models.cherryTree5 = gltf.scene
    models.cherryTree5.position.set(12, 0.4, 2) // Lower height
    models.cherryTree5.scale.setScalar(1.1)
    models.cherryTree5.castShadow = true
    scene.add(models.cherryTree5)
  },
  (progress) => console.log('Stylized tree 5 loading progress:', progress),
  (error) => console.error('Error loading cherry tree 5:', error)
)

// Photogrammetry tree removed

// Load scattered grass
loader.load('/grass_green.glb', 
  (gltf) => {
    console.log('Grass 1 loaded successfully')
    models.grass1 = gltf.scene
    models.grass1.position.set(-3, 0.5, -2)
    models.grass1.scale.setScalar(0.005)
    models.grass1.castShadow = true
    scene.add(models.grass1)
  },
  (progress) => console.log('Grass 1 loading progress:', progress),
  (error) => console.error('Error loading grass 1:', error)
)

loader.load('/grass_green.glb', 
  (gltf) => {
    console.log('Grass 2 loaded successfully')
    models.grass2 = gltf.scene
    models.grass2.position.set(2, 0.5, 4)
    models.grass2.scale.setScalar(0.005)
    models.grass2.castShadow = true
    scene.add(models.grass2)
  },
  (progress) => console.log('Grass 2 loading progress:', progress),
  (error) => console.error('Error loading grass 2:', error)
)

loader.load('/grass_green.glb', 
  (gltf) => {
    console.log('Grass 3 loaded successfully')
    models.grass3 = gltf.scene
    models.grass3.position.set(-8, 0.5, 2)
    models.grass3.scale.setScalar(0.005)
    models.grass3.castShadow = true
    scene.add(models.grass3)
  },
  (progress) => console.log('Grass 3 loading progress:', progress),
  (error) => console.error('Error loading grass 3:', error)
)

loader.load('/grass_green.glb', 
  (gltf) => {
    console.log('Grass 4 loaded successfully')
    models.grass4 = gltf.scene
    models.grass4.position.set(6, 0.5, -8)
    models.grass4.scale.setScalar(0.005)
    models.grass4.castShadow = true
    scene.add(models.grass4)
  },
  (progress) => console.log('Grass 4 loading progress:', progress),
  (error) => console.error('Error loading grass 4:', error)
)

// Lights: key, fill, rim + ambient
const ambientLight = new THREE.AmbientLight(0xffffff, 0.2)
scene.add(ambientLight)

const keyLight = new THREE.DirectionalLight(0xffffff, 2.0)
keyLight.position.set(5, 6, 4)
scene.add(keyLight)

const fillLight = new THREE.DirectionalLight(0xffffff, 0.8)
fillLight.position.set(-6, 4, -2)
scene.add(fillLight)

const rimLight = new THREE.DirectionalLight(0xffffff, 1.2)
rimLight.position.set(-2, 6, 6)
scene.add(rimLight)

const lightPresets = {
  nuclear: {
    ambient: { color: 0x4a2c00, intensity: 0.5 },
    key: { color: 0xff6600, intensity: 1.0 }, // Nuclear orange - toned down
    fill: { color: 0x8b4513, intensity: 0.2 }, // Brown fill - softer
    rim: { color: 0xffaa00, intensity: 1.2 }, // Golden rim - less intense
    exposure: 1.1
  },
  wasteland: {
    ambient: { color: 0x2c1810, intensity: 0.2 },
    key: { color: 0xff4500, intensity: 2.0 }, // Wasteland red-orange
    fill: { color: 0x654321, intensity: 0.6 }, // Dark brown fill
    rim: { color: 0xff8c00, intensity: 1.5 }, // Orange rim
    exposure: 1.1
  },
  afternoon: {
    ambient: { color: 0xf5f5dc, intensity: 0.4 }, // Warm white
    key: { color: 0xffd700, intensity: 1.8 }, // Golden afternoon sun
    fill: { color: 0x87ceeb, intensity: 0.6 }, // Sky blue fill
    rim: { color: 0xffa500, intensity: 1.2 }, // Orange rim
    exposure: 1.0
  }
}

function applyLightPreset(presetName) {
  const p = lightPresets[presetName]
  if (!p) return
  ambientLight.color.setHex(p.ambient.color)
  ambientLight.intensity = p.ambient.intensity
  keyLight.color.setHex(p.key.color)
  keyLight.intensity = p.key.intensity
  fillLight.color.setHex(p.fill.color)
  fillLight.intensity = p.fill.intensity
  rimLight.color.setHex(p.rim.color)
  rimLight.intensity = p.rim.intensity
  renderer.toneMappingExposure = p.exposure
  
  // Apply skybox for afternoon preset
  if (presetName === 'afternoon') {
    // Create beautiful afternoon sky gradient - much closer to scene
    const skyGeometry = new THREE.SphereGeometry(100, 32, 15)
    const skyMaterial = new THREE.ShaderMaterial({
      uniforms: {
        topColor: { value: new THREE.Color(0x87CEEB) }, // Sky blue
        bottomColor: { value: new THREE.Color(0xFFE4B5) }, // Moccasin
        offset: { value: 0 },
        exponent: { value: 0.6 }
      },
      vertexShader: `
        varying vec3 vWorldPosition;
        void main() {
          vec4 worldPosition = modelMatrix * vec4(position, 1.0);
          vWorldPosition = worldPosition.xyz;
          gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
      `,
      fragmentShader: `
        uniform vec3 topColor;
        uniform vec3 bottomColor;
        uniform float offset;
        uniform float exponent;
        varying vec3 vWorldPosition;
        void main() {
          float h = normalize(vWorldPosition + offset).y;
          gl_FragColor = vec4(mix(bottomColor, topColor, pow(max(h, 0.0), exponent)), 1.0);
        }
      `,
      side: THREE.BackSide
    })
    
    const sky = new THREE.Mesh(skyGeometry, skyMaterial)
    sky.position.set(0, 0, 0) // Center it on the scene
    scene.add(sky)
    
    // Remove fog for clear afternoon sky
    scene.fog = null
    
    // Add some clouds
    const cloudGeometry = new THREE.PlaneGeometry(100, 50)
    const cloudMaterial = new THREE.MeshLambertMaterial({
      color: 0xffffff,
      transparent: true,
      opacity: 0.6
    })
    
    for (let i = 0; i < 5; i++) {
      const cloud = new THREE.Mesh(cloudGeometry, cloudMaterial)
      cloud.position.set(
        (Math.random() - 0.5) * 200,
        50 + Math.random() * 30,
        (Math.random() - 0.5) * 200
      )
      cloud.rotation.y = Math.random() * Math.PI
      cloud.scale.setScalar(0.5 + Math.random() * 0.5)
      scene.add(cloud)
    }
  } else {
    // Reset to post-apocalyptic for other presets
    scene.background = new THREE.Color(0x2c1810)
    scene.fog = new THREE.Fog(0x2c1810, 5, 30)
    
    // Remove sky and clouds
    const skyObjects = scene.children.filter(child => 
      child.geometry && child.geometry.type === 'SphereGeometry' ||
      child.material && child.material.transparent && child.material.opacity === 0.6
    )
    skyObjects.forEach(obj => scene.remove(obj))
  }
}

applyLightPreset('nuclear')

// Camera toggle
function setCamera(type) {
  activeCamera = type === 'orthographic' ? orthographicCamera : perspectiveCamera
  activeCamera.lookAt(target)
}

window.addEventListener('keydown', (e) => {
  if (e.key.toLowerCase() === 'c') {
    const next = activeCamera === perspectiveCamera ? 'orthographic' : 'perspective'
    setCamera(next)
  }
})

// GUI
const gui = new GUI()
const params = {
  camera: 'perspective',
  preset: 'nuclear',
  rotateObject: true,
  fog: true,
  particles: true,
  dustOpacity: 0.3
}

gui.add(params, 'camera', ['perspective', 'orthographic']).name('Camera').onChange(setCamera)
gui.add(params, 'preset', ['nuclear', 'wasteland', 'afternoon']).name('Lighting').onChange(applyLightPreset)
gui.add(params, 'rotateObject').name('Rotate demo')

// Post-apocalyptic effect toggles
const effectsFolder = gui.addFolder('Post-Apocalyptic Effects')
effectsFolder.add(params, 'fog').name('Fog').onChange((value) => {
  scene.fog = value ? new THREE.Fog(0x2c1810, 5, 30) : null
})
effectsFolder.add(params, 'particles').name('Dust Particles').onChange((value) => {
  particles.visible = value
})
effectsFolder.add(params, 'dustOpacity', 0, 1).name('Dust Opacity').onChange((value) => {
  particleMaterial.opacity = value
})
effectsFolder.open()

// Post-apocalyptic atmospheric effects
// Add dust particles
const particleGeometry = new THREE.BufferGeometry()
const particleCount = 3000
const positions = new Float32Array(particleCount * 3)

for (let i = 0; i < particleCount * 3; i++) {
  positions[i] = (Math.random() - 0.5) * 200
}

particleGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))

const particleMaterial = new THREE.PointsMaterial({
  color: 0x8b4513, // Dusty brown
  size: 1.0,
  transparent: true,
  opacity: 0.6
})

const particles = new THREE.Points(particleGeometry, particleMaterial)
scene.add(particles)

// Enhanced animations
gsap.to(rimLight.position, { x: 3, z: -3, duration: 6, yoyo: true, repeat: -1, ease: 'sine.inOut' })

// Camera path animation - much larger scale
const cameraPath = new THREE.CatmullRomCurve3([
  new THREE.Vector3(15, 8, 20),   // start - far back
  new THREE.Vector3(25, 12, 10),  // high right - showcase warehouse
  new THREE.Vector3(10, 6, 5),    // low center - close to submarine
  new THREE.Vector3(-15, 10, 15), // left - showcase tree
  new THREE.Vector3(-5, 4, 25),   // back left - wide view
  new THREE.Vector3(5, 15, 30),   // high back - aerial view
  new THREE.Vector3(15, 8, 20)    // return to start
])

// Add camera path controls to GUI
const cameraParams = {
  followPath: false,
  pathSpeed: 2.0
}

gui.add(cameraParams, 'followPath').name('Camera Path')
gui.add(cameraParams, 'pathSpeed', 0.5, 5.0).name('Path Speed')

// Render loop
const clock = new THREE.Clock()
function render() {
  const t = clock.getElapsedTime()
  
  // No special shader animations
  
  // Camera path animation
  if (cameraParams.followPath) {
    const pathTime = (t * cameraParams.pathSpeed * 0.1) % 1
    const pathPoint = cameraPath.getPoint(pathTime)
    activeCamera.position.copy(pathPoint)
    activeCamera.lookAt(target)
  }
  
  if (params.rotateObject) {
    // Sway cherry trees
    if (models.cherryTree) {
      models.cherryTree.rotation.z = Math.sin(t * 0.5) * 0.1
    }
    if (models.cherryTree2) {
      models.cherryTree2.rotation.z = Math.sin(t * 0.3) * 0.08
    }
    if (models.cherryTree3) {
      models.cherryTree3.rotation.z = Math.sin(t * 0.7) * 0.06
    }
    if (models.cherryTree4) {
      models.cherryTree4.rotation.z = Math.sin(t * 0.4) * 0.05
    }
    if (models.cherryTree5) {
      models.cherryTree5.rotation.z = Math.sin(t * 0.6) * 0.07
    }
  }
  renderer.render(scene, activeCamera)
  requestAnimationFrame(render)
}

setCamera('perspective')
activeCamera.lookAt(target)
render()
