import requests
from keys import *

def auth(url):
	files = {
	    'client_secret': (None, CLIENT_SECRET),
	    'client_id': (None, CLIENT_ID),
	    'grant_type': (None, 'authorization_code'),
	    'redirect_uri': (None, REDIRECT_URI),
	    'code': (None, uri),
	}

	response = requests.post('https://login.uber.com/oauth/v2/token', files=files)
	print response.json()['access_token']
