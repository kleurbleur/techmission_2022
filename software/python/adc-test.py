import time
import board
import busio
i2c = busio.I2C(board.SCL, board.SDA)
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

ads = ADS.ADS1115(i2c)
ads.gain = 4
chan = AnalogIn(ads, ADS.P3)

while True:
    print(chan.value, chan.voltage)
    time.sleep(0.2)