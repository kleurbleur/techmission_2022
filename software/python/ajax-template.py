from flask import Flask, request, render_template, jsonify
import datetime
import time
import threading

app = Flask(__name__)

running = False # to control loop in thread
value = 0       

def rpi_function():
    global value

    print('start of thread')
    while running: # global variable to stop loop  
        value += 1
        time.sleep(0.01)
    print('stop of thread')


@app.route('/')
@app.route('/<device>/<action>')
def index(device=None, action=None):
    global running # make running global so the function in the thread can access it
    global value # make value global so the function in the thread can access it

    if device:
        if action == 'on':
            if not running:
                print('start')
                running = True
                threading.Thread(target=rpi_function).start() # refer to the function above
            else:
                print('already running')
        elif action == 'off':
            if running:
                print('stop')
                running = False  # it should stop thread
            else:
                print('not running')

    return render_template('ajax.html')

@app.route('/update', methods=['POST'])
def update():
    return jsonify({
        'value': value,
        'time': datetime.datetime.now().strftime("%H:%M:%S"),
    })

app.run() #debug=True