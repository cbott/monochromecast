import flask
import hardware
import time
tv = hardware.TV_Controller()
app = flask.Flask(__name__)

@app.route('/')
def index():
	return '''
<script>
function seizure(i){
	i = (i === undefined) ? 30 : i;
	fetch('/api/brightness/' + 100 * (i % 2)).then(function() {
		if (i > 0) seizure(i - 1);
	});
}
</script>
<button onclick="fetch('/api/enable')">Enable</button>
<button onclick="fetch('/api/disable')">Disable</button>
<button onclick="fetch('/api/gradient/0/100')">Up</button>
<button onclick="fetch('/api/gradient/100/0')">Down</button>
<button onclick="seizure()">Seizure</button>
'''

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

