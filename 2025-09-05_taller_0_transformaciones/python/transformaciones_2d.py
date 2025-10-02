"""
Taller 0 - Transformaciones Básicas en Python
Implementación de transformaciones geométricas 2D con matplotlib y numpy
Autor: [Tu nombre]
Fecha: 2025-09-05
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Polygon
import imageio
import os

class TransformacionesBasicas:
    def __init__(self):
        """Inicializa la clase con una figura básica (triángulo)"""
        # Definir un triángulo básico
        self.figura_original = np.array([
            [0, 1, 0.5, 0],    # x coordinates
            [0, 0, 1, 0]       # y coordinates
        ])
        
        # Configurar la figura de matplotlib
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.ax.set_xlim(-3, 3)
        self.ax.set_ylim(-3, 3)
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.3)
        self.ax.set_title('Transformaciones Geométricas 2D - Hola Mundo Visual')
        
        # Lista para almacenar frames de animación
        self.frames = []
    
    def matriz_traslacion(self, tx, ty):
        """Crea matriz de traslación homogénea"""
        return np.array([
            [1, 0, tx],
            [0, 1, ty],
            [0, 0, 1]
        ])
    
    def matriz_rotacion(self, angulo):
        """Crea matriz de rotación homogénea (ángulo en radianes)"""
        cos_a = np.cos(angulo)
        sin_a = np.sin(angulo)
        return np.array([
            [cos_a, -sin_a, 0],
            [sin_a, cos_a, 0],
            [0, 0, 1]
        ])
    
    def matriz_escala(self, sx, sy):
        """Crea matriz de escala homogénea"""
        return np.array([
            [sx, 0, 0],
            [0, sy, 0],
            [0, 0, 1]
        ])
    
    def aplicar_transformacion(self, figura, matriz):
        """Aplica una transformación a la figura usando coordenadas homogéneas"""
        # Convertir a coordenadas homogéneas
        figura_homogenea = np.vstack([figura, np.ones(figura.shape[1])])
        
        # Aplicar transformación
        figura_transformada = matriz @ figura_homogenea
        
        # Retornar coordenadas cartesianas
        return figura_transformada[:2, :]
    
    def dibujar_figura(self, figura, color='blue', alpha=0.7, label=''):
        """Dibuja una figura en el plot actual"""
        # Crear polígono para visualización
        vertices = figura.T
        polygon = Polygon(vertices, closed=True, fill=True, 
                         facecolor=color, alpha=alpha, edgecolor='black', label=label)
        self.ax.add_patch(polygon)
    
    def transformacion_estatica(self):
        """Demuestra transformaciones estáticas básicas"""
        self.ax.clear()
        self.ax.set_xlim(-3, 3)
        self.ax.set_ylim(-3, 3)
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.3)
        self.ax.set_title('Transformaciones Estáticas')
        
        # Figura original
        self.dibujar_figura(self.figura_original, 'blue', 0.3, 'Original')
        
        # Traslación
        matriz_t = self.matriz_traslacion(1.5, 0.5)
        figura_trasladada = self.aplicar_transformacion(self.figura_original, matriz_t)
        self.dibujar_figura(figura_trasladada, 'red', 0.7, 'Traslación')
        
        # Rotación (45 grados)
        matriz_r = self.matriz_rotacion(np.pi/4)
        figura_rotada = self.aplicar_transformacion(self.figura_original, matriz_r)
        self.dibujar_figura(figura_rotada, 'green', 0.7, 'Rotación 45°')
        
        # Escala
        matriz_s = self.matriz_escala(1.5, 0.8)
        figura_escalada = self.aplicar_transformacion(self.figura_original, matriz_s)
        self.dibujar_figura(figura_escalada, 'orange', 0.7, 'Escala')
        
        # Transformación compuesta (traslación + rotación + escala)
        matriz_compuesta = matriz_t @ matriz_r @ matriz_s
        figura_compuesta = self.aplicar_transformacion(self.figura_original, matriz_compuesta)
        self.dibujar_figura(figura_compuesta, 'purple', 0.7, 'Compuesta')
        
        self.ax.legend()
        plt.tight_layout()
        return self.fig
    
    def animacion_frame(self, frame):
        """Función para generar cada frame de la animación"""
        self.ax.clear()
        self.ax.set_xlim(-3, 3)
        self.ax.set_ylim(-3, 3)
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.3)
        
        # Parámetro de tiempo normalizado (0 a 1)
        t = frame / 100.0
        
        # Figura original (siempre visible con transparencia)
        self.dibujar_figura(self.figura_original, 'lightgray', 0.2, 'Original')
        
        # Animación 1: Traslación circular
        tx = 1.5 * np.cos(2 * np.pi * t)
        ty = 1.5 * np.sin(2 * np.pi * t)
        matriz_t = self.matriz_traslacion(tx, ty)
        figura_trasladada = self.aplicar_transformacion(self.figura_original, matriz_t)
        self.dibujar_figura(figura_trasladada, 'red', 0.8, 'Traslación circular')
        
        # Animación 2: Rotación continua
        angulo = 2 * np.pi * t * 2  # 2 vueltas completas
        matriz_r = self.matriz_rotacion(angulo)
        figura_rotada = self.aplicar_transformacion(self.figura_original, matriz_r)
        self.dibujar_figura(figura_rotada, 'green', 0.8, 'Rotación continua')
        
        # Animación 3: Escala oscilante
        escala = 1 + 0.5 * np.sin(2 * np.pi * t * 3)  # Oscila entre 0.5 y 1.5
        matriz_s = self.matriz_escala(escala, escala)
        figura_escalada = self.aplicar_transformacion(self.figura_original, matriz_s)
        self.dibujar_figura(figura_escalada, 'orange', 0.8, 'Escala oscilante')
        
        # Animación 4: Transformación compuesta compleja
        # Traslación senoidal + rotación + escala variable
        tx_comp = 0.8 * np.sin(2 * np.pi * t)
        ty_comp = 0.5 * np.cos(2 * np.pi * t * 1.5)
        angulo_comp = np.pi * t
        escala_comp = 0.8 + 0.4 * np.sin(2 * np.pi * t * 2)
        
        matriz_t_comp = self.matriz_traslacion(tx_comp, ty_comp)
        matriz_r_comp = self.matriz_rotacion(angulo_comp)
        matriz_s_comp = self.matriz_escala(escala_comp, escala_comp)
        
        # Aplicar transformaciones en orden: escala -> rotación -> traslación
        matriz_compuesta = matriz_t_comp @ matriz_r_comp @ matriz_s_comp
        figura_compuesta = self.aplicar_transformacion(self.figura_original, matriz_compuesta)
        self.dibujar_figura(figura_compuesta, 'purple', 0.9, 'Compuesta compleja')
        
        self.ax.set_title(f'Transformaciones Animadas - Frame {frame}/100 (t={t:.2f})')
        self.ax.legend(loc='upper right', bbox_to_anchor=(1.15, 1))
        
        # Mostrar matrices actuales como texto
        info_text = f"Tiempo: {t:.2f}\n"
        info_text += f"Traslación: ({tx:.2f}, {ty:.2f})\n"
        info_text += f"Rotación: {np.degrees(angulo):.1f}°\n"
        info_text += f"Escala: {escala:.2f}"
        
        self.ax.text(-2.8, 2.5, info_text, fontsize=9, 
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.8))
    
    def crear_animacion(self, frames=100, intervalo=50):
        """Crea y guarda la animación"""
        print("Creando animación...")
        
        # Crear animación
        anim = animation.FuncAnimation(
            self.fig, self.animacion_frame, frames=frames, 
            interval=intervalo, repeat=True, blit=False
        )
        
        return anim
    
    def guardar_gif(self, anim, nombre_archivo='transformaciones_animadas.gif'):
        """Guarda la animación como GIF"""
        print(f"Guardando GIF: {nombre_archivo}")
        
        # Crear directorio de resultados si no existe
        os.makedirs('../resultados', exist_ok=True)
        
        # Guardar como GIF
        ruta_completa = os.path.join('../resultados', nombre_archivo)
        anim.save(ruta_completa, writer='pillow', fps=20, dpi=100)
        
        print(f"GIF guardado en: {ruta_completa}")
        return ruta_completa

def main():
    """Función principal que ejecuta todas las demostraciones"""
    print("=== Taller 0: Transformaciones Básicas en Python ===")
    print("Creando demostraciones de transformaciones geométricas 2D...")
    
    # Crear instancia de la clase
    transformaciones = TransformacionesBasicas()
    
    # 1. Mostrar transformaciones estáticas
    print("\n1. Generando transformaciones estáticas...")
    fig_estatica = transformaciones.transformacion_estatica()
    plt.savefig('../resultados/transformaciones_estaticas.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    # 2. Crear y mostrar animación
    print("\n2. Creando animación de transformaciones...")
    anim = transformaciones.crear_animacion(frames=100, intervalo=50)
    
    # 3. Guardar como GIF
    print("\n3. Guardando animación como GIF...")
    ruta_gif = transformaciones.guardar_gif(anim, 'hola_mundo_transformaciones_python.gif')
    
    # Mostrar la animación (opcional - comentar si no se quiere mostrar)
    print("\n4. Mostrando animación...")
    plt.show()
    
    print(f"\n✅ Completado! Archivos generados:")
    print(f"   - Imagen estática: ../resultados/transformaciones_estaticas.png")
    print(f"   - GIF animado: {ruta_gif}")
    
    # Información sobre las matrices utilizadas
    print(f"\n📊 Matrices de transformación utilizadas:")
    print(f"   - Traslación: T(tx, ty)")
    print(f"   - Rotación: R(θ) con θ en radianes")
    print(f"   - Escala: S(sx, sy)")
    print(f"   - Compuesta: T × R × S (aplicadas de derecha a izquierda)")

if __name__ == "__main__":
    main()
