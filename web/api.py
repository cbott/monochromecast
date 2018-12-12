import flask
from hardware import tv
import time
tv = tv.TV_Controller()
app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/api/status')
def api_status():
    return flask.jsonify({
        'enabled': tv.enabled,
    })

@app.route('/api/enable')
def api_enable():
    tv.enable_system()
    return ''

@app.route('/api/disable')
def api_disable():
    tv.disable_system()
    return ''

@app.route('/api/brightness/<int:b>')
def api_brightness(b):
    tv.set_brightness(b)
    return ''

@app.route('/api/gradient/<int:a>/<int:b>')
def api_gradient(a, b):
    for i in range(a, b+1, 1 if a < b else -1):
        tv.set_brightness(i)
        time.sleep(0.01)
    return ''

