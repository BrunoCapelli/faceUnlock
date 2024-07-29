import RPi.GPIO as GPIO

def InitializePins():
    GPIO.setmode(GPIO.BCM)

    # Setting pinout 
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(27, GPIO.OUT)

def Activate_Pin17():
    GPIO.output(17, GPIO.HIGH)

def Activate_Pin27():
    GPIO.output(27, GPIO.HIGH)

def Deactivate():
    # Turn down the pins
    GPIO.output(17, GPIO.LOW)
    GPIO.output(27, GPIO.LOW)
    
    GPIO.cleanup()