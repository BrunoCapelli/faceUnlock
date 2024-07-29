import RPi.GPIO as GPIO
import time

# Configurar la numeración de los pines
GPIO.setmode(GPIO.BOARD)

# Configurar el pin 11 (GPIO 17) como una salida
pin_11 = 11
GPIO.setup(pin_11, GPIO.OUT)

try:
    # Establecer el pin 11 en alto (5V)
    GPIO.output(pin_11, GPIO.HIGH)
    print("Pin 11 (GPIO 17) establecido en alto (5V)")
    
    # Mantener el estado por 10 segundos
    time.sleep(10)
    
    # Establecer el pin 11 en bajo (0V)
    GPIO.output(pin_11, GPIO.LOW)
    print("Pin 11 (GPIO 17) establecido en bajo (0V)")

finally:
    # Limpiar la configuración de GPIO
    GPIO.cleanup()
    print("Limpieza de GPIO completada")


#sudo apt-get install python3-rpi.gpio
