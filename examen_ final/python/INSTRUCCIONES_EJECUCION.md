# Instrucciones para Ejecutar el Notebook

## Paso 1: Crear Entorno Virtual (Recomendado)

Abre una terminal/PowerShell y navega a la carpeta `python`:

```powershell
cd "examen_ final\python"
```

Crea un entorno virtual:

```powershell
python -m venv venv
```

Activa el entorno virtual:

**En PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**En CMD:**
```cmd
venv\Scripts\activate.bat
```

**En Linux/Mac:**
```bash
source venv/bin/activate
```

Verás que el prompt cambia a `(venv)` indicando que el entorno está activo.

> **Nota**: Si tienes problemas activando en PowerShell, puede que necesites cambiar la política de ejecución:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

## Paso 2: Instalar Dependencias

Con el entorno virtual activado, instala las dependencias:

```bash
pip install -r requirements.txt
```

O si prefieres instalar una por una:

```bash
pip install opencv-python numpy matplotlib pillow imageio jupyter
```

## Paso 3: Iniciar Jupyter Notebook

Desde la carpeta `python`, ejecuta:

```bash
jupyter notebook
```

Esto abrirá Jupyter en tu navegador (generalmente en `http://localhost:8888`).

## Paso 4: Abrir el Notebook

En la interfaz de Jupyter, busca y haz clic en:
- `examen_final_python.ipynb`

## Paso 5: Ejecutar las Celdas

Tienes dos opciones:

### Opción A: Ejecutar todo de una vez
- En el menú: **Cell → Run All**
- O usa el atajo: `Shift + Enter` en cada celda (una por una)

### Opción B: Ejecutar celda por celda (recomendado)
1. Ve a la primera celda de código (la que tiene los `import`)
2. Presiona `Shift + Enter` para ejecutarla
3. Espera a que termine (verás un `[*]` que cambia a `[1]` cuando termine)
4. Continúa con la siguiente celda

**Importante**: Ejecuta las celdas en orden, de arriba hacia abajo.

## Paso 6: Verificar Resultados

Después de ejecutar todas las celdas:

1. **Verás las visualizaciones** directamente en el notebook
2. **El GIF se generará automáticamente** en la carpeta `gifs/`
3. Verifica que el archivo existe: `gifs/examen_final_animacion.gif`

## Desactivar el Entorno Virtual (cuando termines)

Cuando termines de trabajar, puedes desactivar el entorno virtual:

```bash
deactivate
```

## Solución de Problemas

### Error: "No module named 'cv2'"
- Asegúrate de que el entorno virtual esté activado
- Instala OpenCV: `pip install opencv-python`

### Error: "No module named 'imageio'"
- Instala imageio: `pip install imageio`

### Error al leer la imagen WebP
- El código ya maneja esto automáticamente usando PIL como respaldo
- Si persiste, verifica que la imagen esté en `data/animal.webp`

### El GIF no se genera
- Verifica que la carpeta `gifs/` existe
- Revisa que todas las celdas se ejecutaron sin errores
- Verifica los mensajes de print() en la última celda

## Atajos Útiles de Jupyter

- `Shift + Enter`: Ejecutar celda y avanzar a la siguiente
- `Ctrl + Enter`: Ejecutar celda sin avanzar
- `Esc`: Salir del modo edición
- `A`: Insertar celda arriba (en modo comando)
- `B`: Insertar celda abajo (en modo comando)
- `DD`: Eliminar celda (presiona D dos veces en modo comando)

