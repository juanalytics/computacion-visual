import cv2
import numpy as np

# --- Cargar imagen ---
img = cv2.imread('gato.jpg')
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# --- Ajustar imagen al tamaño de la pantalla ---
screen_res = (1920, 1080)  # puedes cambiar según tu monitor
scale_width = screen_res[0] / img_gray.shape[1]
scale_height = screen_res[1] / img_gray.shape[0]
scale = min(scale_width, scale_height)
window_width = int(img_gray.shape[1] * scale)
window_height = int(img_gray.shape[0] * scale)
img_gray = cv2.resize(img_gray, (window_width, window_height))

# --- Crear ventana y sliders ---
cv2.namedWindow('Filtro Interactivo', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Filtro Interactivo', 800, 400)

def nothing(x):
    pass

# Crear 9 sliders con nombres más claros
labels = [
    "Fila1-Col1", "Fila1-Col2", "Fila1-Col3",
    "Fila2-Col1", "Fila2-Col2", "Fila2-Col3",
    "Fila3-Col1", "Fila3-Col2", "Fila3-Col3"
]

for name in labels:
    cv2.createTrackbar(name, 'Filtro Interactivo', 5, 10, nothing)  # rango 0-10, centrado en 5

# Normalización automática ON/OFF
cv2.createTrackbar('Normalizar (1=Sí, 0=No)', 'Filtro Interactivo', 1, 1, nothing)

while True:
    # Leer valores de los sliders
    vals = [cv2.getTrackbarPos(name, 'Filtro Interactivo') - 5 for name in labels]
    normalize = cv2.getTrackbarPos('Normalizar (1=Sí, 0=No)', 'Filtro Interactivo')

    # Crear kernel 3x3
    kernel = np.array(vals, dtype=np.float32).reshape((3, 3))

    # Normalización opcional
    if normalize:
        kernel_sum = np.sum(kernel)
        if kernel_sum != 0:
            kernel = kernel / kernel_sum

    # Aplicar filtro
    filtered = cv2.filter2D(img_gray, -1, kernel)

    # Combinar imagen original y filtrada lado a lado
    combined = np.hstack((img_gray, filtered))

    # Mostrar resultado
    cv2.imshow('Filtro Interactivo', combined)

    key = cv2.waitKey(30) & 0xFF
    if key == 27:  # ESC para salir
        break

cv2.destroyAllWindows()
