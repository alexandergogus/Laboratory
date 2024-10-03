import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
dac = [8,11,7,1,0,5,12,6]
comp = 14
troyka = 13
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = 1)
GPIO.setup(comp, GPIO.IN)

def num_to_bin(num):
    return [int(digit) for digit in bin(num)[2:].zfill(8)]
def adc():
    for i in range(256):
        dacValue = num_to_bin(i)
        GPIO.output(dac, dacValue)
        time.sleep(0.0007)
        compValue = GPIO.input(comp)
        if compValue > 0:
            return i 
    return 0
try:
    while True:
        timeF = time.time()
        compValue = adc()
        timeF = time.time() - timeF
        volt = compValue/256 *3.3
        print(volt, 'time =', timeF )
finally:
    GPIO.output(dac,0)
    GPIO.cleanup()