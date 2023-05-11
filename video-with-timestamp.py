import cv2
import datetime
import random
import time

# Crea un objeto de captura de video
cap = cv2.VideoCapture(0)  # Cambia "0" por el número de tu cámara si tienes varias

# Variables para controlar el tiempo y el círculo verde
start_time = datetime.datetime.now()
current_time = start_time
circle_time = random.uniform(1, 5)  # Genera un tiempo aleatorio entre 2 y 5 segundos
circle_duration = 0.5  # Duración en segundos para mostrar el círculo verde

# Establece el tamaño de la ventana del video
cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Video', 800, 600)

# Bucle para procesar el video
while True:
    # Lee el cuadro actual del video
    ret, frame = cap.read()

    # Obtiene el tiempo transcurrido desde el inicio
    current_time = datetime.datetime.now()
    elapsed_time = current_time - start_time
    elapsed_seconds = elapsed_time.total_seconds()

    # Dibuja el timestamp del sistema en el cuadro
    timestamp = str(current_time)
    cv2.putText(frame, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    if elapsed_seconds >= circle_time:
        # Calcula las coordenadas del centro de la pantalla
        height, width, _ = frame.shape
        center_x = width // 2
        center_y = height // 2

        # Calcula el radio del círculo
        radius = min(center_x, center_y) // 5

        # Dibuja un círculo verde en el centro de la pantalla
        cv2.circle(frame, (center_x, center_y), radius, (0, 255, 0), -1)
        show_circle = True

    # Comprueba si ha pasado el tiempo para ocultar el círculo verde
    if elapsed_seconds >= circle_time + circle_duration:
        # Genera un nuevo tiempo aleatorio para el próximo círculo verde
        circle_time = random.uniform(1, 5)
        start_time = datetime.datetime.now()
    
    # Muestra el cuadro resultante
    cv2.imshow('Video', frame)

    # Comprueba si se presiona la tecla 'q' para salir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera los recursos y cierra las ventanas
cap.release()
cv2.destroyAllWindows()
