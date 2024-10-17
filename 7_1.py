import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt
def decimal2binary(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def adc():
    k = 0
    for i in range (0,8):
        k += 2**(7 - i)
        GPIO.output(dac, decimal2binary(k))
        time.sleep(0.005)
        if GPIO.input(comp) == 1:
            k -= 2**(7 - i)
    return k
def led_out(val):
    GPIO.output(leds, decimal2binary(val))

if __name__ == '__main__':
    dac = [8, 11, 7, 1, 0, 5, 12, 6]
    leds = [2, 3, 4, 17, 27, 22, 10 ,9]
    comp = 14
    troyka = 13
    maxU = 243
    u = 0
    GPIO.setmode(GPIO.BCM) #настройка малинки
    GPIO.setup(dac, GPIO.OUT)
    GPIO.setup(leds, GPIO.OUT)
    GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
    GPIO.setup(comp, GPIO.IN)
    startT = time.time()
    endT = 0
    end1T = 0
    end1U = 25
    res = []
    res1 = []
    try:
        while u < maxU: #начало первого жксперимента
            u = adc()
            if u != 0:
                print(u, round(u * 3.3 / 256, 2))
            else:
                print(255, 3,28)
            res.append(u)
            led_out(u)
        endT = time.time()
        N = [i + 1 for i in range(len(res))]
        lenN = len(N)
        GPIO.setup(troyka, GPIO.OUT, initial = GPIO.LOW)
        start1T = time.time() #начало второго эксперимента
        while u > end1U:
            u = adc()
            if u != 0:
                print(u, round(u * 3.3 / 256, 2))
            else:
                print(255, 3,28)
            res.append(u)
            led_out(u)
        end1T = time.time() #конец второго эксперимента
        for i in range(len(res) - lenN):
            N.append(i + lenN)
        plt.scatter(N, res)
        plt.show() #построение графика
        totalN = len(res)
        totalT = round(-startT + endT, 2) + round(end1T - start1T, 2)
        print('Time =', totalT)
        print('T =', round(totalT / totalN, 3))
        print('Freq =', round(totalN / totalT))
        print('Step =', round(3.3 / 256, 3)) #вывод в терминал

        with open("data.txt", "w") as file: #запись в файлы
            for i in res:
                file.write(str(i) + '\n')

        with open("settings.txt", "w") as file:
            file.write(str(round(totalN / totalT)) + '\n')
            file.write(str(round(3.3 / 256, 3)) + '\n')
    finally:
        GPIO.cleanup()