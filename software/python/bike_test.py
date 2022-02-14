from gevent import monkey; monkey.patch_all()
from flask import Flask, Response, render_template
from gevent.pywsgi import WSGIServer
import json, time, board, busio, subprocess
i2c = busio.I2C(board.SCL, board.SDA)
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from gpiozero import DigitalOutputDevice, DigitalInputDevice


print("start the Flask server")
app = Flask(__name__)

ads = ADS.ADS1115(i2c)
chan_01 = AnalogIn(ads, ADS.P2)
chan_02 = AnalogIn(ads, ADS.P3)
flits_a_rood = DigitalOutputDevice(15, active_high=False)
flits_b_groen = DigitalOutputDevice(23, active_high=False)
flits_b_oranje = DigitalOutputDevice(24, active_high=False)
flits_b_rood = DigitalOutputDevice(25, active_high=False)
ledstrip_rood = DigitalOutputDevice(21, active_high=False)
ledstrip_groen = DigitalOutputDevice(20, active_high=False)
ledstrip_blauw = DigitalOutputDevice(16, active_high=False)
reset_button = DigitalInputDevice(5)
b_onder = DigitalInputDevice(10)
b_midden = DigitalInputDevice(22)
b_boven = DigitalInputDevice(27)
a_onder = DigitalInputDevice(17)
a_midden = DigitalInputDevice(4)
a_boven = DigitalInputDevice(1)

start = True
scanner_video = 0
scanner_running = False
cable_a_out = True
b_onder_if = False
b_midden_if = False
b_boven_if = False
circuit_b = False
battery_slider_if = True
circuit_b_if = True
bike_01 = 0
bike_02 = 0
generator_text = 0
generator_text_color = "rgb(0, 226, 252)"
generator_volt = 0
generator_ampere = 0
generator_slider = 0 #max 1085
battery_text = 0
battery_volt = 0
battery_ampere = 0
battery_slider = 0 #max 267
battery_slider_color = "rgb(0, 226, 252)"
battery_icon = "hidden"
status_100 = False
generator_100 = False
mess_01 = "hidden"
mess_02 = "hidden"
mess_03 = "hidden"
mess_04 = "hidden"
mess_05 = "hidden"
mess_06 = "hidden"
mess_07 = "hidden"
mess_08 = "hidden"

##############################
@app.route("/")
def render_index():
  return render_template("index.html")

##############################
@app.route("/listen")
def listen():

  def respond_to_client():
    print("found client")  
    while True:
        global start
        global reset_button
        global scanner_video
        global scanner_running
        global cable_a_out
        global b_onder_if
        global b_midden_if
        global b_boven_if
        global circuit_b
        global circuit_b_if
        global battery_slider_if
        global audio_01
        global audio_02
        global audio_03
        global audio_04
        global audio_05
        global audio_06
        global audio_07
        global audio_08
        global a_onder
        global a_midden
        global a_boven
        global b_onder
        global b_midden
        global b_boven
        global bike_01
        global bike_02
        global battery_text
        global battery_volt
        global battery_ampere
        global battery_slider
        global battery_slider_color
        global battery_icon
        global generator_text
        global generator_text_color
        global generator_volt
        global generator_ampere
        global generator_slider
        global status_100
        global generator_100
        global mess_01
        global mess_02
        global mess_03
        global mess_04
        global mess_05
        global mess_06
        global mess_07
        global mess_08
        if battery_slider >= 267: 
            battery_slider = 267
            battery_text = 100
        if battery_slider_if == True:
            battery_slider_if = False
            audio_05.terminate()
            audio_05.kill()
            subprocess.Popen(["killall", "omxplayer.bin"])
            scanner_video = subprocess.Popen(["omxplayer", "/home/pi/Desktop/techmission/software/python/static/video/scanner_scant_mapped.mov", "--loop", "--display=7", ">", "/dev/null", "2>&1"])
            audio_06 = subprocess.Popen(["omxplayer", "/home/pi/Desktop/techmission/software/python/static/sound/06_opstart_engine.mp3", "-o", "local"]) #16S moet de slider duren
        while generator_text < 100:
            print("generator_slider", generator_slider)
            print("generator_text", generator_text)
            generator_volt += 1.92
            generator_ampere += 0.56
            generator_text += 1
            generator_slider += 10.85
            if generator_text >= 400:
                    generator_text_color = "rgb(27, 30, 61)"
            else:
                    generator_text_color = "rgb(0, 226, 252)"
            _data_generator_slider = json.dumps({
                    "generator_slider": generator_slider,
                    "generator_text_color": generator_text_color,
                    "generator_text": generator_text,
                    "generator_volt": generator_volt,
                    "generator_ampere": generator_ampere
            })
            yield f"id: 1\ndata: {_data_generator_slider}\nevent: generator_slider\n\n"
            time.sleep(0.16)
        if generator_text == 100:
            generator_slider = 1085
            circuit_b_if = False
            status_100 = True
        else:
            print("bikes ready")
            mess_04 = "hidden"
            mess_05 = "visible"
            bike_01 = chan_01.value / 29000 # 29000 is de max wanneer je hard fietst
            bike_02 = chan_02.value / 29000 # 29000 is de max wanneer je hard fietst
            if bike_01 >= 1 and bike_02 >= 1: 
                battery_icon = "visible"
                battery_slider += int(bike_01) + int(bike_02) #max 267
                battery_text = int(battery_slider/2.7)
            # else:
            #       while bike_01 < 0.1 and bike_02 < 0.1: 
            #             battery_slider -= 0.5
            #             battery_text -= 0.5
            #             time.sleep(0.16)
            # if bike_01 >= 1 or bike_02 >= 1:
            #       battery_volt = 230
            # else:
            #       battery_volt = 0
            # if bike_01 > 0.1 and bike_02 > 0.1:
            #       battery_ampere = 16
            # elif bike_01 > 0.1 and bike_02 < 0.1:
            #       battery_ampere = 8
            # elif bike_02 > 0.1 and bike_01 < 0.1:
            #       battery_ampere = 8
            # else:
            #       battery_ampere = 0
            # if battery_text > 10:
            #       battery_slider_color = "rgb(226, 6,19)"
            # elif battery_text < 10 and battery_text > 95:
            #       battery_slider_color = "rgb(0, 226, 252)"
            # elif battery_text < 95:
            #       battery_slider_color = "rgb(0, 249, 0)"
            print('batt_slider: ', battery_slider)
            print('batt_text: ', battery_text)
            print('bike_01:',bike_01, chan_01.value, chan_01.voltage)
            print('bike_02:',bike_02, chan_02.value, chan_02.voltage)
        _data_battery = json.dumps({
            "battery_slider": battery_slider,
            "battery_volt": battery_volt,
            "battery_ampere": battery_ampere,
            "battery_text": battery_text,
            "battery_icon": battery_icon,
            "battery_slider_color": battery_slider_color,
            "mess_04": mess_04,
            "mess_05": mess_05,
        })
        yield f"id: 1\ndata: {_data_battery}\nevent: battery\n\n"
