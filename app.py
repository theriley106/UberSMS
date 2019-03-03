# Copy of http://stackoverflow.com/a/20104705
from flask import Flask, render_template, request, url_for, redirect, Markup, jsonify, make_response, send_from_directory, session
from flask import Flask, render_template
from flask_sockets import Sockets
import random
import datetime
import time
import os
import auth2
from keys import *

app = Flask(__name__, static_url_path='/static')
URL = "https://login.uber.com/oauth/v2/authorize?response_type=code&client_id={}&scope=all_trips+delivery+history+history_lite+places+profile+request+request_receipt+ride_widgets&redirect_uri={}".format(CLIENT_ID, REDIRECT_URI)
KEYS = ["JA.VUNmGAAAAAAAEgASAAAABwAIAAwAAAAAAAAAEgAAAAAAAAG8AAAAFAAAAAAADgAQAAQAAAAIAAwAAAAOAAAAkAAAABwAAAAEAAAAEAAAAOaTmxEFtIZpiCsp1RiVVc9sAAAAFV1Fgn8m3lYna4mDfwUGyH8whQN2kUfxq2itj0ovDUi6lW7YY-iCCdVzXci0bUKU4O0XRSJTpdV_YUN3gHQWE2z94S_BncBSUtj0KdkLE8a0x4f_t7Yck6fmOSjiYUvEM3FUHdxMBjA665xDDAAAAICeDMMNMTHl4dD5RyQAAABiMGQ4NTgwMy0zOGEwLTQyYjMtODA2ZS03YTRjZjhlMTk2ZWU"]
sockets = Sockets(app)

print URL
LIST_VALS = [False]

@sockets.route('/echo')
def echo_socket(ws):
	cache = random.randint(1, 99999)
	total = 0
	while True:
		#message = ws.receive()
		if LIST_VALS[0] == False:
			ws.send('<img style="height:300px;width:300px" src="static/frame.png?cache={}"></img>'.format(cache))
			time.sleep(.1)
		elif LIST_VALS[0] == True:
			total += 1
			if total > 100:
				LIST_VALS[0] = None
			ws.send('<img style="height:300px;width:300px" src="static/spinny.gif?cache={}"></img><br><center><p>Authorizing on mobile device</p></center>'.format(cache))
			time.sleep(.1)
		else:
			ws.send('<img style="height:300px;width:300px" src="static/uber.png?cache={}"></img><br><center><p>Authorization now complete</p></center>'.format(cache))
			time.sleep(.1)

@app.route('/')
def hello():
	return 'Hello World!'

@app.route('/rider', methods=['GET'])
def echo_test():
	LIST_VALS[0] = False
	return render_template('example.html')

@app.route('/driver', methods=['GET'])
def echo_test_driver():
	return render_template('driver.html')

@app.route('/done', methods=['GET'])
def scan_qr():
	LIST_VALS[0] = True
	return render_template('authorized.html')

@app.route('/last', methods=['GET'])
def last():
	LIST_VALS[0] = None
	return jsonify({"success": True})
	return "Finished"

@app.route('/startAuth')
def startAuth():
	LIST_VALS[0] = True
	return redirect(URL, code=302)

@app.route('/auth', methods=['GET'])
def auth():
	code = request.args.get("code")
	print code
	g = auth2.authorize(code)
	print g
	KEYS.append(g)
	return str(g)

@app.route('/ride', methods=['GET'])
def sendTo():
	request.args.get("fromState")
	request.args.get("fromCity")
	request.args.get("toCity")
	request.args.get("toState")
	code = request.args.get("code")
	print code
	g = auth2.authorize(code)
	print g
	return str(g)

@app.route('/options', methods=['GET'])
def getOptions():
	lat1 = request.args.get("lat1")
	lng1 = request.args.get("lng1")
	lat2 = request.args.get("lat2")
	lng2 = request.args.get("lng2")
	headers = {
	    'Authorization': 'Bearer {}'.format(KEYS[-1]),
    	'Content-Type': 'application/json',
	}

	params = (
	    ('start_latitude', lat1),
	    ('start_longitude', lng1),
	    ('end_latitude', lat2),
	    ('end_longitude', lng2),
	)

	response = requests.get('https://api.uber.com/v1.2/estimates/price', headers=headers, params=params)
	return response.text

if __name__ == '__main__':
	app.run('0.0.0.0')
	# Start with gunicorn -k flask_sockets.worker app:app


