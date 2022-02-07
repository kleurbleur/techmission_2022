from gevent import monkey; monkey.patch_all()
from flask import Flask, Response, render_template
from gevent.pywsgi import WSGIServer
import json, time, board, busio
i2c = busio.I2C(board.SCL, board.SDA)
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

app = Flask(__name__)

ads = ADS.ADS1115(i2c)
chan = AnalogIn(ads, ADS.P0)


generator_slider = 0
generator_volt = 0
generator_ampere = 0
battery_text = 0
battery_slider = 0 #max 267 value
battery_volt = 0
battery_ampere = 0
bike_01 = 0
bike_02 = 0
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
      global bike_01
      global battery_text
      global generator_slider
      global battery_slider
      global mess_05
      # print('gen_counter: ', generator_slider)
      print('bike_01: ', bike_01)
      print(chan.value, chan.voltage)
      if battery_slider >= 267:
        mess_05 = "visible"
        battery_slider = 267
        battery_text = 100
      else:
        bike_01 = chan.value / 1000
        battery_slider += int(bike_01)
        battery_text = int(battery_slider/2.7)
        print('batt_slider: ', battery_slider)
        print('batt_text: ', battery_text)
      _data = json.dumps({
        "generator_slider": generator_slider,
        "battery_slider": battery_slider,
        "battery_text": battery_text,
        "mess_05": mess_05
        })
      yield f"id: 1\ndata: {_data}\nevent: online\n\n"
      time.sleep(0.1)
  return Response(respond_to_client(), mimetype='text/event-stream')
  

##############################
if __name__ == "__main__":
  # app.run(port=80, debug=True)
  http_server = WSGIServer(("localhost", 8080), app)
  http_server.serve_forever()