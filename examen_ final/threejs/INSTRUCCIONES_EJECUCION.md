# Instrucciones para Ejecutar Three.js

## Paso 1: Abrir Terminal en la Carpeta threejs

Abre PowerShell o CMD y navega a la carpeta:

```powershell
cd "examen_ final\threejs"
```

## Paso 2: Iniciar Servidor HTTP Local

**IMPORTANTE**: Three.js necesita un servidor HTTP local debido a restricciones CORS. No puedes simplemente abrir el archivo HTML directamente.

### Opción A: Python (Recomendado - Más Simple)

Si tienes Python instalado:

```powershell
python -m http.server 8000
```

### Opción B: Node.js (http-server)

Si tienes Node.js instalado:

```powershell
# Primero instala http-server (solo una vez)
npm install -g http-server

# Luego ejecuta
http-server -p 8000
```

### Opción C: VS Code Live Server

Si usas VS Code:
1. Instala la extensión "Live Server"
2. Click derecho en `index.html`
3. Selecciona "Open with Live Server"

## Paso 3: Abrir en el Navegador

Una vez que el servidor esté corriendo, verás algo como:

```
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

Abre tu navegador y ve a:

```
http://localhost:8000
```

O simplemente:

```
http://127.0.0.1:8000
```

## Paso 4: Interactuar con la Escena

Una vez que veas la escena 3D:

- **Click + Arrastrar**: Rotar la cámara alrededor de la escena
- **Rueda del Mouse**: Zoom in/out
- **Click Derecho + Arrastrar**: Mover la cámara (pan)
- **Botón "Cambiar Perspectiva"**: Alternar entre vista frontal y superior

## Detener el Servidor

En la terminal donde está corriendo el servidor, presiona:
```
Ctrl + C
```

## Solución de Problemas

### Error: "python no se reconoce como comando"
- Asegúrate de tener Python instalado
- O usa la Opción B (Node.js)

### Error: "No se puede acceder al sitio"
- Verifica que el servidor esté corriendo
- Asegúrate de usar `http://localhost:8000` (no `file://`)
- Verifica que no haya otro programa usando el puerto 8000

### La escena no se ve
- Abre la consola del navegador (F12) para ver errores
- Verifica que todos los archivos estén en la carpeta `threejs/`
- Asegúrate de estar usando un navegador moderno (Chrome, Firefox, Edge)

