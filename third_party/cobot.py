import json

import urllib, urllib2
import json
import datetime

from config import COBOT

class CobotAPI(object):
	def __init__(self, config=COBOT):
		self.client_id = config['client_id']
		self.client_secret = config['client_secret']
		self.scope = config['scope']
		self.redirect_uri = config['redirect_uri']
		self.access_token = config['access_token']

	def auth_url(self):
		return "https://www.cobot.me/oauth/authorize?response_type=code&client_id=%s&redirect_uri=%s&state=&scope=%s"%(self.client_id, self.redirect_uri, self.scope)

	def get_access_token(self, code):
		params = {
			"client_id": self.client_id,
			"client_secret": self.client_secret,
			"grant_type": "authorization_code",
			"code": code
		}
		url = "https://www.cobot.me/oauth/access_token?"
		response = json.loads(urllib2.urlopen(url, data=urllib.urlencode(params)).read())
		return response['access_token']
