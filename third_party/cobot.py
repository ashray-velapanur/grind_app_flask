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

	def create_membership(self, name, country):
		params = {
			"plan[id]": 'ddf097bfe38f9ac8598a97478f27a9ca',
			"address[name]": name,
			"address[country]": country,
			"access_token": self.access_token
		}
		url = "https://grind.cobot.me/api/memberships?"
		try:
			return json.loads(urllib2.urlopen(url, data=urllib.urlencode(params)).read())
		except urllib2.HTTPError as e:
			return e.read()