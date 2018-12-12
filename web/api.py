import flask
import socket
import time
app = flask.Flask(__name__)

def hw_send(msg):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(msg.encode(), ('127.0.0.1', 8900))

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/api/status')
def api_status():
    return flask.jsonify({
        # 'enabled': tv.enabled,
    })

@app.route('/api/enable')
def api_enable():
    hw_send('e')
    return ''

@app.route('/api/disable')
def api_disable():
    hw_send('d')
    return ''

@app.route('/api/brightness/<int:b>')
def api_brightness(b):
    hw_send(str(b))
    return ''

@app.route('/api/gradient/<int:a>/<int:b>')
def api_gradient(a, b):
    dir = 1 if a < b else -1
    for i in range(a, b + dir, dir):
        hw_send(str(i))
        time.sleep(0.01)
    return ''

