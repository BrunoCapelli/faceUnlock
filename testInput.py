import RPi.GPIO as GPIO
import time

# Configuración de la biblioteca RPi.GPIO
GPIO.setmode(GPIO.BCM)  # Usar la numeración BCM de los pines

# Configuración del pin GPIO 23 (pin físico 16) como entrada
GPIO.setup(23, GPIO.IN)

try:
    while True:
        # Leer el estado del pin GPIO 23
        input_state = GPIO.input(23)
        if input_state == GPIO.HIGH:
            print("Corriente detectada en el pin GPIO 23 (pin 16)")
        else:
            print("No se detecta corriente en el pin GPIO 23 (pin 16)")
        
        # Esperar un momento antes de la siguiente lectura
        time.sleep(1)
except KeyboardInterrupt:
    # Limpiar la configuración de los pines GPIO al salir
    GPIO.cleanup()
