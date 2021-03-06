#!/usr/local/bin/python
import RPi.GPIO as GPIO
import time
from subprocess import call

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
#Pin al que esta conectado el sensor TLR
pin_to_circuit = 7
#Punto de corte para luz encedida y apagada
lux = 10000

def rc_time (pin_to_circuit):
    count = 0
  
    #Output on the pin for 
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    time.sleep(0.1)

    #Change the pin back to input
    GPIO.setup(pin_to_circuit, GPIO.IN)
  
    #Count until the pin goes high
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        count += 1

    return count
	
try:	
	while True:
		i = rc_time(pin_to_circuit)
		if i < lux:
			print("Screen on", i)
			call(["/usr/bin/vcgencmd", "display_power", "1"])
			time.sleep(1)
		elif i >=lux:
			print("Screen off", i)
			call(["/usr/bin/vcgencmd", "display_power", "0"])
			time.sleep(1)
		
except KeyboardInterrupt:
	pass
finally:
	GPIO.cleanup()
