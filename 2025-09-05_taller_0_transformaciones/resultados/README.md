# Resultados - Taller 0 Transformaciones Básicas

Esta carpeta contiene todos los resultados visuales generados por las implementaciones del taller.

## Archivos Esperados

### GIFs Animados (Obligatorios)

1. **`hola_mundo_transformaciones_python.gif`**
   - Generado por: `python/transformaciones_2d.py`
   - Contenido: Transformaciones 2D con matplotlib
   - Duración: ~5 segundos, 20 FPS

2. **`hola_mundo_transformaciones_threejs.gif`**
   - Generado por: Captura de pantalla del navegador
   - Contenido: Escena 3D interactiva con React Three Fiber
   - Duración: ~10 segundos mostrando interactividad

3. **`hola_mundo_transformaciones_processing.gif`**
   - Generado por: Captura externa del sketch Processing
   - Contenido: Transformaciones 3D con controles de mouse
   - Duración: ~8 segundos mostrando navegación

4. **`hola_mundo_transformaciones_unity.gif`** (Opcional)
   - Generado por: Captura del Game View de Unity
   - Contenido: GameObjects con scripts de transformación
   - Duración: ~6 segundos mostrando múltiples objetos

### Capturas Estáticas

1. **`transformaciones_estaticas.png`**
   - Generado por: Python matplotlib
   - Contenido: Todas las transformaciones en una sola imagen

2. **Capturas adicionales por entorno** (opcionales)
   - Screenshots de cada implementación
   - Comparativas lado a lado
   - Diagramas de matrices de transformación

## Instrucciones para Generar

### Python
```bash
cd python
python transformaciones_2d.py
# Genera automáticamente los archivos en ../resultados/
```

### Three.js
```bash
cd threejs
npm run dev
# Usar herramientas de captura de pantalla para crear GIF
# Recomendado: OBS Studio, ScreenToGif, o Peek (Linux)
```

### Processing
```bash
# Ejecutar el sketch transformaciones_3d.pde
# Usar tecla 'S' para capturas individuales
# Usar herramientas externas para GIF animado
```

### Unity
```bash
# Ejecutar el proyecto en Play Mode
# Usar Window > General > Recorder para capturar GIF
# O herramientas externas de captura de pantalla
```

## Herramientas Recomendadas para GIFs

- **Windows**: ScreenToGif, OBS Studio
- **macOS**: Kap, QuickTime + conversión
- **Linux**: Peek, SimpleScreenRecorder
- **Multiplataforma**: OBS Studio, FFmpeg

## Especificaciones Técnicas

- **Resolución**: Mínimo 800x600, máximo 1920x1080
- **Duración**: 5-10 segundos por GIF
- **FPS**: 15-30 FPS (balance entre calidad y tamaño)
- **Tamaño de archivo**: Máximo 10MB por GIF
- **Formato**: GIF animado o MP4 (según requerimientos)

## Checklist de Resultados

- [ ] GIF Python generado automáticamente
- [ ] GIF Three.js capturado manualmente
- [ ] GIF Processing capturado manualmente  
- [ ] GIF Unity capturado (opcional)
- [ ] Imagen estática Python generada
- [ ] Todos los archivos tienen nombres descriptivos
- [ ] Tamaños de archivo apropiados (<10MB)
- [ ] Calidad visual adecuada para demostración
