#!/usr/bin/env python3
"""
Script de ejecución para el Ejercicio 6: Análisis Geométrico
Ejecuta el análisis geométrico completo y genera las imágenes de demostración
"""

import os
import sys
import subprocess

def install_requirements():
    """Instala las dependencias necesarias"""
    print("Instalando dependencias...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("OK: Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Error instalando dependencias: {e}")
        return False

def run_geometric_analysis():
    """Ejecuta el script principal de análisis geométrico"""
    print("Ejecutando análisis geométrico...")
    try:
        # Importar y ejecutar el módulo principal
        from analisis_geometrico import demostrar_analisis_geometrico
        demostrar_analisis_geometrico()
        print("OK: Análisis geométrico ejecutado correctamente")
        return True
    except Exception as e:
        print(f"ERROR: Error ejecutando análisis geométrico: {e}")
        return False

def main():
    """Función principal"""
    print("=" * 60)
    print("EJERCICIO 6: ANÁLISIS GEOMÉTRICO")
    print("=" * 60)
    print()
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("analisis_geometrico.py"):
        print("ERROR: No se encontró el archivo analisis_geometrico.py")
        print("Asegúrate de ejecutar este script desde el directorio del ejercicio")
        return
    
    # Crear directorio de resultados si no existe
    os.makedirs("resultados", exist_ok=True)
    
    try:
        # Instalar dependencias (desde el directorio actual donde está requirements.txt)
        if not install_requirements():
            return
        
        # Cambiar al directorio de resultados para guardar las imágenes
        original_dir = os.getcwd()
        os.chdir("resultados")
        
        # Ejecutar análisis geométrico
        if not run_geometric_analysis():
            return
        
        print("\n" + "=" * 60)
        print("OK: EJERCICIO COMPLETADO EXITOSAMENTE")
        print("=" * 60)
        print()
        print("Archivos generados:")
        print("- 00_imagen_original.png")
        print("- 01_binarizacion_otsu.png")
        print("- 02_binarizacion_adaptativa.png")
        print("- 03_binarizacion_fija.png")
        print("- 04_analisis_completo.png")
        print("- 05_solo_contornos.png")
        print("- 06_solo_metricas.png")
        print("- 07_analisis_estadistico.png")
        print()
        print("Este ejercicio demuestra:")
        print("1. Binarización de imágenes (Otsu, adaptativa, fija)")
        print("2. Detección de contornos")
        print("3. Cálculo de métricas geométricas:")
        print("   - Área y perímetro")
        print("   - Centroides (momentos)")
        print("   - Bounding boxes")
        print("   - Círculos mínimos envolventes")
        print("4. Clasificación automática de formas")
        print("5. Análisis estadístico completo")
        
        # Volver al directorio original
        os.chdir(original_dir)
        
    except Exception as e:
        print(f"ERROR: Error durante la ejecución: {e}")
        # Asegurar que volvemos al directorio original en caso de error
        if 'original_dir' in locals():
            os.chdir(original_dir)

if __name__ == "__main__":
    main()
