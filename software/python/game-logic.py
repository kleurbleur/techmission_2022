from ast import And
from gevent import monkey; monkey.patch_all()
from flask import Flask, Response, render_template
from gevent.pywsgi import WSGIServer
import json, time, board, busio, subprocess
i2c = busio.I2C(board.SCL, board.SDA)
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

app = Flask(__name__)

ads = ADS.ADS1115(i2c)
chan_01 = AnalogIn(ads, ADS.P0)
chan_02 = AnalogIn(ads, ADS.P3)

start = True
reset_button = False
scanner_video = 0
scanner_running = False
audio_01 = ""
audio_02 = ""
audio_03 = ""
audio_04 = ""
audio_05 = ""
audio_06 = ""
audio_07 = ""
audio_08 = ""
cables_a1 = True
cables_a2 = True
cables_a3 = True
cables_b1 = False
cables_b2 = False
cables_b3 = False
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
      global audio_01
      global audio_02
      global audio_03
      global audio_04
      global audio_05
      global audio_06
      global audio_07
      global audio_08
      global cables_a1
      global cables_a2
      global cables_a3
      global cables_b1
      global cables_b2
      global cables_b3
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
      if start == True and cables_a1 == True and cables_a2 == True and cables_a3 == True: #START OF THE INSTALLATION
            if scanner_running == False:
                  print("start scanner video")
                  scanner_video = subprocess.Popen(["omxplayer", "static/video/test.mp4", "--loop", "--display=7"])
            print("flitslicht A rood aan")
            print("ledstrip rood aan")
            print("audio kortsluiting aan")
            audio_01 = subprocess.Popen(["omxplayer", "static/sound/01_kortsluiting_alarm_loop.mp3", "--loop"])
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
                "battery_slider": battery_slider,
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
      if not all([cables_a1, cables_a2, cables_a3]): #CABLES A OUT
            print("flitslicht B oranje aan")
            print("ledstrip oranje aan")  
            audio_01.kill()
            audio_02 = subprocess.Popen(["omxplayer", "static/sound/02_kortsluiting_standby_loop.mp3", "--loop"])
            mess_03 = "hidden"
            mess_04 = "visible"      
            _data_cable_a = json.dumps({
                "mess_03": mess_03,
                "mess_04": mess_04,
            })
            yield f"id: 1\ndata: {_data_cable_a}\nevent: cable_a\n\n" #we push the data towards the interface per event
      if cables_b1 and not all([cables_b1, cables_b2, cables_b3]): #
            audio_03 = subprocess.Popen(["omxplayer", "static/sound/03_goede_kabel_groep.mp3"])
            print("flitslicht b groen aan 4s") #TIMER UITZOEKEN
      elif cables_b2 and not all([cables_b1, cables_b2, cables_b3]): #
            audio_03 = subprocess.Popen(["omxplayer", "static/sound/03_goede_kabel_groep.mp3"])
            print("flitslicht b groen aan 4s") #TIMER UITZOEKEN
      elif cables_b3 and not all([cables_b1, cables_b2, cables_b3]): #
            audio_03 = subprocess.Popen(["omxplayer", "static/sound/03_goede_kabel_groep.mp3"])
            print("flitslicht b groen aan 4s") #TIMER UITZOEKEN - apart python script met simple timer en gpio handeling?
      elif all([cables_b1, cables_b2, cables_b3]):
            mess_04 = "hidden"
            print("flitslicht B groen aan")
            print("ledstrip blauw")
            audio_04 = subprocess.Popen(["omxplayer", "static/sound/04_goede_kabels_all.mp3"])
            audio_05 = subprocess.Popen(["omxplayer", "static/sound/05_kabels_ok_loop.mp3"])
            if battery_slider >= 267: 
                  battery_slider = 267
                  battery_text = 100
                  status_100 = True
                  audio_05.kill()
                  audio_06 = subprocess.Popen(["omxplayer", "static/sound/06_opstart_engine.mp3"]) #TIMER NODIG!
                  #status slider oplaten lopen naar 100% in sync met geluid!
            else:
                  mess_05 = "visible"
                  bike_01 = chan_01.value / 1000
                  bike_02 = chan_02.value / 1000
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
                  print(chan_01.value, chan_01.voltage)
                  print(chan_02.value, chan_02.voltage)
            _data_battery = json.dumps({
                    "generator_slider": generator_slider,
                    "battery_slider": battery_slider,
                    "battery_text": battery_text,
                    "mess_04": mess_04,
                    "mess_05": mess_05,
              })
            yield f"id: 1\ndata: {_data_battery}\nevent: battery\n\n"
      if status_100 == True:
            mess_05 = "hidden"
            mess_06 = "visible"
            print("ledstrip groen")
            time.sleep(10)
            mess_06 = "hidden"
            mess_07 = "visible"
            audio_07 = subprocess.Popen(["omxplayer", "static/sound/07_pop_updated.mp3"])             
      time.sleep(0.1)
  return Response(respond_to_client(), mimetype='text/event-stream')
  

##############################
if __name__ == "__main__":
  # app.run(port=80, debug=True)
  http_server = WSGIServer(("localhost", 8080), app)
  http_server.serve_forever()