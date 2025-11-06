# Instrucciones Rápidas - Visualizador 360°

## Inicio Rápido

1. **Navegar a la carpeta raíz del proyecto** (donde está `taller_3.md`)

2. **Iniciar servidor local desde la raíz**:
   ```bash
   # Opción 1: Python
   python -m http.server 8000
   
   # Opción 2: Node.js
   npx http-server -p 8000
   ```

3. **Abrir en navegador**:
   ```
   http://localhost:8000/threejs/punto_5/
   ```

4. **Usar el visualizador**:
   - Arrastra con el mouse para rotar
   - Usa la rueda para zoom
   - **Carga tus propias imágenes/videos 360°** con los botones "Cargar Imagen 360°" o "Cargar Video 360°"
   - Cambia entre escenas con el selector
   - Activa modo video con el botón

## Cargar tus Propias Imágenes/Videos

**Método recomendado**: Usa los botones de carga en la interfaz:
- **📷 Cargar Imagen 360°**: Para cargar imágenes equirectangulares
- **🎥 Cargar Video 360°**: Para cargar videos 360°

Los archivos se cargan directamente desde tu computadora y se guardan en caché por escena. No necesitas colocarlos en ninguna carpeta del proyecto.

## Controles

- 🖱️ **Mouse**: Arrastrar para rotar, rueda para zoom
- ⌨️ **Teclado**: WASD o flechas para navegar, R para reset, Espacio para play/pause
- 📱 **Móvil**: Activar giroscopio en el panel de controles

## Notas Importantes

- ⚠️ **Siempre usa un servidor HTTP** (no abras directamente el HTML)
- ⚠️ **Formato equirectangular 2:1** requerido para imágenes/videos
- ⚠️ **Giroscopio requiere HTTPS** en algunos navegadores móviles

