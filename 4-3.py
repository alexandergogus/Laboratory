import RPi.GPIO as GPIO
from time import sleep as sp

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT)

port = GPIO.PWM(24, 1000)
port.start(0)

try:
    while True:
        k = int(input(Введите цикл свободы : ))
        port.ChangeDutyCycle(k)
        print(3.3 * k / 100)
        sp(1)
except ValueError:
    print('Неправильное значение')
finally:
    port.stop()
    GPIO.output(24, 0)
    GPIO.cleanup()