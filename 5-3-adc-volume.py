import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
dac = [8,11,7,1,0,5,12,6]
led = [2,3,4,17,27,22,10,9]
comp = 14
troyka = 13
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = 1)
GPIO.setup(comp, GPIO.IN)

def num_to_bin(num):
    return [int(digit) for digit in bin(num)[2:].zfill(8)]
def adc1():
    num = 0
    for i in range(7,-1,-1):
        num+=2**i
        num_list = num_to_bin(num)
        GPIO.output(dac, num_list)
        time.sleep(0.0005)
        compValue = GPIO.input(comp)
        if compValue>= 0.95 and compValue<= 1.05:
            num-=2**i
    return num
def adc2():
    def adc():
        for i in range(256):
            dacValue = num_to_bin(i)
            GPIO.output(dac, dacValue)
            time.sleep(0.0007)
            compValue = GPIO.input(comp)
            if compValue > 0:
                return i 
            if i >=255:
                return 255
    return 0
def Volume(num):
    if num == 0:
        return 8*[0]
    array = [int((i)*255/8) for i in range(8)]
    result = [1 if num >= array_elem else 0 for array_elem in array]

    return result
try:
    while True:
        compValue = adc1()
        volt = compValue/256 *3.3
        compL = Volume(compValue)
        time.sleep(0.07)
        GPIO.output(led, compL)
        print(volt)
finally:
    GPIO.output(dac,0)
    GPIO.cleanup()