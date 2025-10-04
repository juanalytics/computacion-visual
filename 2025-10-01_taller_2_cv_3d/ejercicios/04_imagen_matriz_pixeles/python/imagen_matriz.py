"""
Ejercicio 4: Imagen = Matriz - Canales, Slicing, Histogramas
Taller: Computación Visual & 3D

Objetivo: Manipular pixeles y regiones directamente.
Implementa separación RGB/HSV, editar regiones por slicing, histograma de intensidades,
brillo/contraste, y operaciones de matriz directas.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import os

class ImagenMatriz:
    def __init__(self, image_path):
        """
        Inicializa el procesador de matrices de imagen con OpenCV
        
        Args:
            image_path (str): Ruta a la imagen de entrada
        """
        self.image_path = image_path
        self.original = None
        self.original_rgb = None
        self.results = {}
        
    def load_image(self):
        """Carga la imagen original"""
        self.original = cv2.imread(self.image_path)
        if self.original is None:
            raise ValueError(f"No se pudo cargar la imagen: {self.image_path}")
        
        # Convertir BGR a RGB para matplotlib
        self.original_rgb = cv2.cvtColor(self.original, cv2.COLOR_BGR2RGB)
        print(f"Imagen cargada: {self.original.shape}")
        
    def separate_channels(self):
        """Separa los canales RGB y HSV"""
        # Separar canales RGB
        r, g, b = cv2.split(self.original)
        self.results['red'] = r
        self.results['green'] = g
        self.results['blue'] = b
        
        # Convertir a HSV y separar canales
        hsv = cv2.cvtColor(self.original, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        self.results['hue'] = h
        self.results['saturation'] = s
        self.results['value'] = v
        
        print("✓ Separación de canales RGB y HSV completada")
        
    def create_region_operations(self):
        """Crea operaciones de slicing y edición de regiones"""
        # Crear copias para edición
        img_copy1 = self.original_rgb.copy()
        img_copy2 = self.original_rgb.copy()
        img_copy3 = self.original_rgb.copy()
        
        # Operación 1: Cambiar color de una región específica
        # Seleccionar región (x1, y1, x2, y2)
        region1 = img_copy1[100:200, 150:300]  # Slicing de región
        region1[:, :] = [255, 0, 0]  # Cambiar a rojo
        self.results['region_red'] = img_copy1
        
        # Operación 2: Copiar y pegar región
        # Copiar región de una parte a otra
        source_region = img_copy2[50:150, 50:150]
        img_copy2[250:350, 250:350] = source_region  # Pegar en nueva ubicación
        self.results['region_copy_paste'] = img_copy2
        
        # Operación 3: Aplicar filtro a región específica
        # Aplicar blur gaussiano solo a una región
        region3 = img_copy3[200:300, 200:400]
        region3_blurred = cv2.GaussianBlur(region3, (15, 15), 0)
        img_copy3[200:300, 200:400] = region3_blurred
        self.results['region_blur'] = img_copy3
        
        # Operación 4: Crear máscara y aplicar operación
        mask = np.zeros(img_copy1.shape[:2], dtype=np.uint8)
        cv2.circle(mask, (300, 200), 80, 255, -1)  # Círculo blanco
        img_masked = self.original_rgb.copy()
        img_masked[mask == 255] = [0, 255, 0]  # Verde donde hay máscara
        self.results['region_masked'] = img_masked
        
        print("✓ Operaciones de slicing y edición de regiones completadas")
        
    def create_histograms(self):
        """Crea histogramas de intensidades para diferentes canales"""
        # Histograma de imagen en escala de grises
        gray = cv2.cvtColor(self.original, cv2.COLOR_BGR2GRAY)
        hist_gray = cv2.calcHist([gray], [0], None, [256], [0, 256])
        
        # Histogramas de canales RGB
        hist_r = cv2.calcHist([self.original], [2], None, [256], [0, 256])  # Red (BGR)
        hist_g = cv2.calcHist([self.original], [1], None, [256], [0, 256])  # Green
        hist_b = cv2.calcHist([self.original], [0], None, [256], [0, 256])  # Blue
        
        # Guardar histogramas como imágenes
        self.results['histogram_gray'] = hist_gray
        self.results['histogram_r'] = hist_r
        self.results['histogram_g'] = hist_g
        self.results['histogram_b'] = hist_b
        
        print("✓ Histogramas de intensidades calculados")
        
    def apply_brightness_contrast(self):
        """Aplica operaciones de brillo y contraste"""
        # Brillo y contraste manual
        alpha = 1.5  # Contraste (1.0 = sin cambio)
        beta = 50    # Brillo (0 = sin cambio)
        
        # Aplicar transformación: new_pixel = alpha * pixel + beta
        bright_contrast = cv2.convertScaleAbs(self.original, alpha=alpha, beta=beta)
        bright_contrast_rgb = cv2.cvtColor(bright_contrast, cv2.COLOR_BGR2RGB)
        self.results['bright_contrast'] = bright_contrast_rgb
        
        # Usar OpenCV para brillo y contraste
        # Crear lookup table para transformación
        lut = np.zeros((1, 256), dtype=np.uint8)
        for i in range(256):
            lut[0, i] = np.clip(alpha * i + beta, 0, 255)
        
        # Aplicar lookup table
        enhanced = cv2.LUT(self.original, lut)
        enhanced_rgb = cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB)
        self.results['enhanced'] = enhanced_rgb
        
        print("✓ Operaciones de brillo y contraste aplicadas")
        
    def create_matrix_operations(self):
        """Crea operaciones de matriz directas"""
        # Operación 1: Inversión de colores
        inverted = 255 - self.original_rgb
        self.results['inverted'] = inverted
        
        # Operación 2: Escala de grises manual (promedio de canales)
        gray_manual = np.mean(self.original_rgb, axis=2).astype(np.uint8)
        self.results['gray_manual'] = gray_manual
        
        # Operación 3: Operaciones bitwise
        # Crear máscara binaria
        gray = cv2.cvtColor(self.original, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        
        # Aplicar operaciones bitwise
        bitwise_and = cv2.bitwise_and(self.original_rgb, self.original_rgb, mask=mask)
        self.results['bitwise_and'] = bitwise_and
        
        # Operación 4: Transformaciones geométricas con matrices
        # Rotación usando matriz de transformación
        height, width = self.original_rgb.shape[:2]
        center = (width // 2, height // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, 45, 1.0)  # 45 grados
        rotated = cv2.warpAffine(self.original_rgb, rotation_matrix, (width, height))
        self.results['rotated'] = rotated
        
        print("✓ Operaciones de matriz directas completadas")
        
    def create_comparison_visualization(self):
        """Crea visualización comparativa de todas las operaciones"""
        # Configurar la figura
        fig, axes = plt.subplots(4, 4, figsize=(20, 16))
        fig.suptitle('Imagen = Matriz - Operaciones de Píxeles y Canales', fontsize=20, fontweight='bold')
        
        # Lista de operaciones a mostrar
        operations = [
            (self.original_rgb, 'Original'),
            (self.results['red'], 'Canal Rojo'),
            (self.results['green'], 'Canal Verde'),
            (self.results['blue'], 'Canal Azul'),
            (self.results['hue'], 'Canal Hue (HSV)'),
            (self.results['saturation'], 'Canal Saturación'),
            (self.results['value'], 'Canal Valor'),
            (self.results['region_red'], 'Región Roja'),
            (self.results['region_copy_paste'], 'Copia y Pega'),
            (self.results['region_blur'], 'Región con Blur'),
            (self.results['region_masked'], 'Región Enmascarada'),
            (self.results['bright_contrast'], 'Brillo/Contraste'),
            (self.results['inverted'], 'Invertido'),
            (self.results['gray_manual'], 'Gris Manual'),
            (self.results['bitwise_and'], 'Bitwise AND'),
            (self.results['rotated'], 'Rotado 45°')
        ]
        
        # Mostrar cada operación
        for i, (img, title) in enumerate(operations):
            row = i // 4
            col = i % 4
            ax = axes[row, col]
            
            if len(img.shape) == 3:  # Imagen a color
                ax.imshow(img)
            else:  # Imagen en escala de grises
                ax.imshow(img, cmap='gray')
            
            ax.set_title(title, fontsize=10, fontweight='bold')
            ax.axis('off')
        
        plt.tight_layout()
        return fig
        
    def create_histogram_visualization(self):
        """Crea visualización de histogramas"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Histogramas de Intensidades', fontsize=16, fontweight='bold')
        
        # Histograma de escala de grises
        gray = cv2.cvtColor(self.original, cv2.COLOR_BGR2GRAY)
        hist_gray = cv2.calcHist([gray], [0], None, [256], [0, 256])
        axes[0, 0].plot(hist_gray, color='black')
        axes[0, 0].set_title('Escala de Grises')
        axes[0, 0].set_xlabel('Intensidad')
        axes[0, 0].set_ylabel('Frecuencia')
        axes[0, 0].grid(True)
        
        # Histogramas RGB
        hist_r = cv2.calcHist([self.original], [2], None, [256], [0, 256])  # Red
        hist_g = cv2.calcHist([self.original], [1], None, [256], [0, 256])  # Green
        hist_b = cv2.calcHist([self.original], [0], None, [256], [0, 256])  # Blue
        
        axes[0, 1].plot(hist_r, color='red', label='Rojo')
        axes[0, 1].plot(hist_g, color='green', label='Verde')
        axes[0, 1].plot(hist_b, color='blue', label='Azul')
        axes[0, 1].set_title('Canales RGB')
        axes[0, 1].set_xlabel('Intensidad')
        axes[0, 1].set_ylabel('Frecuencia')
        axes[0, 1].legend()
        axes[0, 1].grid(True)
        
        # Histograma HSV
        hsv = cv2.cvtColor(self.original, cv2.COLOR_BGR2HSV)
        hist_h = cv2.calcHist([hsv], [0], None, [256], [0, 256])  # Hue
        hist_s = cv2.calcHist([hsv], [1], None, [256], [0, 256])  # Saturation
        hist_v = cv2.calcHist([hsv], [2], None, [256], [0, 256])  # Value
        
        axes[1, 0].plot(hist_h, color='orange', label='Hue')
        axes[1, 0].plot(hist_s, color='purple', label='Saturación')
        axes[1, 0].plot(hist_v, color='brown', label='Valor')
        axes[1, 0].set_title('Canales HSV')
        axes[1, 0].set_xlabel('Intensidad')
        axes[1, 0].set_ylabel('Frecuencia')
        axes[1, 0].legend()
        axes[1, 0].grid(True)
        
        # Comparación antes/después
        hist_original = cv2.calcHist([gray], [0], None, [256], [0, 256])
        enhanced_gray = cv2.cvtColor(self.results['bright_contrast'], cv2.COLOR_RGB2GRAY)
        hist_enhanced = cv2.calcHist([enhanced_gray], [0], None, [256], [0, 256])
        
        axes[1, 1].plot(hist_original, color='blue', label='Original', alpha=0.7)
        axes[1, 1].plot(hist_enhanced, color='red', label='Mejorado', alpha=0.7)
        axes[1, 1].set_title('Antes vs Después (Brillo/Contraste)')
        axes[1, 1].set_xlabel('Intensidad')
        axes[1, 1].set_ylabel('Frecuencia')
        axes[1, 1].legend()
        axes[1, 1].grid(True)
        
        plt.tight_layout()
        return fig
        
    def analyze_matrix_operations(self):
        """Analiza las operaciones de matriz realizadas"""
        print("\n" + "="*60)
        print("ANÁLISIS DE OPERACIONES DE MATRIZ")
        print("="*60)
        
        # Análisis de canales
        print("\n1. SEPARACIÓN DE CANALES:")
        print("   • RGB: Rojo, Verde, Azul - canales de color aditivos")
        print("   • HSV: Hue (matiz), Saturación, Valor - representación perceptual")
        print("   • Cada canal es una matriz 2D independiente")
        
        # Análisis de slicing
        print("\n2. OPERACIONES DE SLICING:")
        print("   • Slicing: img[y1:y2, x1:x2] para seleccionar regiones")
        print("   • Edición directa: Modificar píxeles por coordenadas")
        print("   • Máscaras: Aplicar operaciones solo a regiones específicas")
        
        # Análisis de histogramas
        print("\n3. ANÁLISIS DE HISTOGRAMAS:")
        gray = cv2.cvtColor(self.original, cv2.COLOR_BGR2GRAY)
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        
        # Calcular estadísticas del histograma
        mean_intensity = np.mean(gray)
        std_intensity = np.std(gray)
        min_intensity = np.min(gray)
        max_intensity = np.max(gray)
        
        print(f"   • Intensidad promedio: {mean_intensity:.1f}")
        print(f"   • Desviación estándar: {std_intensity:.1f}")
        print(f"   • Rango de intensidades: {min_intensity} - {max_intensity}")
        
        # Análisis de operaciones
        print("\n4. OPERACIONES DE MATRIZ:")
        print("   • Inversión: 255 - pixel (operación elemento a elemento)")
        print("   • Brillo/Contraste: alpha * pixel + beta")
        print("   • Transformaciones geométricas: Matrices de rotación/traslación")
        print("   • Operaciones bitwise: AND, OR, XOR a nivel de bits")
        
    def save_individual_results(self, output_dir):
        """Guarda cada resultado individualmente"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Guardar imágenes de canales
        for name, img in self.results.items():
            if name.startswith('histogram'):
                continue  # Los histogramas se guardan por separado
                
            filename = f"{name}.png"
            filepath = output_path / filename
            
            if len(img.shape) == 3:  # Imagen a color
                # Convertir RGB a BGR para OpenCV
                img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                cv2.imwrite(str(filepath), img_bgr)
            else:  # Imagen en escala de grises
                cv2.imwrite(str(filepath), img)
            
            print(f"✓ Guardado: {filepath}")
            
    def run_complete_analysis(self, output_dir="../resultados"):
        """Ejecuta el análisis completo"""
        print("Iniciando análisis de Imagen = Matriz...")
        print("="*50)
        
        # Cargar imagen
        self.load_image()
        
        # Aplicar operaciones
        self.separate_channels()
        self.create_region_operations()
        self.create_histograms()
        self.apply_brightness_contrast()
        self.create_matrix_operations()
        
        # Crear visualizaciones
        fig1 = self.create_comparison_visualization()
        comparison_path = Path(output_dir) / "comparison_matrix_operations.png"
        fig1.savefig(str(comparison_path), dpi=300, bbox_inches='tight')
        print(f"✓ Comparación guardada en: {comparison_path}")
        plt.show()
        
        # Crear visualización de histogramas
        fig2 = self.create_histogram_visualization()
        histogram_path = Path(output_dir) / "histograms_analysis.png"
        fig2.savefig(str(histogram_path), dpi=300, bbox_inches='tight')
        print(f"✓ Histogramas guardados en: {histogram_path}")
        plt.show()
        
        # Guardar resultados individuales
        self.save_individual_results(output_dir)
        
        # Análisis
        self.analyze_matrix_operations()
        
        print("\n" + "="*50)
        print("✓ Análisis completo finalizado!")

def main():
    """Función principal"""
    # Crear directorio de resultados
    output_dir = Path("../resultados")
    output_dir.mkdir(exist_ok=True)
    
    # Ruta de imagen de ejemplo (se puede cambiar)
    image_path = "../assets/sample_image.jpg"
    
    # Si no existe la imagen de ejemplo, crear una
    if not os.path.exists(image_path):
        print("Creando imagen de ejemplo...")
        # Crear una imagen de prueba con colores y patrones
        test_image = np.zeros((400, 600, 3), dtype=np.uint8)
        
        # Agregar regiones de diferentes colores
        # Región roja
        test_image[50:150, 50:200] = [255, 0, 0]  # Rojo
        
        # Región verde
        test_image[50:150, 250:400] = [0, 255, 0]  # Verde
        
        # Región azul
        test_image[200:300, 50:200] = [0, 0, 255]  # Azul
        
        # Región amarilla
        test_image[200:300, 250:400] = [255, 255, 0]  # Amarillo
        
        # Región con gradiente
        for i in range(100):
            intensity = int(255 * i / 100)
            test_image[350:400, 50 + i:150 + i] = [intensity, intensity, intensity]
        
        # Agregar texto
        cv2.putText(test_image, "COLORS", (200, 350), 
                   cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
        
        # Guardar imagen de prueba
        os.makedirs("../assets", exist_ok=True)
        cv2.imwrite(image_path, test_image)
        print(f"✓ Imagen de ejemplo creada: {image_path}")
    
    # Ejecutar análisis
    matriz = ImagenMatriz(image_path)
    matriz.run_complete_analysis(str(output_dir))

if __name__ == "__main__":
    main()
