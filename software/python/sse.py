from flask import Flask, render_template
from flask_sse import sse
import datetime

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/stream')



@app.route('/')
def index():
    now = datetime.datetime.now().strftime("%H:%M:%S")
    sse.publish({"message": now}, type='greeting')    
    return render_template("index.html")

# @app.route('/hello')
# def publish_hello():
#     return now