from gevent import monkey; monkey.patch_all()
from flask import Flask, Response, render_template
from gevent.pywsgi import WSGIServer
import json, time, board, busio, subprocess
i2c = busio.I2C(board.SCL, board.SDA)
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from gpiozero import DigitalOutputDevice, DigitalInputDevice

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
reset_button = False
scanner_video = 0
scanner_running = False
cable_a_out = True
audio_01 = ""
audio_02 = ""
audio_03 = ""
audio_04 = ""
audio_05 = ""
audio_06 = ""
audio_07 = ""
audio_08 = ""
bike_01 = 0
bike_02 = 0
generator_text = 0
generator_volt = 0
generator_ampere = 0
generator_slider = 0 #max 1085
battery_text = 0
battery_volt = 0
battery_ampere = 0
battery_slider = 0 #max 267
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
    while True:
      global start
      global reset_button
      global scanner_video
      global scanner_running
      global cable_a_out
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
      global generator_text
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
      if reset_button == True:
            start = True
      if start == True and a_onder.value == 1 and a_midden.value == 1 and a_boven.value == 1: #START OF THE INSTALLATION
            flits_a_rood.off()
            flits_b_groen.off()
            flits_b_oranje.off()
            flits_b_rood.off()
            ledstrip_rood.off()
            ledstrip_blauw.off()
            ledstrip_groen.off() 
            if scanner_running == False:
                  print("start scanner video")
                  scanner_video = subprocess.Popen(["omxplayer", "static/video/scanner_scant_mapped.mov", "--loop", "--display=7"])
            print("flitslicht A rood aan")
            print("ledstrip rood aan")
            print("audio kortsluiting aan")
            flits_a_rood.on()
            ledstrip_rood.on()            
            audio_01 = subprocess.Popen(["omxplayer", "static/sound/01_kortsluiting_alarm_loop.mp3", "--loop", "-o", "local"])
            bike_01 = 0
            bike_02 = 0
            generator_text = 0
            generator_volt = 0
            generator_ampere = 0
            generator_slider = 0 #max 1085
            battery_text = 0
            battery_volt = 0
            battery_ampere = 0
            battery_slider = 0 #max 267
            mess_01 = "hidden"
            mess_02 = "hidden"
            mess_03 = "visible"
            mess_04 = "hidden"
            mess_05 = "hidden"
            mess_06 = "hidden"
            mess_07 = "hidden"
            mess_08 = "hidden"
            _data_start = json.dumps({
                "generator_slider": generator_slider,
                "generator_text": generator_text,
                "generator_volt": generator_volt,
                "generator_ampere": generator_ampere,
                "battery_slider": battery_slider,
                "battery_volt": battery_volt,
                "battery_ampere": battery_ampere,
                "battery_text": battery_text,
                "mess_01": mess_01,
                "mess_02": mess_02,
                "mess_03": mess_03,
                "mess_04": mess_04,
                "mess_05": mess_05,
                "mess_06": mess_06,
                "mess_07": mess_07,
                "mess_08": mess_08
            })
            yield f"id: 1\ndata: {_data_start}\nevent: start\n\n" #we push the data towards the interface per event
            scanner_running = True
            start = False      
      if not all([a_onder.value, a_midden.value, a_boven.value]) and cable_a_out == True: #CABLES A OUT
            print("flitslicht a rood uit")
            print("flitslicht B oranje aan")
            print("audio 01 uit, audio 02 aan")
            flits_a_rood.off()
            flits_b_oranje.on()
            audio_01.kill()
            audio_02 = subprocess.Popen(["omxplayer", "static/sound/02_kortsluiting_standby_loop.mp3", "--loop", "-o", "local"])
            mess_03 = "hidden"
            mess_04 = "visible"      
            _data_cable_a = json.dumps({
                "mess_03": mess_03,
                "mess_04": mess_04,
            })
            yield f"id: 1\ndata: {_data_cable_a}\nevent: cable_a\n\n" #we push the data towards the interface per event
            cable_a_out = False
      if b_onder.value and not all([b_onder.value, b_midden.value, b_boven.value]): #
            #
            #
            # condities maken in de if statements zodat ze maar eenmaal lopen
            #
            #
            audio_03 = subprocess.Popen(["omxplayer", "static/sound/03_goede_kabel_groep.mp3", "-o", "local"])
            print("flitslicht b groen aan 4s")
            subprocess.Popen(["python", "flits_b_groen.py"])
      elif b_midden.value and not all([b_onder.value, b_midden.value, b_boven.value]): #
            audio_03 = subprocess.Popen(["omxplayer", "static/sound/03_goede_kabel_groep.mp3", "-o", "local"])
            print("flitslicht b groen aan 4s")
            subprocess.Popen(["python", "flits_b_groen.py"])
      elif b_boven.value and not all([b_onder.value, b_midden.value, b_boven.value]): #
            audio_03 = subprocess.Popen(["omxplayer", "static/sound/03_goede_kabel_groep.mp3", "-o", "local"])
            print("flitslicht b groen aan 4s")
            subprocess.Popen(["python", "flits_b_groen.py"])
      elif all([b_onder.value, b_midden.value, b_boven.value]): #CIRCUIT B COMPLEET
            print("flitslicht B groen aan")
            print("ledstrip blauw")
            flits_b_groen.on()
            ledstrip_rood.off()
            ledstrip_blauw.on()
            audio_04 = subprocess.Popen(["omxplayer", "static/sound/04_goede_kabels_all.mp3", "-o", "local"])
            audio_05 = subprocess.Popen(["python", "audio_05_303s.py"])
            if battery_slider >= 267: 
                  battery_slider = 267
                  battery_text = 100
                  audio_05.kill()
                  audio_06 = subprocess.Popen(["omxplayer", "static/sound/06_opstart_engine.mp3", "-o", "local"]) #16S moet de slider duren
                  while generator_text < 100:
                        generator_text += 1
                        generator_slider += 67.8125
                        time.sleep(0.16)
                  if generator_text == 100:
                        generator_slider = 1085
                        status_100 = True
            else:
                  mess_04 = "hidden"
                  mess_05 = "visible"
                  bike_01 = chan_01.value / 29000 # 29000 is de max wanneer je hard fietst
                  bike_02 = chan_02.value / 29000 # 29000 is de max wanneer je hard fietst
                  battery_slider += int(bike_01) + int(bike_02) #max 267
                  battery_text = int(battery_slider/2.7)
                  if bike_01 >= 1 or bike_02 >= 1:
                        battery_volt = 230
                  if bike_01 and bike_02:
                        battery_ampere = 32
                  elif bike_01 and not bike_02:
                        battery_ampere = 16
                  elif bike_02 and not bike_01:
                        battery_ampere = 16
                  print('batt_slider: ', battery_slider)
                  print('batt_text: ', battery_text)
                  print('bike_01:',bike_01, chan_01.value, chan_01.voltage)
                  print('bike_02:',bike_02, chan_02.value, chan_02.voltage)
            _data_battery = json.dumps({
                    "generator_slider": generator_slider,
                    "generator_text": generator_text,
                    "battery_slider": battery_slider,
                    "battery_volt": battery_volt,
                    "battery_ampere": battery_ampere,
                    "battery_text": battery_text,
                    "mess_04": mess_04,
                    "mess_05": mess_05,
              })
            yield f"id: 1\ndata: {_data_battery}\nevent: battery\n\n"
      if status_100 == True:
            mess_05 = "hidden"
            mess_06 = "visible"
            print("ledstrip groen")
            ledstrip_blauw.off()
            ledstrip_groen.on()
            time.sleep(10)
            mess_05 = "hidden"
            mess_06 = "visible"
            _data_status_100 = json.dumps({
                    "mess_05": mess_05,
                    "mess_06": mess_06
              })
            yield f"id: 1\ndata: {_data_status_100}\nevent: status_100\n\n"
            time.sleep(10)
            generator_100 = True
      if generator_100 == True:
            mess_06 = "hidden"
            mess_07 = "visible"
            audio_07 = subprocess.Popen(["omxplayer", "static/sound/07_pop_updated.mp3", "-o", "local"])    
            _data_generator_100 = json.dumps({
                    "mess_06": mess_06,
                    "mess_07": mess_07
              })
            yield f"id: 1\ndata: {_data_generator_100}\nevent: generator_100\n\n"            
      time.sleep(0.1)
  return Response(respond_to_client(), mimetype='text/event-stream')
  

##############################
if __name__ == "__main__":
  # app.run(port=80, debug=True)
  http_server = WSGIServer(("localhost", 8080), app)
  http_server.serve_forever()