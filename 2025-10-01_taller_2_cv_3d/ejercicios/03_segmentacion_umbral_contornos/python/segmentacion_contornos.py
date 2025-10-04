"""
Ejercicio 3: Segmentando el Mundo - Binarización y Contornos
Taller: Computación Visual & 3D

Objetivo: Umbralización (fija y adaptativa) y detección de formas.
Implementa threshold, adaptiveThreshold, findContours, dibujar contornos,
calcular centroides (momentos), área, perímetro, y clasificar por vértices.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import os
import imageio

class SegmentacionContornos:
    def __init__(self, image_path):
        """
        Inicializa el procesador de segmentación con OpenCV
        
        Args:
            image_path (str): Ruta a la imagen de entrada
        """
        self.image_path = image_path
        self.original = None
        self.gray = None
        self.results = {}
        self.contours = []
        self.hierarchy = None
        
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
        
    def apply_thresholding(self):
        """Aplica diferentes métodos de umbralización"""
        # Threshold fijo
        _, thresh_fixed = cv2.threshold(self.gray, 127, 255, cv2.THRESH_BINARY)
        self.results['thresh_fixed'] = thresh_fixed
        
        # Threshold adaptativo - Media (con parámetros más pequeños y THRESH_BINARY_INV)
        thresh_adaptive_mean = cv2.adaptiveThreshold(
            self.gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2
        )
        self.results['thresh_adaptive_mean'] = thresh_adaptive_mean
        
        # Threshold adaptativo - Gaussiano (con parámetros más pequeños y THRESH_BINARY_INV)
        thresh_adaptive_gaussian = cv2.adaptiveThreshold(
            self.gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
        )
        self.results['thresh_adaptive_gaussian'] = thresh_adaptive_gaussian
        
        # Otsu's thresholding
        _, thresh_otsu = cv2.threshold(self.gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        self.results['thresh_otsu'] = thresh_otsu
        
        print("✓ Umbralización completada")
        
    def find_contours(self, thresh_image):
        """Encuentra contornos en la imagen umbralizada"""
        # Encontrar contornos
        contours, hierarchy = cv2.findContours(
            thresh_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        
        # Filtrar contornos por área mínima (eliminar contornos muy grandes que son el fondo)
        min_area = 500  # Área mínima para considerar un contorno
        filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]
        
        self.contours = filtered_contours
        self.hierarchy = hierarchy
        
        print(f"✓ Encontrados {len(filtered_contours)} contornos (filtrados de {len(contours)})")
        return filtered_contours
        
    def calculate_contour_properties(self, contours):
        """Calcula propiedades de los contornos"""
        properties = []
        
        for i, contour in enumerate(contours):
            # Área
            area = cv2.contourArea(contour)
            
            # Perímetro
            perimeter = cv2.arcLength(contour, True)
            
            # Centroide (momentos)
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
            else:
                cx, cy = 0, 0
            
            # Aproximación de polígono
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            vertices = len(approx)
            
            # Clasificación por forma
            if vertices == 3:
                shape = "Triángulo"
            elif vertices == 4:
                shape = "Cuadrado/Rectángulo"
            elif vertices > 8:
                shape = "Círculo/Óvalo"
            else:
                shape = f"Polígono ({vertices} lados)"
            
            properties.append({
                'index': i,
                'area': area,
                'perimeter': perimeter,
                'centroid': (cx, cy),
                'vertices': vertices,
                'shape': shape,
                'contour': contour
            })
        
        return properties
        
    def draw_contours_and_properties(self, thresh_image, properties, title_suffix=""):
        """Dibuja contornos y sus propiedades"""
        # Crear imagen base
        result_image = self.original_rgb.copy()
        
        # Dibujar contornos
        cv2.drawContours(result_image, [prop['contour'] for prop in properties], -1, (0, 255, 0), 2)
        
        # Dibujar centroides y etiquetas
        for prop in properties:
            cx, cy = prop['centroid']
            
            # Dibujar centroide
            cv2.circle(result_image, (cx, cy), 5, (255, 0, 0), -1)
            
            # Dibujar caja delimitadora
            x, y, w, h = cv2.boundingRect(prop['contour'])
            cv2.rectangle(result_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            
            # Etiqueta con información
            label = f"{prop['shape']} A:{int(prop['area'])}"
            cv2.putText(result_image, label, (x, y - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        return result_image
        
    def create_comparison_visualization(self):
        """Crea visualización comparativa de todos los métodos"""
        # Configurar la figura
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Segmentando el Mundo - Binarización y Contornos', fontsize=20, fontweight='bold')
        
        # Lista de métodos a comparar
        methods = [
            ('thresh_fixed', 'Threshold Fijo'),
            ('thresh_adaptive_mean', 'Adaptativo (Media)'),
            ('thresh_adaptive_gaussian', 'Adaptativo (Gaussiano)'),
            ('thresh_otsu', 'Otsu'),
        ]
        
        # Mostrar cada método
        for i, (method_key, method_name) in enumerate(methods):
            row = i // 3
            col = i % 3
            
            if method_key in self.results:
                thresh_image = self.results[method_key]
                
                # Encontrar contornos
                contours = self.find_contours(thresh_image)
                
                # Calcular propiedades
                properties = self.calculate_contour_properties(contours)
                
                # Dibujar resultado
                result_image = self.draw_contours_and_properties(thresh_image, properties)
                
                # Mostrar imagen
                axes[row, col].imshow(result_image)
                axes[row, col].set_title(f'{method_name}\nContornos: {len(contours)}', fontsize=12, fontweight='bold')
                axes[row, col].axis('off')
        
        # Mostrar imagen original en la posición (1,1)
        axes[1, 1].imshow(self.original_rgb)
        axes[1, 1].set_title('Imagen Original', fontsize=12, fontweight='bold')
        axes[1, 1].axis('off')
        
        # Ocultar el subplot vacío en (1,2)
        axes[1, 2].axis('off')
        
        plt.tight_layout()
        return fig
        
    def create_animated_gif(self, output_path):
        """Crea un GIF animado mostrando el proceso"""
        frames = []
        
        # Imagen original
        frames.append(self.original_rgb)
        
        # Para cada método de umbralización
        methods = [
            ('thresh_fixed', 'Threshold Fijo'),
            ('thresh_adaptive_mean', 'Adaptativo (Media)'),
            ('thresh_adaptive_gaussian', 'Adaptativo (Gaussiano)'),
            ('thresh_otsu', 'Otsu'),
        ]
        
        for method_key, method_name in methods:
            if method_key in self.results:
                thresh_image = self.results[method_key]
                contours = self.find_contours(thresh_image)
                properties = self.calculate_contour_properties(contours)
                result_image = self.draw_contours_and_properties(thresh_image, properties)
                frames.append(result_image)
        
        # Guardar GIF
        imageio.mimsave(output_path, frames, duration=1.5)
        print(f"✓ GIF animado guardado en: {output_path}")
        
    def analyze_thresholding_methods(self):
        """Analiza las diferencias entre métodos de umbralización"""
        print("\n" + "="*60)
        print("ANÁLISIS DE MÉTODOS DE UMBRALIZACIÓN")
        print("="*60)
        
        methods = [
            ('thresh_fixed', 'Threshold Fijo'),
            ('thresh_adaptive_mean', 'Adaptativo (Media)'),
            ('thresh_adaptive_gaussian', 'Adaptativo (Gaussiano)'),
            ('thresh_otsu', 'Otsu'),
        ]
        
        print("\nComparación de métodos:")
        print("-" * 50)
        
        for method_key, method_name in methods:
            if method_key in self.results:
                thresh_image = self.results[method_key]
                contours = self.find_contours(thresh_image)
                properties = self.calculate_contour_properties(contours)
                
                total_area = sum(prop['area'] for prop in properties)
                avg_area = total_area / len(properties) if properties else 0
                
                print(f"{method_name:20} | Contornos: {len(contours):3d} | Área total: {total_area:8.0f} | Área promedio: {avg_area:6.0f}")
        
        print("\nCaracterísticas de cada método:")
        print("• Threshold Fijo: Simple, rápido, pero no se adapta a la iluminación")
        print("• Adaptativo (Media): Se adapta a la iluminación local, bueno para imágenes con variaciones")
        print("• Adaptativo (Gaussiano): Similar al anterior pero con peso gaussiano, más suave")
        print("• Otsu: Automático, encuentra el umbral óptimo basado en histograma")
        
    def save_individual_results(self, output_dir):
        """Guarda cada resultado individualmente"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Guardar imágenes umbralizadas
        for name, img in self.results.items():
            filename = f"{name}.png"
            filepath = output_path / filename
            cv2.imwrite(str(filepath), img)
            print(f"✓ Guardado: {filepath}")
            
    def run_complete_analysis(self, output_dir="../resultados"):
        """Ejecuta el análisis completo"""
        print("Iniciando análisis de Segmentación y Contornos...")
        print("="*50)
        
        # Cargar imagen
        self.load_image()
        
        # Aplicar filtros
        self.convert_to_grayscale()
        self.apply_thresholding()
        
        # Crear visualización comparativa
        fig = self.create_comparison_visualization()
        comparison_path = Path(output_dir) / "comparison_segmentation.png"
        fig.savefig(str(comparison_path), dpi=300, bbox_inches='tight')
        print(f"✓ Comparación guardada en: {comparison_path}")
        plt.show()
        
        # Crear GIF animado
        gif_path = Path(output_dir) / "segmentacion_proceso.gif"
        self.create_animated_gif(str(gif_path))
        
        # Guardar resultados individuales
        self.save_individual_results(output_dir)
        
        # Análisis
        self.analyze_thresholding_methods()
        
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
        # Crear una imagen de prueba con formas geométricas
        test_image = np.zeros((400, 600, 3), dtype=np.uint8)
        
        # Agregar formas geométricas de diferentes colores con mejor contraste
        # Rectángulo blanco
        cv2.rectangle(test_image, (50, 50), (200, 150), (255, 255, 255), -1)
        
        # Círculo gris oscuro
        cv2.circle(test_image, (400, 100), 80, (80, 80, 80), -1)
        
        # Triángulo (usando polígono) - gris medio
        triangle_pts = np.array([[300, 250], [200, 350], [400, 350]], np.int32)
        cv2.fillPoly(test_image, [triangle_pts], (120, 120, 120), -1)
        
        # Rectángulo con borde - gris claro
        cv2.rectangle(test_image, (100, 250), (500, 350), (180, 180, 180), -1)
        cv2.rectangle(test_image, (100, 250), (500, 350), (0, 0, 0), 3)
        
        # Agregar más formas para mejor detección
        # Círculo pequeño
        cv2.circle(test_image, (150, 300), 30, (60, 60, 60), -1)
        
        # Rectángulo pequeño
        cv2.rectangle(test_image, (450, 300), (500, 330), (90, 90, 90), -1)
        
        # Agregar texto
        cv2.putText(test_image, "SHAPES", (250, 320), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        
        # Guardar imagen de prueba
        os.makedirs("../assets", exist_ok=True)
        cv2.imwrite(image_path, test_image)
        print(f"✓ Imagen de ejemplo creada: {image_path}")
    
    # Ejecutar análisis
    segmentador = SegmentacionContornos(image_path)
    segmentador.run_complete_analysis(str(output_dir))

if __name__ == "__main__":
    main()
