from gpiozero import DigitalOutputDevice, DigitalInputDevice
import time

flits_b_groen = DigitalOutputDevice(23, active_high=False)
flits_b_oranje = DigitalOutputDevice(24, active_high=False)

flits_b_groen.on()
time.sleep(4)
flits_b_groen.off()
print(1)