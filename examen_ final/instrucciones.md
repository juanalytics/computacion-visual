
# Examen Final – Computación Visual

## Instrucciones Generales

- Dentro del repositorio personal debe existir una carpeta `examen_final/` con:
  - Carpeta `python/`
  - Carpeta `threejs/`
  - Un archivo `README.md` general con:
    - GIFs que presenten las soluciones.
    - Las soluciones organizadas y explicadas.

---

## Punto 1 – Procesamiento de Imágenes en Python (50%)

### Enunciado

1. **Carga y visualización de una imagen (RGB) de un animal en via de extinción:**
   - Carga una imagen a color (RGB) desde archivo.
   - Muestra la imagen original en una figura.

2. **Filtros básicos:**
   Aplica los siguientes filtros a la imagen :
   - Suavizado / desenfoque 
   - Realce de bordes 

   Para cada filtro:
   - Muestra la imagen resultante.
   - Escribe en el notebook un breve comentario sobre el efecto visual observado.

3. **Visualización de canales de color:**
   - Separa la imagen original en sus tres canales (R, G, B).
   - Muestra en una figura:
     - Los tres canales en escala de grises (cada canal por separado).
   - Explica brevemente qué estructuras se ven más claras u oscuras en cada canal y por qué.

4. **Operaciones morfológicas :**
   - Trabaja sobre una versión en escala de grises o binarizada de la imagen.
   - Aplica dos operaciones morfológicas diferentes

   - Muestra los resultados comparando:
     - Imagen original (o binarizada).
     - Imagen después de cada operación.
   - Explica brevemente que efecto tuvo la operación sobre la imagen

5. **Animación:**
   - Genera una animación simple  o creando un GIF a partir de varios frames donde se vea:
     - La imagen original.
     - Los resultados de los filtros y/o operaciones morfológicas de forma secuencial.

### Entregables del Punto 1

Dentro de la carpeta `python/`:

- `examen_final_python.ipynb` (notebook con todo el proceso y comentarios).
- Carpeta `data/` con la(s) imagen(es) usadas.
- Carpeta `gifs/` con **al menos un GIF** que muestre:
  - Antes y después de los filtros.
  - Antes y después de las operaciones morfológicas.

En el `README.md` principal:

- Sección: `## Punto 1 – Python`
- Incluir los GIFs (enlazados desde `python/gifs`) y una breve explicación (2–3 párrafos máximo).

---

## Punto 2 – Escena con Formas Básicas en Three.js (50%)

**Objetivo:** Construir una **escena 3D** con formas geométricas básicas, animaciones, texturas y controles de cámara.

### Enunciado

Crea una escena 3D en **Three.js** que contenga varias formas geométricas básicas y que cumpla con los siguientes requisitos:

1. **Escena básica con formas geométricas:**
   - Configura una escena con:
     - Escena (`THREE.Scene`).
     - Cámara de perspectiva 
     - Renderizador WebGL.
   - Añade **múltiples formas básicas**
   - Organiza las formas en el espacio para que la escena se vea equilibrada (como una pequeña composición o “escultura” 3D).

2. **Cambio de perspectiva (cámara):**
   - Configura la cámara para poder usar **al menos dos perspectivas diferentes**
   - Debe existir una forma de alternar entre estas perspectivas (por ejemplo, con una tecla, un botón o una pequeña interfaz).

3. **Animación de las formas:**
   - Anima algunas de las formas geométricas
   - La animación debe ser continua usando un bucle de render

4. **Aplicación de texturas e iluminación:**
   - Aplica **al menos dos texturas diferentes**:
     - Por ejemplo, una textura para un plano del piso y otra para algunos cubos o esferas.
   - Debe ser claro visualmente qué objetos tienen cada textura.
   - Aplica dos luces.

5. **Controles de cámara y OrbitControls:**
   - Integra `OrbitControls` para permitir que el usuario:
     - Gire la cámara alrededor de la escena.
     - Haga zoom (acercar y alejar).
   - Asegúrate de que siempre se pueda observar la escena completa y las formas animadas.


### Entregables del Punto 2

Dentro de la carpeta `threejs/`:

- Archivos del proyecto (`index.html`, `main.js` o similar, `package.json` si aplica, etc.).
- Carpeta `textures/` con las texturas utilizadas.
- Carpeta `gifs/` con **al menos un GIF** que muestre:
  - La escena con las formas básicas desde distintas perspectivas.
  - La animación de las formas.
  - El uso de OrbitControls (rotación / zoom).

En el `README.md` principal:

- Sección: `## Punto 2 – Three.js`
- Incluir los GIFs (enlazados desde `threejs/gifs`) y una breve explicación de:
  - Cómo correr el proyecto.
  - Cómo se implementaron:
    - El cambio de perspectiva.
    - Las animaciones.
    - Las texturas.
    - OrbitControls.

---

## Estructura mínima del repositorio

```text
examen_final/
└── examen_final/
    ├── python/
    │   ├── examen_final_python.ipynb
    │   ├── data/
    │   └── gifs/
    ├── threejs/
    │   ├── index.html
    │   ├── src/ (o main.js, según tu estructura)
    │   ├── textures/
    │   └── gifs/
    └── README.md
````

---

## Contenido obligatorio del `README.md`

El `README.md` en la carpeta `examen_final/` debe contener:


1. **Punto 1 – Python:**

   * Breve descripción del enfoque usado.
   * GIFs incrustados con los resultados principales (filtros y morfología).

2. **Punto 2 – Three.js:**

   * Breve descripción de la escena de formas básicas y de la interacción.
   * GIFs incrustados mostrando la escena, las animaciones y los controles.

3. **Instrucciones de ejecución:**

   * Cómo abrir y ejecutar el notebook de Python.
   * Cómo correr el proyecto de Three.js (comandos, servidor local, etc.).

---



