#!/usr/bin/env python3
"""
Script de ejecución para el Ejercicio 5: Rasterización desde Cero
Ejecuta todos los algoritmos de rasterización y genera las imágenes de demostración
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

def run_rasterization():
    """Ejecuta el script principal de rasterización"""
    print("Ejecutando algoritmos de rasterización...")
    try:
        # Importar y ejecutar el módulo principal
        from rasterizacion_clasica import demostrar_algoritmos
        demostrar_algoritmos()
        print("OK: Algoritmos ejecutados correctamente")
        return True
    except Exception as e:
        print(f"ERROR: Error ejecutando algoritmos: {e}")
        return False

def main():
    """Función principal"""
    print("=" * 60)
    print("EJERCICIO 5: RASTERIZACIÓN DESDE CERO")
    print("=" * 60)
    print()
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("rasterizacion_clasica.py"):
        print("ERROR: No se encontró el archivo rasterizacion_clasica.py")
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
        
        # Ejecutar algoritmos
        if not run_rasterization():
            return
        
        print("\n" + "=" * 60)
        print("OK: EJERCICIO COMPLETADO EXITOSAMENTE")
        print("=" * 60)
        print()
        print("Archivos generados:")
        print("- 01_lineas_bresenham.png")
        print("- 02_circulos_punto_medio.png") 
        print("- 03_triangulos_scanline.png")
        print("- 04_composicion_final.png")
        print()
        print("Estas imágenes demuestran los algoritmos de rasterización clásicos:")
        print("1. Algoritmo de Bresenham para líneas")
        print("2. Algoritmo del punto medio para círculos")
        print("3. Algoritmo scanline para relleno de triángulos")
        
        # Volver al directorio original
        os.chdir(original_dir)
        
    except Exception as e:
        print(f"ERROR: Error durante la ejecución: {e}")
        # Asegurar que volvemos al directorio original en caso de error
        if 'original_dir' in locals():
            os.chdir(original_dir)

if __name__ == "__main__":
    main()
