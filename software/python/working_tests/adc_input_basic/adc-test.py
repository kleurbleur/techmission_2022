import time
import board
import busio
i2c = busio.I2C(board.SCL, board.SDA)
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

ads = ADS.ADS1115(i2c)
chan1 = AnalogIn(ads, ADS.P2)
chan2 = AnalogIn(ads, ADS.P3)

while True:
    print('chan1', chan1.value, chan1.voltage)
    print('chan2', chan2.value, chan2.voltage)
    time.sleep(0.2)