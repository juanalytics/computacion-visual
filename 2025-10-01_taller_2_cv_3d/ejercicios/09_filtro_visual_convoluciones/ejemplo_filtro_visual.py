import cv2
import numpy as np

# === Cargar imagen ===
img = cv2.imread('gato.jpg')
if img is None:
    raise FileNotFoundError("No se encontró 'gato.jpg'. Verifica la ruta o el nombre del archivo.")

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_gray = cv2.resize(img_gray, (400, 400))


# === Función para aplicar convolución manual ===
def convolucion_manual(imagen, kernel):
    h, w = imagen.shape
    kh, kw = kernel.shape
    pad = kh // 2
    imagen_padded = np.pad(imagen, pad, mode='constant')
    salida = np.zeros_like(imagen, dtype=np.float32)
    
    for i in range(h):
        for j in range(w):
            region = imagen_padded[i:i+kh, j:j+kw]
            salida[i, j] = np.sum(region * kernel)
    
    # Normalizar al rango 0-255
    salida = np.clip(salida, 0, 255)
    return salida.astype(np.uint8)

# === Definir kernels ===
kernels = {
    'Blur (Suavizado)': (1/9) * np.array([[1,1,1],
                                          [1,1,1],
                                          [1,1,1]]),
    
    'Sharpen (Nitidez)': np.array([[0,-1,0],
                                   [-1,5,-1],
                                   [0,-1,0]]),
    
    'Bordes (Sobel X)': np.array([[-1,0,1],
                                  [-2,0,2],
                                  [-1,0,1]])
}

# === Aplicar filtros ===
resultados = []

for nombre, kernel in kernels.items():
    conv_manual = convolucion_manual(img_gray, kernel)
    conv_cv2 = cv2.filter2D(img_gray, -1, kernel)
    combinado = np.hstack((conv_manual, conv_cv2))
    resultados.append((nombre, combinado))

# === Mostrar resultados ===
for nombre, res in resultados:
    cv2.imshow(nombre + " | Izq: Manual - Der: cv2.filter2D", res)

# === BONUS: Interactivo ===
cv2.namedWindow('Filtro Interactivo')

def nothing(x):
    pass

# Crear sliders (con nombres más claros)
nombres = [
    "Fila1-Col1", "Fila1-Col2", "Fila1-Col3",
    "Fila2-Col1", "Fila2-Col2", "Fila2-Col3",
    "Fila3-Col1", "Fila3-Col2", "Fila3-Col3"
]

for nombre in nombres:
    cv2.createTrackbar(nombre, 'Filtro Interactivo', 5, 10, nothing)

cv2.createTrackbar('Normalizar', 'Filtro Interactivo', 1, 1, nothing)

while True:
    valores = [cv2.getTrackbarPos(nombre, 'Filtro Interactivo') - 5 for nombre in nombres]
    normalize = cv2.getTrackbarPos('Normalizar', 'Filtro Interactivo')
    kernel = np.array(valores, dtype=np.float32).reshape((3, 3))

    if normalize:
        s = np.sum(kernel)
        if s != 0:
            kernel = kernel / s

    filtrado = cv2.filter2D(img_gray, -1, kernel)
    filtrado_resized = cv2.resize(filtrado, (img_gray.shape[1]//2, img_gray.shape[0]//2))
    cv2.imshow('Filtro Interactivo', filtrado_resized)

    if cv2.waitKey(30) & 0xFF == 27:
        break

cv2.destroyAllWindows()
