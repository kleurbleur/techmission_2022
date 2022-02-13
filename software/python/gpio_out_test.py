from ast import While
from gpiozero import DigitalOutputDevice, DigitalInputDevice
import time

flits_a_rood = DigitalOutputDevice(15)
flits_b_groen = DigitalOutputDevice(23)
flits_b_oranje = DigitalOutputDevice(24)
flits_b_rood = DigitalOutputDevice(25)
ledstrip_rood = DigitalOutputDevice(21)
ledstrip_groen = DigitalOutputDevice(20)
ledstrip_blauw = DigitalOutputDevice(16)


while True:
    flits_a_rood.on()
    flits_b_groen.on()
    flits_b_oranje.on()
    flits_b_rood.on()
    ledstrip_rood.on()
    ledstrip_groen.on()
    ledstrip_blauw.on()
    time.sleep(3)
    flits_a_rood.off()
    flits_b_groen.off()
    flits_b_oranje.off()
    flits_b_rood.off()
    ledstrip_rood.off()
    ledstrip_groen.off()
    ledstrip_blauw.off()
    time.sleep(3)