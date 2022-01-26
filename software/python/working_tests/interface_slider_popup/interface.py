from gevent import monkey; monkey.patch_all()
from flask import Flask, Response, render_template, stream_with_context
from gevent.pywsgi import WSGIServer
import json
import time

app = Flask(__name__)
generator_counter = 100
battery_counter = 10
mess_05 = "hidden"


##############################
@app.route("/")
def render_index():
  return render_template("index.html")

##############################
@app.route("/listen")
def listen():

  def respond_to_client():
    while True:
      global generator_counter
      global battery_counter
      global mess_05
      print('gen_counter: ', generator_counter)
      print('batt_counter: ', battery_counter)
      generator_counter += 1
      if battery_counter == 300:
        mess_05 = "visible"
      else:
        battery_counter += 2
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