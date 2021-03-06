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


generator_counter = 100
battery_counter = 10
bike_01 = 0
mess_05 = "hidden"


##############################
@app.route("/")
def render_index():
  return render_template("interface.html")

##############################
@app.route("/listen")
def listen():

  def respond_to_client():
    while True:
      global bike_01
      global generator_counter
      global battery_counter
      global mess_05
      # print('gen_counter: ', generator_counter)
      print('batt_counter: ', battery_counter)
      print('bike_01: ', bike_01)
      # generator_counter += 1
      print(chan.value, chan.voltage)
      if battery_counter >= 300:
        mess_05 = "visible"
      else:
        bike_01 = chan.value / 1000
        battery_counter += int(bike_01)
        # battery_counter += 2
      _data = json.dumps({
        "generator_counter": generator_counter,
        "battery_counter": battery_counter,
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