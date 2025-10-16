"""
Ejercicio 6: Análisis Geométrico (Centroide, Área, Perímetro)
Extracción de métricas de contornos en imágenes binarizadas

Autor: Felipe
Fecha: 2025-01-15
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
import os
import time

class AnalizadorGeometrico:
    """Clase para análisis geométrico de contornos en imágenes"""
    
    def __init__(self):
        """Inicializa el analizador geométrico"""
        self.imagen_original = None
        self.imagen_gris = None
        self.imagen_binaria = None
        self.contornos = []
        self.metricas = []
        
    def cargar_imagen(self, ruta_imagen):
        """
        Carga una imagen desde archivo
        
        Args:
            ruta_imagen (str): Ruta al archivo de imagen
        """
        self.imagen_original = cv2.imread(ruta_imagen)
        if self.imagen_original is None:
            raise ValueError(f"No se pudo cargar la imagen: {ruta_imagen}")
        
        # Convertir a escala de grises
        self.imagen_gris = cv2.cvtColor(self.imagen_original, cv2.COLOR_BGR2GRAY)
        print(f"OK: Imagen cargada: {self.imagen_original.shape}")
        
    def generar_imagen_sintetica(self, ancho=800, alto=600):
        """
        Genera una imagen sintética con formas geométricas para demostración
        
        Args:
            ancho (int): Ancho de la imagen
            alto (int): Alto de la imagen
        """
        # Crear fondo con gradiente
        self.imagen_original = np.zeros((alto, ancho, 3), dtype=np.uint8)
        
        # Agregar gradiente de fondo (de negro a gris oscuro)
        for y in range(alto):
            for x in range(ancho):
                intensidad = int(30 * (y / alto))  # Gradiente vertical
                self.imagen_original[y, x] = [intensidad, intensidad, intensidad]
        
        # Agregar ruido sutil
        ruido = np.random.normal(0, 10, (alto, ancho, 3))
        self.imagen_original = np.clip(self.imagen_original.astype(np.float32) + ruido, 0, 255).astype(np.uint8)
        
        # Dibujar formas geométricas con variaciones de intensidad
        # Rectángulos con diferentes intensidades
        cv2.rectangle(self.imagen_original, (50, 50), (150, 150), (200, 200, 200), -1)  # Gris medio
        cv2.rectangle(self.imagen_original, (200, 100), (350, 200), (180, 180, 180), -1)  # Gris más oscuro
        
        # Círculos con gradientes internos
        cv2.circle(self.imagen_original, (500, 100), 60, (220, 220, 220), -1)
        cv2.circle(self.imagen_original, (500, 100), 40, (180, 180, 180), -1)
        cv2.circle(self.imagen_original, (500, 100), 20, (160, 160, 160), -1)
        
        cv2.circle(self.imagen_original, (650, 150), 40, (190, 190, 190), -1)
        
        # Triángulos con diferentes intensidades
        triangulo1 = np.array([[100, 300], [50, 400], [150, 400]], np.int32)
        cv2.fillPoly(self.imagen_original, [triangulo1], (210, 210, 210))
        
        triangulo2 = np.array([[250, 250], [200, 350], [300, 350]], np.int32)
        cv2.fillPoly(self.imagen_original, [triangulo2], (170, 170, 170))
        
        # Elipses con diferentes intensidades
        cv2.ellipse(self.imagen_original, (450, 300), (80, 50), 0, 0, 360, (185, 185, 185), -1)
        cv2.ellipse(self.imagen_original, (600, 350), (40, 80), 0, 0, 360, (195, 195, 195), -1)
        
        # Pentágono separado
        puntos = np.array([[100, 500], [150, 450], [200, 480], [180, 550], [120, 550]], np.int32)
        cv2.fillPoly(self.imagen_original, [puntos], (200, 200, 200))
        
        # Círculos concéntricos separados (más a la derecha)
        cv2.circle(self.imagen_original, (300, 500), 50, (205, 205, 205), -1)
        cv2.circle(self.imagen_original, (300, 500), 30, (140, 140, 140), -1)
        cv2.circle(self.imagen_original, (300, 500), 10, (220, 220, 220), -1)
        
        # Convertir a escala de grises
        self.imagen_gris = cv2.cvtColor(self.imagen_original, cv2.COLOR_BGR2GRAY)
        print(f"OK: Imagen sintética con gradientes y ruido generada: {self.imagen_original.shape}")
        
    def binarizar_imagen(self, metodo='otsu', umbral=None):
        """
        Binariza la imagen usando diferentes métodos
        
        Args:
            metodo (str): Método de binarización ('otsu', 'adaptativo', 'fijo')
            umbral (int): Umbral fijo (solo para método 'fijo')
        """
        if self.imagen_gris is None:
            raise ValueError("Primero debe cargar o generar una imagen")
        
        if metodo == 'otsu':
            _, self.imagen_binaria = cv2.threshold(self.imagen_gris, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            print("OK: Binarización con método Otsu")
            
        elif metodo == 'adaptativo':
            self.imagen_binaria = cv2.adaptiveThreshold(
                self.imagen_gris, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
            )
            print("OK: Binarización adaptativa")
            
        elif metodo == 'fijo':
            if umbral is None:
                umbral = 127
            _, self.imagen_binaria = cv2.threshold(self.imagen_gris, umbral, 255, cv2.THRESH_BINARY)
            print(f"OK: Binarización con umbral fijo: {umbral}")
            
        else:
            raise ValueError("Método debe ser 'otsu', 'adaptativo' o 'fijo'")
    
    def encontrar_contornos(self, modo=cv2.RETR_EXTERNAL, metodo=cv2.CHAIN_APPROX_SIMPLE):
        """
        Encuentra contornos en la imagen binarizada
        
        Args:
            modo: Modo de recuperación de contornos
            metodo: Método de aproximación de contornos
        """
        if self.imagen_binaria is None:
            raise ValueError("Primero debe binarizar la imagen")
        
        self.contornos, _ = cv2.findContours(
            self.imagen_binaria, modo, metodo
        )
        print(f"OK: Encontrados {len(self.contornos)} contornos")
        
    def calcular_metricas(self):
        """Calcula métricas geométricas para cada contorno"""
        if not self.contornos:
            raise ValueError("Primero debe encontrar contornos")
        
        self.metricas = []
        
        for i, contorno in enumerate(self.contornos):
            # Filtrar contornos muy pequeños
            area = cv2.contourArea(contorno)
            if area < 100:  # Ignorar contornos con área menor a 100 píxeles
                continue
                
            # Calcular métricas básicas
            perimetro = cv2.arcLength(contorno, True)
            
            # Calcular centroide usando momentos
            momentos = cv2.moments(contorno)
            if momentos['m00'] != 0:
                cx = int(momentos['m10'] / momentos['m00'])
                cy = int(momentos['m01'] / momentos['m00'])
            else:
                cx, cy = 0, 0
            
            # Rectángulo delimitador
            x, y, w, h = cv2.boundingRect(contorno)
            rect_area = w * h
            
            # Círculo mínimo envolvente
            (cx_circle, cy_circle), radius = cv2.minEnclosingCircle(contorno)
            circle_area = np.pi * radius * radius
            
            # Relación de aspecto
            aspect_ratio = float(w) / h
            
            # Extensión (proporción de área del contorno vs rectángulo delimitador)
            extent = float(area) / rect_area
            
            # Solidez (proporción de área del contorno vs convex hull)
            hull = cv2.convexHull(contorno)
            hull_area = cv2.contourArea(hull)
            solidity = float(area) / hull_area if hull_area > 0 else 0
            
            # Aproximación poligonal
            epsilon = 0.02 * perimetro
            approx = cv2.approxPolyDP(contorno, epsilon, True)
            vertices = len(approx)
            
            # Clasificación de forma
            forma = self._clasificar_forma(vertices, aspect_ratio, solidity, extent, area, perimetro)
            
            metrica = {
                'indice': i,
                'contorno': contorno,
                'area': area,
                'perimetro': perimetro,
                'centroide': (cx, cy),
                'bbox': (x, y, w, h),
                'aspect_ratio': aspect_ratio,
                'extent': extent,
                'solidity': solidity,
                'vertices': vertices,
                'forma': forma,
                'radio_circulo': radius,
                'centro_circulo': (int(cx_circle), int(cy_circle))
            }
            
            self.metricas.append(metrica)
        
        print(f"OK: Calculadas métricas para {len(self.metricas)} contornos válidos")
    
    def _clasificar_forma(self, vertices, aspect_ratio, solidity, extent, area, perimetro):
        """
        Clasifica la forma basándose en las métricas calculadas
        
        Args:
            vertices (int): Número de vértices
            aspect_ratio (float): Relación de aspecto
            solidity (float): Solidez
            extent (float): Extensión
            area (float): Área de la forma
            perimetro (float): Perímetro de la forma
            
        Returns:
            str: Tipo de forma detectada
        """
        # Calcular circularidad para mejor clasificación
        circularidad = (4 * np.pi * area) / (perimetro * perimetro) if perimetro != 0 else 0
        
        if vertices == 3:
            return "Triangulo"
        elif vertices == 4:
            if 0.9 <= aspect_ratio <= 1.1:
                return "Cuadrado"
            else:
                return "Rectangulo"
        elif vertices == 5:
            return "Pentagono"
        elif vertices == 6:
            return "Hexagono"
        elif vertices >= 8:
            # Para formas con muchos vértices, usar circularidad y relación de aspecto
            # Criterio más estricto: solo círculos perfectos
            if circularidad > 0.85 and solidity > 0.95 and 0.98 <= aspect_ratio <= 1.02:
                return "Circulo"
            elif circularidad > 0.5 and solidity > 0.7:
                return "Ovalo/Elipse"
            else:
                return "Poligono Regular"
        else:
            if circularidad > 0.8:
                return "Poligono Regular"
            else:
                return "Forma Irregular"
    
    def visualizar_resultados(self, mostrar_contornos=True, mostrar_metricas=True):
        """
        Visualiza los resultados del análisis geométrico
        
        Args:
            mostrar_contornos (bool): Si mostrar contornos detectados
            mostrar_metricas (bool): Si mostrar métricas sobre la imagen
        """
        if not self.metricas:
            raise ValueError("Primero debe calcular las métricas")
        
        # Crear imagen de resultado
        resultado = self.imagen_original.copy()
        
        # Colores para diferentes formas
        colores_formas = {
            "Triangulo": (0, 255, 0),      # Verde
            "Cuadrado": (255, 0, 0),       # Azul
            "Rectangulo": (0, 0, 255),     # Rojo
            "Circulo": (255, 255, 0),      # Cian
            "Ovalo/Elipse": (255, 0, 255), # Magenta
            "Pentagono": (0, 255, 255),    # Amarillo
            "Hexagono": (128, 0, 128),     # Púrpura
            "Poligono Regular": (255, 165, 0), # Naranja
            "Forma Irregular": (128, 128, 128) # Gris
        }
        
        for metrica in self.metricas:
            contorno = metrica['contorno']
            forma = metrica['forma']
            color = colores_formas.get(forma, (255, 255, 255))
            
            # Obtener coordenadas del bounding box para uso posterior
            x, y, w, h = metrica['bbox']
            
            if mostrar_contornos:
                # Dibujar contorno
                cv2.drawContours(resultado, [contorno], -1, color, 2)
                
                # Dibujar rectángulo delimitador
                cv2.rectangle(resultado, (x, y), (x + w, y + h), color, 1)
                
                # Dibujar círculo mínimo envolvente
                cv2.circle(resultado, metrica['centro_circulo'], int(metrica['radio_circulo']), color, 1)
            
            if mostrar_metricas:
                # Dibujar centroide
                cx, cy = metrica['centroide']
                cv2.circle(resultado, (cx, cy), 5, (0, 0, 0), -1)
                cv2.circle(resultado, (cx, cy), 3, (255, 255, 255), -1)
                
                # Agregar texto con información
                texto = f"{forma} A:{int(metrica['area'])}"
                # Asegurar que el texto esté dentro del área visible
                texto_y = max(y - 10, 20)  # Mínimo 20 píxeles desde el borde superior
                
                # Obtener el tamaño del texto para crear un fondo
                (text_width, text_height), baseline = cv2.getTextSize(texto, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                
                # Dibujar fondo para el texto
                cv2.rectangle(resultado, (x, texto_y - text_height - 5), (x + text_width + 5, texto_y + 5), (0, 0, 0), -1)
                cv2.rectangle(resultado, (x, texto_y - text_height - 5), (x + text_width + 5, texto_y + 5), color, 1)
                
                # Dibujar el texto
                cv2.putText(resultado, texto, (x + 2, texto_y - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        return resultado
    
    def generar_reporte(self):
        """Genera un reporte detallado de las métricas calculadas"""
        if not self.metricas:
            raise ValueError("Primero debe calcular las métricas")
        
        print("\n" + "="*60)
        print("REPORTE DE ANÁLISIS GEOMÉTRICO")
        print("="*60)
        
        for i, metrica in enumerate(self.metricas):
            print(f"\n--- CONTORNO {i+1} ---")
            print(f"Forma detectada: {metrica['forma']}")
            print(f"Área: {metrica['area']:.2f} píxeles²")
            print(f"Perímetro: {metrica['perimetro']:.2f} píxeles")
            print(f"Centroide: ({metrica['centroide'][0]}, {metrica['centroide'][1]})")
            print(f"Vértices: {metrica['vertices']}")
            print(f"Relación de aspecto: {metrica['aspect_ratio']:.3f}")
            print(f"Extensión: {metrica['extent']:.3f}")
            print(f"Solidez: {metrica['solidity']:.3f}")
            print(f"Bounding Box: {metrica['bbox']}")
            print(f"Radio círculo mínimo: {metrica['radio_circulo']:.2f}")
        
        # Estadísticas generales
        print(f"\n--- ESTADÍSTICAS GENERALES ---")
        print(f"Total de formas detectadas: {len(self.metricas)}")
        
        # Conteo por tipo de forma
        conteo_formas = {}
        for metrica in self.metricas:
            forma = metrica['forma']
            conteo_formas[forma] = conteo_formas.get(forma, 0) + 1
        
        print("\nDistribución por tipo de forma:")
        for forma, cantidad in conteo_formas.items():
            print(f"  {forma}: {cantidad}")
        
        # Área total y promedio
        area_total = sum(m['area'] for m in self.metricas)
        area_promedio = area_total / len(self.metricas)
        print(f"\nÁrea total: {area_total:.2f} píxeles²")
        print(f"Área promedio: {area_promedio:.2f} píxeles²")

def demostrar_analisis_geometrico():
    """Función principal que demuestra el análisis geométrico"""
    
    print("=== DEMOSTRACIÓN DE ANÁLISIS GEOMÉTRICO ===\n")
    
    # Crear analizador
    analizador = AnalizadorGeometrico()
    
    # 1. Generar imagen sintética
    print("1. Generando imagen sintética con formas geométricas...")
    analizador.generar_imagen_sintetica()
    
    # Guardar imagen original
    cv2.imwrite("00_imagen_original.png", analizador.imagen_original)
    
    # 2. Binarización con diferentes métodos
    print("\n2. Aplicando binarización...")
    
    # Método Otsu
    analizador.binarizar_imagen('otsu')
    cv2.imwrite("01_binarizacion_otsu.png", analizador.imagen_binaria)
    
    # Método adaptativo
    analizador.binarizar_imagen('adaptativo')
    cv2.imwrite("02_binarizacion_adaptativa.png", analizador.imagen_binaria)
    
    # Método fijo
    analizador.binarizar_imagen('fijo', 127)
    cv2.imwrite("03_binarizacion_fija.png", analizador.imagen_binaria)
    
    # 3. Detección de contornos
    print("\n3. Detectando contornos...")
    analizador.encontrar_contornos()
    
    # 4. Cálculo de métricas
    print("\n4. Calculando métricas geométricas...")
    analizador.calcular_metricas()
    
    # 5. Visualización de resultados
    print("\n5. Generando visualizaciones...")
    
    # Crear imagen comparativa de las 3 binarizaciones
    print("Creando comparativa de binarizaciones...")
    
    # Cargar las 3 imágenes binarizadas
    img_otsu = cv2.imread("01_binarizacion_otsu.png")
    img_adaptativa = cv2.imread("02_binarizacion_adaptativa.png")
    img_fija = cv2.imread("03_binarizacion_fija.png")
    
    # Redimensionar para que tengan el mismo tamaño
    alto, ancho = img_otsu.shape[:2]
    img_adaptativa = cv2.resize(img_adaptativa, (ancho, alto))
    img_fija = cv2.resize(img_fija, (ancho, alto))
    
    # Crear imagen horizontal con las 3 binarizaciones
    comparativa_binarizaciones = np.hstack([img_otsu, img_adaptativa, img_fija])
    
    # Agregar títulos
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.8
    color = (255, 255, 255)
    thickness = 2
    
    cv2.putText(comparativa_binarizaciones, "Otsu", (50, 30), font, font_scale, color, thickness)
    cv2.putText(comparativa_binarizaciones, "Adaptativa", (ancho + 50, 30), font, font_scale, color, thickness)
    cv2.putText(comparativa_binarizaciones, "Umbral Fijo (127)", (2*ancho + 50, 30), font, font_scale, color, thickness)
    
    cv2.imwrite("04_comparativa_binarizaciones.png", comparativa_binarizaciones)
    
    # Imagen con contornos y métricas (usando Otsu)
    resultado_completo = analizador.visualizar_resultados(mostrar_contornos=True, mostrar_metricas=True)
    cv2.imwrite("05_analisis_completo.png", resultado_completo)
    
    # Solo contornos
    resultado_contornos = analizador.visualizar_resultados(mostrar_contornos=True, mostrar_metricas=False)
    cv2.imwrite("06_solo_contornos.png", resultado_contornos)
    
    # Solo métricas
    resultado_metricas = analizador.visualizar_resultados(mostrar_contornos=False, mostrar_metricas=True)
    cv2.imwrite("07_solo_metricas.png", resultado_metricas)
    
    # 6. Generar reporte
    print("\n6. Generando reporte detallado...")
    analizador.generar_reporte()
    
    # 7. Crear visualización con matplotlib
    print("\n7. Creando visualización avanzada...")
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Análisis Geométrico Completo', fontsize=16, fontweight='bold')
    
    # Imagen original
    axes[0, 0].imshow(cv2.cvtColor(analizador.imagen_original, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title('Imagen Original')
    axes[0, 0].axis('off')
    
    # Imagen binarizada
    axes[0, 1].imshow(analizador.imagen_binaria, cmap='gray')
    axes[0, 1].set_title('Imagen Binarizada (Otsu)')
    axes[0, 1].axis('off')
    
    # Resultado completo
    axes[0, 2].imshow(cv2.cvtColor(resultado_completo, cv2.COLOR_BGR2RGB))
    axes[0, 2].set_title('Análisis Completo')
    axes[0, 2].axis('off')
    
    # Gráfico de áreas
    areas = [m['area'] for m in analizador.metricas]
    formas = [m['forma'] for m in analizador.metricas]
    axes[1, 0].bar(range(len(areas)), areas, color='skyblue', edgecolor='navy')
    axes[1, 0].set_title('Áreas de las Formas Detectadas')
    axes[1, 0].set_xlabel('Índice de Forma')
    axes[1, 0].set_ylabel('Área (píxeles²)')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Gráfico de perímetros
    perimetros = [m['perimetro'] for m in analizador.metricas]
    axes[1, 1].bar(range(len(perimetros)), perimetros, color='lightcoral', edgecolor='darkred')
    axes[1, 1].set_title('Perímetros de las Formas Detectadas')
    axes[1, 1].set_xlabel('Índice de Forma')
    axes[1, 1].set_ylabel('Perímetro (píxeles)')
    axes[1, 1].grid(True, alpha=0.3)
    
    # Gráfico de distribución de formas
    conteo_formas = {}
    for forma in formas:
        conteo_formas[forma] = conteo_formas.get(forma, 0) + 1
    
    axes[1, 2].pie(conteo_formas.values(), labels=conteo_formas.keys(), autopct='%1.1f%%', startangle=90)
    axes[1, 2].set_title('Distribucion de Tipos de Formas')
    
    plt.tight_layout()
    plt.savefig("08_analisis_estadistico.png", dpi=300, bbox_inches='tight')
    plt.show()
    
    print("\n" + "="*60)
    print("OK: ANÁLISIS GEOMÉTRICO COMPLETADO")
    print("="*60)
    print("\nArchivos generados:")
    print("- 00_imagen_original.png")
    print("- 01_binarizacion_otsu.png")
    print("- 02_binarizacion_adaptativa.png")
    print("- 03_binarizacion_fija.png")
    print("- 04_comparativa_binarizaciones.png")
    print("- 05_analisis_completo.png")
    print("- 06_solo_contornos.png")
    print("- 07_solo_metricas.png")
    print("- 08_analisis_estadistico.png")
    
    print("\nMétricas calculadas:")
    print("- Área y perímetro de cada forma")
    print("- Centroides usando momentos")
    print("- Bounding boxes y círculos mínimos")
    print("- Clasificación automática de formas")
    print("- Análisis estadístico completo")

if __name__ == "__main__":
    # Crear directorio de resultados
    os.makedirs("resultados", exist_ok=True)
    demostrar_analisis_geometrico()
