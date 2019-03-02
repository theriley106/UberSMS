from flask import Flask, render_template, request, url_for, redirect, Markup, jsonify, make_response, send_from_directory, session
import requests
import os
import auth2
from keys import *

app = Flask(__name__, static_url_path='/static')
URL = "https://login.uber.com/oauth/v2/authorize?response_type=code&client_id={}&scope=all_trips+delivery+history+history_lite+places+profile+request+request_receipt+ride_widgets&redirect_uri={}".format(CLIENT_ID, REDIRECT_URI)

@app.route('/', methods=['GET'])
def index():
	return render_template("index.html")

@app.route('/startAuth')
def startAuth():
	return redirect(URL, code=302)

@app.route('/auth', methods=['GET'])
def auth():
	code = request.args.get("code")
	print code
	g = auth2.authorize(code)
	print g
	return str(g)


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=8000)
