from gpiozero import DigitalOutputDevice, DigitalInputDevice
import time

flits_b_oranje = DigitalOutputDevice(24, active_high=False)

flits_b_oranje.on()
time.sleep(4)
flits_b_oranje.off()