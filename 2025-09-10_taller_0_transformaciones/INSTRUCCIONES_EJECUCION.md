# Instrucciones de Ejecución - Taller 0 Transformaciones

## Orden Recomendado de Ejecución

### 1. Python (Más Fácil - Empezar Aquí)
```bash
cd python
pip install -r requirements.txt
python transformaciones_2d.py
```
**Resultado**: GIF automático + imagen estática generados en `../resultados/`

### 2. Processing (Intermedio)
1. Descargar [Processing](https://processing.org/download/)
2. Abrir `processing/transformaciones_3d.pde`
3. Presionar Play (Ctrl+R)
4. Usar controles de mouse para navegar
5. Tecla 'S' para capturas, 'R' para reiniciar

### 3. Three.js (Web - Requiere Node.js)
```bash
cd threejs
npm install
npm run dev
```
1. Abrir http://localhost:5173/
2. Usar mouse para navegar la escena 3D
3. Capturar GIF con herramientas externas

### 4. Unity (Opcional - Requiere Unity Hub)
1. Instalar Unity Hub + Unity LTS
2. Crear proyecto 3D nuevo
3. Importar scripts de `unity/`
4. Agregar `ControladorEscena.cs` a GameObject vacío
5. Play Mode para ver animaciones

## Verificación de Resultados

### ✅ Checklist de Funcionamiento

**Python:**
- [ ] Se ejecuta sin errores
- [ ] Muestra ventana con transformaciones estáticas
- [ ] Genera GIF animado automáticamente
- [ ] Archivos aparecen en carpeta `resultados/`

**Three.js:**
- [ ] Servidor se inicia correctamente
- [ ] Página carga sin errores en navegador
- [ ] Se ven 4 objetos con transformaciones diferentes
- [ ] OrbitControls funcionan con mouse

**Processing:**
- [ ] Sketch se ejecuta sin errores
- [ ] Se ve escena 3D con múltiples objetos
- [ ] Mouse controla rotación de cámara
- [ ] Rueda del mouse hace zoom
- [ ] Teclas R y S funcionan

**Unity:**
- [ ] Scripts se importan sin errores de compilación
- [ ] Objetos se crean automáticamente en escena
- [ ] Animaciones se ejecutan suavemente
- [ ] Controles de teclado (R, Espacio) funcionan

## Solución de Problemas Comunes

### Python
**Error: ModuleNotFoundError**
```bash
pip install --upgrade pip
pip install numpy matplotlib imageio pillow
```

**Error: No se genera GIF**
- Verificar que existe carpeta `../resultados/`
- Instalar pillow: `pip install pillow`

### Three.js
**Error: npm no encontrado**
- Instalar Node.js desde https://nodejs.org/

**Error: Puerto ocupado**
```bash
npm run dev -- --port 3000
```

### Processing
**Error: Sketch no se ejecuta**
- Verificar que Processing IDE está actualizado
- Cambiar renderer a P2D si hay problemas con P3D

**Error: Controles no funcionan**
- Verificar que ventana de Processing tiene foco
- Reiniciar sketch con Ctrl+R

### Unity
**Error: Scripts no compilan**
- Verificar versión Unity LTS (2022.3+)
- Revisar que no hay errores de sintaxis

**Error: Objetos no se mueven**
- Verificar que está en Play Mode
- Comprobar que scripts están asignados correctamente

## Capturas de Pantalla y GIFs

### Herramientas Recomendadas
- **Windows**: ScreenToGif (gratuito)
- **macOS**: Kap (gratuito) 
- **Linux**: Peek (gratuito)
- **Multiplataforma**: OBS Studio

### Configuración Recomendada
- **Resolución**: 1280x720 o 1920x1080
- **FPS**: 20-30 FPS
- **Duración**: 5-10 segundos
- **Calidad**: Balance entre tamaño y claridad

## Tiempos Estimados

| Entorno | Setup | Ejecución | Captura | Total |
|---------|-------|-----------|---------|-------|
| Python | 5 min | 2 min | Auto | 7 min |
| Processing | 3 min | 1 min | 3 min | 7 min |
| Three.js | 10 min | 2 min | 5 min | 17 min |
| Unity | 30 min | 5 min | 5 min | 40 min |

**Total estimado**: 1-2 horas (incluyendo Unity opcional)

## Contacto y Ayuda

Si encuentras problemas:
1. Revisar documentación específica en cada carpeta
2. Verificar versiones de software requeridas
3. Consultar logs de error específicos
4. Buscar soluciones en documentación oficial de cada herramienta
