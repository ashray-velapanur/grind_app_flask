from config import SUPERSAAS
import requests
from flask import Flask, render_template, request, redirect, json, session, jsonify

import urllib, urllib2

class SuperSaasAPI(object):
	def __init__(self, config=SUPERSAAS):
		self.username = config['username']
		self.password = config['password']

	def bookings(self):
		url = "http://www.supersaas.com/api/bookings?"
		data = {
			'schedule_id': '250803',
			'password': self.password,
			'booking[start]': '2015-12-14 12:00',
			'booking[finish]': '2015-12-14 16:00',
			'booking[full_name]': 'test 2',
			'booking[email]': 'asdashray@beagles.com',
			'booking[field_1]': 'ashray@beagles.com'
		}
		print url
		print urllib.urlencode(data)
		try:
			print urllib2.urlopen(url, data=urllib.urlencode(data)).read()
		except urllib2.HTTPError as e:
			print e.read()
