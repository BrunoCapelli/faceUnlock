import cv2

# Iniciar la captura de video desde la cámara (0 es el índice de la cámara por defecto)
cap = cv2.VideoCapture(0)

# Verificar si la cámara se abrió correctamente
if not cap.isOpened():
    print("Error: No se puede acceder a la cámara.")
else:
    print("Cámara iniciada.")

# Definir el nombre de la ventana
window_name = 'Live Video'

# Crear una ventana con el nombre especificado
cv2.namedWindow(window_name)

# Configurar el tamaño de la ventana
cv2.resizeWindow(window_name, 800, 600)

# Bucle para capturar frame por frame
while cap.isOpened():
    ret, frame = cap.read()  # Leer un frame de la cámara

    if not ret:
        print("Error: No se puede recibir frame (se ha alcanzado el final del stream).")
        break

    # Redimensionar el frame a 800x600
    frame_resized = cv2.resize(frame, (800, 600))

    # Mostrar el frame redimensionado en la ventana
    cv2.imshow(window_name, frame_resized)

    # Salir del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar el objeto de captura y cerrar todas las ventanas
cap.release()
cv2.destroyAllWindows()
