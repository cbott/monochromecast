import flask
import hardware
tv = hardware.TV_Controller()
app = flask.Flask(__name__)

@app.route('/')
def index():
	return 'hi'

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

