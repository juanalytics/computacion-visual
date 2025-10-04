"""
Ejercicio 2: Ojos Digitales - Filtros y Bordes con OpenCV
Taller: Computación Visual & 3D

Objetivo: Entender el flujo básico de percepción: escala de grises, filtros y bordes.
Implementa conversión a gris, blur/sharpen, Sobel X/Y, Laplaciano, y comparación visual.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import os

class OjosDigitales:
    def __init__(self, image_path):
        """
        Inicializa el procesador de imágenes con OpenCV
        
        Args:
            image_path (str): Ruta a la imagen de entrada
        """
        self.image_path = image_path
        self.original = None
        self.gray = None
        self.results = {}
        
    def load_image(self):
        """Carga la imagen original"""
        self.original = cv2.imread(self.image_path)
        if self.original is None:
            raise ValueError(f"No se pudo cargar la imagen: {self.image_path}")
        
        # Convertir BGR a RGB para matplotlib
        self.original_rgb = cv2.cvtColor(self.original, cv2.COLOR_BGR2RGB)
        print(f"Imagen cargada: {self.original.shape}")
        
    def convert_to_grayscale(self):
        """Convierte la imagen a escala de grises"""
        self.gray = cv2.cvtColor(self.original, cv2.COLOR_BGR2GRAY)
        self.results['grayscale'] = self.gray
        print("✓ Conversión a escala de grises completada")
        
    def apply_blur_filters(self):
        """Aplica diferentes tipos de filtros de desenfoque"""
        # Blur gaussiano
        gaussian_blur = cv2.GaussianBlur(self.gray, (15, 15), 0)
        self.results['gaussian_blur'] = gaussian_blur
        
        # Blur promedio
        average_blur = cv2.blur(self.gray, (15, 15))
        self.results['average_blur'] = average_blur
        
        # Blur bilateral (preserva bordes)
        bilateral_blur = cv2.bilateralFilter(self.gray, 15, 80, 80)
        self.results['bilateral_blur'] = bilateral_blur
        
        print("✓ Filtros de desenfoque aplicados")
        
    def apply_sharpen_filters(self):
        """Aplica filtros de enfoque/realce"""
        # Kernel de enfoque
        sharpen_kernel = np.array([[-1, -1, -1],
                                   [-1,  9, -1],
                                   [-1, -1, -1]])
        sharpen = cv2.filter2D(self.gray, -1, sharpen_kernel)
        self.results['sharpen'] = sharpen
        
        # Unsharp masking
        gaussian = cv2.GaussianBlur(self.gray, (0, 0), 2.0)
        unsharp = cv2.addWeighted(self.gray, 1.5, gaussian, -0.5, 0)
        self.results['unsharp_masking'] = unsharp
        
        print("✓ Filtros de enfoque aplicados")
        
    def apply_edge_detection(self):
        """Aplica diferentes métodos de detección de bordes"""
        # Sobel X
        sobel_x = cv2.Sobel(self.gray, cv2.CV_64F, 1, 0, ksize=3)
        sobel_x = np.uint8(np.absolute(sobel_x))
        self.results['sobel_x'] = sobel_x
        
        # Sobel Y
        sobel_y = cv2.Sobel(self.gray, cv2.CV_64F, 0, 1, ksize=3)
        sobel_y = np.uint8(np.absolute(sobel_y))
        self.results['sobel_y'] = sobel_y
        
        # Sobel combinado
        sobel_combined = cv2.addWeighted(sobel_x, 0.5, sobel_y, 0.5, 0)
        self.results['sobel_combined'] = sobel_combined
        
        # Laplaciano
        laplacian = cv2.Laplacian(self.gray, cv2.CV_64F)
        laplacian = np.uint8(np.absolute(laplacian))
        self.results['laplacian'] = laplacian
        
        # Canny
        canny = cv2.Canny(self.gray, 50, 150)
        self.results['canny'] = canny
        
        print("✓ Detección de bordes completada")
        
    def create_comparison_collage(self, save_path=None):
        """Crea un collage comparativo de todos los resultados"""
        # Configurar la figura
        fig, axes = plt.subplots(3, 4, figsize=(20, 15))
        fig.suptitle('Ojos Digitales - Comparación de Filtros y Bordes', fontsize=20, fontweight='bold')
        
        # Lista de imágenes y títulos
        images = [
            (self.original_rgb, 'Original'),
            (self.results['grayscale'], 'Escala de Grises'),
            (self.results['gaussian_blur'], 'Blur Gaussiano'),
            (self.results['bilateral_blur'], 'Blur Bilateral'),
            (self.results['sharpen'], 'Enfoque'),
            (self.results['unsharp_masking'], 'Unsharp Masking'),
            (self.results['sobel_x'], 'Sobel X'),
            (self.results['sobel_y'], 'Sobel Y'),
            (self.results['sobel_combined'], 'Sobel Combinado'),
            (self.results['laplacian'], 'Laplaciano'),
            (self.results['canny'], 'Canny'),
            (self.results['average_blur'], 'Blur Promedio')
        ]
        
        # Mostrar cada imagen
        for i, (img, title) in enumerate(images):
            row = i // 4
            col = i % 4
            ax = axes[row, col]
            
            if len(img.shape) == 3:  # Imagen a color
                ax.imshow(img)
            else:  # Imagen en escala de grises
                ax.imshow(img, cmap='gray')
            
            ax.set_title(title, fontsize=12, fontweight='bold')
            ax.axis('off')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Collage guardado en: {save_path}")
        
        plt.show()
        
    def analyze_differences(self):
        """Analiza las diferencias entre los métodos de filtrado"""
        print("\n" + "="*60)
        print("ANÁLISIS DE DIFERENCIAS ENTRE MÉTODOS")
        print("="*60)
        
        # Análisis de desenfoque
        print("\n1. FILTROS DE DESENFOQUE:")
        print("   • Gaussiano: Suavizado uniforme, elimina ruido pero difumina bordes")
        print("   • Promedio: Más agresivo, puede crear artefactos")
        print("   • Bilateral: Preserva bordes mientras suaviza, mejor para fotos")
        
        # Análisis de enfoque
        print("\n2. FILTROS DE ENFOQUE:")
        print("   • Kernel de enfoque: Realza bordes pero puede crear halos")
        print("   • Unsharp Masking: Más natural, evita sobre-enfoque")
        
        # Análisis de detección de bordes
        print("\n3. DETECCIÓN DE BORDES:")
        print("   • Sobel X: Detecta bordes verticales")
        print("   • Sobel Y: Detecta bordes horizontales")
        print("   • Sobel Combinado: Detecta bordes en todas las direcciones")
        print("   • Laplaciano: Detecta cambios bruscos de intensidad")
        print("   • Canny: Más robusto, elimina ruido y conecta bordes")
        
        # Comparación de rendimiento
        print("\n4. RENDIMIENTO COMPARATIVO:")
        print("   • Sobel: Rápido, bueno para bordes simples")
        print("   • Laplaciano: Sensible al ruido, detecta detalles finos")
        print("   • Canny: Más lento pero más preciso y robusto")
        
    def save_individual_results(self, output_dir):
        """Guarda cada resultado individualmente"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        for name, img in self.results.items():
            filename = f"{name}.png"
            filepath = output_path / filename
            cv2.imwrite(str(filepath), img)
            print(f"✓ Guardado: {filepath}")
            
    def run_complete_analysis(self, output_dir="resultados"):
        """Ejecuta el análisis completo"""
        print("Iniciando análisis de Ojos Digitales...")
        print("="*50)
        
        # Cargar imagen
        self.load_image()
        
        # Aplicar filtros
        self.convert_to_grayscale()
        self.apply_blur_filters()
        self.apply_sharpen_filters()
        self.apply_edge_detection()
        
        # Crear collage
        collage_path = Path(output_dir) / "comparison_collage.png"
        self.create_comparison_collage(str(collage_path))
        
        # Guardar resultados individuales
        self.save_individual_results(output_dir)
        
        # Análisis
        self.analyze_differences()
        
        print("\n" + "="*50)
        print("✓ Análisis completo finalizado!")

def main():
    """Función principal"""
    # Crear directorio de resultados
    output_dir = Path("resultados")
    output_dir.mkdir(exist_ok=True)
    
    # Ruta de imagen de ejemplo (se puede cambiar)
    image_path = "assets/sample_image.jpg"
    
    # Si no existe la imagen de ejemplo, crear una
    if not os.path.exists(image_path):
        print("Creando imagen de ejemplo...")
        # Crear una imagen de prueba con patrones
        test_image = np.zeros((400, 600, 3), dtype=np.uint8)
        
        # Agregar formas geométricas
        cv2.rectangle(test_image, (50, 50), (200, 150), (255, 255, 255), -1)
        cv2.circle(test_image, (400, 100), 80, (128, 128, 128), -1)
        cv2.rectangle(test_image, (100, 250), (500, 350), (200, 200, 200), -1)
        
        # Agregar texto
        cv2.putText(test_image, "SAMPLE IMAGE", (200, 320), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        
        # Guardar imagen de prueba
        os.makedirs("assets", exist_ok=True)
        cv2.imwrite(image_path, test_image)
        print(f"✓ Imagen de ejemplo creada: {image_path}")
    
    # Ejecutar análisis
    ojos = OjosDigitales(image_path)
    ojos.run_complete_analysis(str(output_dir))

if __name__ == "__main__":
    main()
