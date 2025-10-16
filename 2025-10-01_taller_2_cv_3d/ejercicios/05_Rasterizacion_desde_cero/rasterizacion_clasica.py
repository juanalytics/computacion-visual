"""
Ejercicio 5: Rasterización desde Cero
Implementación de algoritmos clásicos de rasterización:
- Algoritmo de Bresenham para líneas
- Algoritmo del punto medio para círculos
- Algoritmo scanline para relleno de triángulos

Autor: Felipe
Fecha: 2025-01-15
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import math

class Rasterizador:
    """Clase principal para implementar algoritmos de rasterización clásicos"""
    
    def __init__(self, width=800, height=600):
        """
        Inicializa el rasterizador con un canvas de dimensiones específicas
        
        Args:
            width (int): Ancho del canvas en píxeles
            height (int): Alto del canvas en píxeles
        """
        self.width = width
        self.height = height
        self.canvas = np.zeros((height, width, 3), dtype=np.uint8)
        self.clear_canvas()
    
    def clear_canvas(self, color=(0, 0, 0)):
        """
        Limpia el canvas con un color específico
        
        Args:
            color (tuple): Color RGB (R, G, B) de 0-255
        """
        self.canvas.fill(color[0])
        self.canvas[:, :, 1] = color[1]
        self.canvas[:, :, 2] = color[2]
    
    def set_pixel(self, x, y, color=(255, 255, 255)):
        """
        Establece un píxel en las coordenadas dadas
        
        Args:
            x (int): Coordenada X
            y (int): Coordenada Y
            color (tuple): Color RGB (R, G, B)
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            self.canvas[y, x] = color
    
    def bresenham_line(self, x0, y0, x1, y1, color=(255, 255, 255)):
        """
        Algoritmo de Bresenham para dibujar líneas
        
        Args:
            x0, y0 (int): Coordenadas del punto inicial
            x1, y1 (int): Coordenadas del punto final
            color (tuple): Color RGB de la línea
        """
        # Intercambiar puntos si es necesario para manejar todas las direcciones
        if abs(y1 - y0) > abs(x1 - x0):
            # Línea más vertical que horizontal
            x0, y0, x1, y1 = y0, x0, y1, x1
            steep = True
        else:
            steep = False
        
        # Asegurar que x0 < x1
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        
        dx = x1 - x0
        dy = abs(y1 - y0)
        error = dx / 2
        y_step = 1 if y1 > y0 else -1
        y = y0
        
        for x in range(x0, x1 + 1):
            if steep:
                self.set_pixel(y, x, color)
            else:
                self.set_pixel(x, y, color)
            
            error -= dy
            if error < 0:
                y += y_step
                error += dx
    
    def midpoint_circle(self, center_x, center_y, radius, color=(255, 255, 255)):
        """
        Algoritmo del punto medio para dibujar círculos
        
        Args:
            center_x, center_y (int): Coordenadas del centro del círculo
            radius (int): Radio del círculo
            color (tuple): Color RGB del círculo
        """
        x = radius
        y = 0
        decision = 1 - radius
        
        # Dibujar los puntos iniciales
        self._draw_circle_points(center_x, center_y, x, y, color)
        
        while x > y:
            y += 1
            
            # Decidir si mover x hacia adentro
            if decision <= 0:
                decision += 2 * y + 1
            else:
                x -= 1
                decision += 2 * (y - x) + 1
            
            self._draw_circle_points(center_x, center_y, x, y, color)
    
    def _draw_circle_points(self, cx, cy, x, y, color):
        """
        Dibuja los 8 puntos simétricos de un círculo
        
        Args:
            cx, cy (int): Centro del círculo
            x, y (int): Coordenadas relativas del punto
            color (tuple): Color RGB
        """
        points = [
            (cx + x, cy + y), (cx - x, cy + y),
            (cx + x, cy - y), (cx - x, cy - y),
            (cx + y, cy + x), (cx - y, cy + x),
            (cx + y, cy - x), (cx - y, cy - x)
        ]
        
        for px, py in points:
            self.set_pixel(px, py, color)
    
    def scanline_triangle(self, vertices, color=(255, 255, 255)):
        """
        Algoritmo scanline para relleno de triángulos
        
        Args:
            vertices (list): Lista de 3 tuplas (x, y) con las coordenadas de los vértices
            color (tuple): Color RGB del triángulo
        """
        if len(vertices) != 3:
            raise ValueError("El triángulo debe tener exactamente 3 vértices")
        
        # Ordenar vértices por Y (de menor a mayor)
        vertices_sorted = sorted(vertices, key=lambda v: v[1])
        v1, v2, v3 = vertices_sorted
        
        # Dividir el triángulo en dos partes: superior e inferior
        # Parte superior: v1 -> v2 -> v3
        self._fill_triangle_half(v1, v2, v3, color)
        
        # Parte inferior: v2 -> v3
        self._fill_triangle_half(v2, v3, v3, color)
    
    def _fill_triangle_half(self, v1, v2, v3, color):
        """
        Rellena la mitad superior o inferior de un triángulo
        
        Args:
            v1, v2, v3 (tuple): Vértices del triángulo ordenados por Y
            color (tuple): Color RGB
        """
        # Calcular las pendientes de los bordes
        if v2[1] - v1[1] != 0:
            slope_left = (v2[0] - v1[0]) / (v2[1] - v1[1])
        else:
            slope_left = 0
            
        if v3[1] - v1[1] != 0:
            slope_right = (v3[0] - v1[0]) / (v3[1] - v1[1])
        else:
            slope_right = 0
        
        # Rellenar línea por línea
        y_start = int(v1[1])
        y_end = int(v2[1])
        
        for y in range(y_start, y_end + 1):
            if y - v1[1] != 0:
                x_left = v1[0] + slope_left * (y - v1[1])
                x_right = v1[0] + slope_right * (y - v1[1])
                
                # Asegurar que left <= right
                if x_left > x_right:
                    x_left, x_right = x_right, x_left
                
                # Dibujar la línea horizontal
                for x in range(int(x_left), int(x_right) + 1):
                    self.set_pixel(x, y, color)
    
    def save_image(self, filename):
        """
        Guarda el canvas como una imagen
        
        Args:
            filename (str): Nombre del archivo de imagen
        """
        img = Image.fromarray(self.canvas)
        img.save(filename)
        print(f"Imagen guardada como: {filename}")
    
    def show_image(self, title="Rasterización"):
        """
        Muestra la imagen usando matplotlib
        
        Args:
            title (str): Título de la ventana
        """
        plt.figure(figsize=(12, 9))
        plt.imshow(self.canvas)
        plt.title(title, fontsize=16, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.show()

def demostrar_algoritmos():
    """Función principal que demuestra todos los algoritmos de rasterización"""
    
    print("=== DEMOSTRACIÓN DE ALGORITMOS DE RASTERIZACIÓN CLÁSICOS ===\n")
    
    # Crear rasterizador
    raster = Rasterizador(800, 600)
    
    # 1. DEMOSTRACIÓN DE LÍNEAS (Bresenham)
    print("1. Dibujando líneas con algoritmo de Bresenham...")
    raster.clear_canvas()
    
    # Líneas de diferentes ángulos y colores
    raster.bresenham_line(100, 100, 700, 150, (255, 0, 0))      # Rojo - horizontal
    raster.bresenham_line(100, 200, 700, 500, (0, 255, 0))      # Verde - diagonal
    raster.bresenham_line(400, 50, 400, 550, (0, 0, 255))       # Azul - vertical
    raster.bresenham_line(50, 300, 750, 300, (255, 255, 0))     # Amarillo - horizontal
    raster.bresenham_line(100, 550, 700, 100, (255, 0, 255))    # Magenta - diagonal inversa
    
    # Agregar título
    raster.set_pixel(350, 20, (255, 255, 255))
    
    raster.save_image("01_lineas_bresenham.png")
    raster.show_image("Algoritmo de Bresenham - Líneas")
    
    # 2. DEMOSTRACIÓN DE CÍRCULOS (Punto Medio)
    print("\n2. Dibujando círculos con algoritmo del punto medio...")
    raster.clear_canvas()
    
    # Círculos de diferentes tamaños y colores
    raster.midpoint_circle(200, 200, 80, (255, 0, 0))           # Rojo - grande
    raster.midpoint_circle(500, 200, 60, (0, 255, 0))           # Verde - mediano
    raster.midpoint_circle(350, 400, 40, (0, 0, 255))           # Azul - pequeño
    raster.midpoint_circle(600, 400, 100, (255, 255, 0))        # Amarillo - muy grande
    raster.midpoint_circle(150, 450, 30, (255, 0, 255))         # Magenta - pequeño
    
    # Patrón de círculos concéntricos
    for i in range(5):
        radius = 20 + i * 15
        color_intensity = 255 - i * 40
        raster.midpoint_circle(400, 300, radius, (color_intensity, color_intensity, color_intensity))
    
    raster.save_image("02_circulos_punto_medio.png")
    raster.show_image("Algoritmo del Punto Medio - Círculos")
    
    # 3. DEMOSTRACIÓN DE TRIÁNGULOS (Scanline)
    print("\n3. Dibujando triángulos con algoritmo scanline...")
    raster.clear_canvas()
    
    # Triángulos de diferentes formas y colores
    triangulo1 = [(200, 150), (150, 250), (250, 250)]
    raster.scanline_triangle(triangulo1, (255, 0, 0))
    
    triangulo2 = [(400, 100), (350, 200), (450, 200)]
    raster.scanline_triangle(triangulo2, (0, 255, 0))
    
    triangulo3 = [(600, 200), (550, 300), (650, 300)]
    raster.scanline_triangle(triangulo3, (0, 0, 255))
    
    # Triángulo más complejo
    triangulo4 = [(300, 350), (200, 500), (400, 500)]
    raster.scanline_triangle(triangulo4, (255, 255, 0))
    
    # Triángulo isósceles
    triangulo5 = [(500, 400), (450, 550), (550, 550)]
    raster.scanline_triangle(triangulo5, (255, 0, 255))
    
    raster.save_image("03_triangulos_scanline.png")
    raster.show_image("Algoritmo Scanline - Triángulos")
    
    # 4. DEMOSTRACIÓN COMBINADA
    print("\n4. Creando composición final...")
    raster.clear_canvas()
    
    # Fondo con líneas
    for i in range(0, 600, 50):
        raster.bresenham_line(0, i, 800, i, (20, 20, 20))
    
    # Círculos decorativos
    for i in range(5):
        x = 100 + i * 150
        y = 100
        raster.midpoint_circle(x, y, 30, (100, 100, 255))
    
    # Triángulos principales
    triangulo_principal = [(400, 200), (300, 400), (500, 400)]
    raster.scanline_triangle(triangulo_principal, (255, 100, 100))
    
    # Círculo central
    raster.midpoint_circle(400, 300, 80, (100, 255, 100))
    
    # Líneas de conexión
    raster.bresenham_line(400, 200, 400, 300, (255, 255, 255))
    
    raster.save_image("04_composicion_final.png")
    raster.show_image("Composición Final - Todos los Algoritmos")
    
    print("\n=== ANÁLISIS COMPARATIVO ===")
    print("1. ALGORITMO DE BRESENHAM (Líneas):")
    print("   ✓ Ventajas: Rápido, usa solo operaciones enteras, preciso")
    print("   ✓ Desventajas: Limitado a líneas rectas")
    print("   ✓ Eficiencia: O(n) donde n = max(|x1-x0|, |y1-y0|)")
    
    print("\n2. ALGORITMO DEL PUNTO MEDIO (Círculos):")
    print("   ✓ Ventajas: Simétrico, eficiente, usa solo operaciones enteras")
    print("   ✓ Desventajas: Solo círculos perfectos")
    print("   ✓ Eficiencia: O(π×r) donde r es el radio")
    
    print("\n3. ALGORITMO SCANLINE (Triángulos):")
    print("   ✓ Ventajas: Relleno eficiente, maneja formas complejas")
    print("   ✓ Desventajas: Más complejo, requiere ordenamiento")
    print("   ✓ Eficiencia: O(n×m) donde n es altura, m es ancho promedio")
    
    print("\n=== REFLEXIÓN FINAL ===")
    print("Estos algoritmos clásicos forman la base de la rasterización moderna.")
    print("Aunque las GPUs usan métodos más sofisticados, entender estos")
    print("algoritmos fundamentales es crucial para comprender cómo se")
    print("generan las imágenes en computadoras.")

if __name__ == "__main__":
    demostrar_algoritmos()
