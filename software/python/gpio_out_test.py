from gpiozero import DigitalOutputDevice, DigitalInputDevice
import time

flits_a_rood = DigitalOutputDevice(15, active_high=False)
flits_b_groen = DigitalOutputDevice(23, active_high=False)
flits_b_oranje = DigitalOutputDevice(24, active_high=False)
flits_b_rood = DigitalOutputDevice(25, active_high=False)
ledstrip_rood = DigitalOutputDevice(21, active_high=False)
ledstrip_groen = DigitalOutputDevice(20, active_high=False)
ledstrip_blauw = DigitalOutputDevice(16, active_high=False)


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