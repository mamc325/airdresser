import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
pin = 17
GPIO.setup(pin, GPIO.OUT)
p = GPIO.PWM(pin, 500)

def speaker(start_stop):
    try:
        if start_stop == 1:
            p.start(40)
            time.sleep(0.1)
            p.stop()
        else:
            p.stop()
            GPIO.cleanup()
    except KeyboardInterrupt:
        p.stop()
        GPIO.cleanup()
