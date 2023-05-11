import cv2
import datetime
import time

# Esperar X segundos antes de empezar
time.sleep(10)

# Crea un objeto de captura de video
cap = cv2.VideoCapture(0)  # Cambia "0" por el número de tu cámara si tienes varias

# Define los momentos en los que quieres que aparezca el punto verde (en segundos)
timestamps = [10, 15, 25, 35, 40]

# Variables para controlar el tiempo
start_time = datetime.datetime.now()
current_time = start_time

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

    # Comprueba si se alcanza uno de los momentos deseados
    if int(elapsed_seconds) in timestamps:
        # Dibuja un punto verde en el cuadro
        cv2.circle(frame, (250, 250), 100, (0, 255, 0), -1)

    # Muestra el cuadro resultante
    cv2.imshow('Video', frame)

    # Comprueba si se presiona la tecla 'q' para salir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera los recursos y cierra las ventanas
cap.release()
cv2.destroyAllWindows()
