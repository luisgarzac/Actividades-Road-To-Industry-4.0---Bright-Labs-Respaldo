import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

SERVO = 17
 

GPIO.setup(SERVO,GPIO.OUT)

p =GPIO.PWM(SERVO,50)
p.start(2.5)
angulo = 1.5
time.sleep(2)
while True: 
    angulo = input("Introduce el angulo: ")
    if angulo =='s':
        break
    angulo = (int(angulo)/18) + 2
    p.ChangeDutyCycle(angulo)
    time.sleep(0.5)
    angulo = (angulo-2)*18
    print("angulo "+ str(round(angulo,2)))
p.stop()
GPIO.cleanup()