from gevent import monkey; monkey.patch_all()
from flask import Flask, Response, render_template, stream_with_context
from gevent.pywsgi import WSGIServer
import json
import time

app = Flask(__name__)
counter = 100

##############################
@app.route("/")
def render_index():
  return render_template("index.html")

##############################
@app.route("/listen")
def listen():

  def respond_to_client():
    while True:
      global counter
      print(counter)
      counter += 1
      _data = json.dumps({"counter":counter})
      yield f"id: 1\ndata: {_data}\nevent: online\n\n"
      time.sleep(0.1)
  return Response(respond_to_client(), mimetype='text/event-stream')
  

##############################
if __name__ == "__main__":
  # app.run(port=80, debug=True)
  http_server = WSGIServer(("localhost", 8080), app)
  http_server.serve_forever()