from cgitb import reset
from gpiozero import DigitalOutputDevice, DigitalInputDevice
import time

reset_button = DigitalInputDevice(5)
b_onder = DigitalInputDevice(10)
b_midden = DigitalInputDevice(22)
b_boven = DigitalInputDevice(27)
a_onder = DigitalInputDevice(17)
a_midden = DigitalInputDevice(4)
a_boven = DigitalInputDevice(1)


while True:
    if reset_button.value == 1:
            print("reset")
    if b_onder.value == 1:
            print("b_onder")
    if b_midden.value == 1:
            print("b_midden")
    if b_boven.value == 1:
            print("b_boven")
    if a_onder.value == 1:
            print("a_onder")
    if a_midden.value == 1:
            print("a_midden")
    if a_boven.value == 1:
            print("a_boven")                                                                      
    time.sleep(0.2)
