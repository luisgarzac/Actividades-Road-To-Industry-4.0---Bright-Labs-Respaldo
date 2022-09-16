# Importar librerías necesarias
import RPi.GPIO as GPIO
import time
import numpy as np
import csv

# Seleccionar tipo de referenciá para los pines
GPIO.setmode(GPIO.BCM)
# Numero de los pines segun BCM
TRIG = 23
ECHO = 24
SERVO = 17

print ("Distance Measurement In Progress")

# Configurar los puertos como salidas o entradas
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(SERVO,GPIO.OUT)

# Apagar el Trigger para evitar problemas con el ultrasonicos
GPIO.output(TRIG, False)

print ("Waiting For Sensor To Settle")

# Crear un PWM con frecuencia de 50Hz
p =GPIO.PWM(SERVO,50)
# Configurar Duty Cycle a 2.5% Angulo de 9%
p.start(2.5)
# Inicializar angulo en -9 grados
angulo = 1.5
# Esperar 2 segundos
time.sleep(2)

# Escribir en mapeo.csv guardar el archivo en la variable csv_file
with open('mapeo.csv', mode='w') as csv_file:
    #Configurar CSV para usar delimitador de , y guardar el modificador en la variable writer
    writer = csv.writer(csv_file, delimiter=',', quotechar ='"', quoting=csv.QUOTE_MINIMAL)
    # Escribir la primera linea del CSV
    writer.writerow(['angulo','0', '9', '18', '27', '36', '45', '54', '63', '72', '81',
     '90', '99', '108', '117', '126', '135', '144', '153', '162', '171', '180',])
    # Inicializar distancias en la array
    distanceArray = np.zeros(21)
    # Inicializar el contador de linea
    i = 0

    # Empezar lecturas y escrituras
    while True:
        # Modificar el angulo a 0.5% de Duty Cycle = +9 grados
        angulo = angulo + 0.5
        # Identificar cuando el angulo llega a 12.5% de Duty Cycle = 180 grados
        if angulo == 12.5:
            # Cambiar las distancias a lista para que sea una lista de Strings
            distan = list(distanceArray)
            # Contar
            i=i+1
            # Agregar el primer dato de cada línea
            lectura = "lectura"+str(i)
            # Escribir una línea del CSV
            writer.writerow([lectura]+ distan)
            # Inicializar angulo en -9 grados
            angulo = 1.5

        # Mover el Servo
        p.ChangeDutyCycle(angulo)
        # Disparar un pulso de 0.00001 segundos con el Trigger
        time.sleep(0.5)
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
        #Tomar una lectura con el Echo
        while GPIO.input(ECHO)==0:
            pulse_start = time.time()
        while GPIO.input(ECHO)==1:
            pulse_end = time.time()
        # Calcular con los tiempos de respuesta la distancia y guardarla en la array
        pulse_duration = pulse_end - pulse_start
        distanceArray[round(2*(angulo-2))] = round((pulse_duration * 17150), 2)
        #Calcular Angulo Real en grados
        anguloreal = (angulo-2)*18
        # Mostrar angulo y distancia
        print ("Distance:",distanceArray[round(2*(angulo-2))],"cm", " Angulo", anguloreal)
# Resetear puertos
p.stop()
GPIO.cleanup()
