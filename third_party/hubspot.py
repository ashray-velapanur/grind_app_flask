from config import HUBSPOT
import requests
from flask import Flask, render_template, request, redirect, json, session, jsonify

class HubspotAPI(object):
	def __init__(self, config=HUBSPOT):
		self.client_id = config['client_id']
		self.scope = config['scope']
		self.redirect_uri = config['redirect_uri']
		self.portal_id = config['portal_id']
		self.access_token = config['access_token']
		self.refresh_token = config['refresh_token']
		self.api_key = config['api_key']

	def auth_url(self):
		return "https://app.hubspot.com/auth/authenticate?client_id=%s&portalId=%s&redirect_uri=%s&scope=%s"%(self.client_id, self.portal_id, self.redirect_uri, self.scope)

	def get_contacts(self):
		response = requests.get(
			"https://api.hubapi.com/contacts/v1/lists/all/contacts/all?hapikey="+self.api_key+"&count=20",
			headers = {
			    "Authorization": "Bearer "+self.access_token,
			},
			verify = False,  # Verify SSL certificate
		)
		contacts_list = response.json()['contacts']
		return jsonify({'contacts':contacts_list})
