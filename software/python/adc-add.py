import time
import board
import busio
i2c = busio.I2C(board.SCL, board.SDA)
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

ads = ADS.ADS1115(i2c)
chan = AnalogIn(ads, ADS.P0)
battery_slider = 0

while True:
    print(chan.value, chan.voltage)
    if chan.value < 100:
        print("battery needs charging")
    else:
        battery_value = chan.value / 1000
        print("battery_value", battery_value)
        battery_slider += battery_value
        print("battery_slider", battery_slider)

    time.sleep(0.2)