from config import HUBSPOT
import requests
from flask import Flask, render_template, request, redirect, json, session, jsonify

import urllib, urllib2


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
	
	def create_deal(self):
		name = request.form['name']
		amount = request.form['amount']
		response = requests.post(
			"https://api.hubapi.com/deals/v1/deal?hapikey=" + self.api_key + '&portalId=1713132',
			headers = {
				"Content-Type": 'application/json'
			},
			verify = False,  # Verify SSL certificate
			data = json.dumps({"associations":{"associatedCompanyIds":[63732902],"associatedVids":[3]},"portalId": 1713132,"properties":[{"value": name,"name": "dealname"},{"value": "appointmentscheduled","name": "dealstage"},{"value": "","name": "hubspot_owner_id"},{"value": 1409443200000,"name": "closedate"},{"value": amount,"name": "amount"},{"value": "newbusiness","name": "dealtype"}]})
		)
		return jsonify(response.json())

	def update_deal(self):
		name = request.form['property']
		value = request.form['value']
		id = request.form['id']
		response = requests.put(
			"https://api.hubapi.com/deals/v1/deal/"+id+"?hapikey=" + self.api_key + '&portalId=1713132',
			headers = {
				"Content-Type": 'application/json'
			},
			verify = False,  # Verify SSL certificate
			data = json.dumps({"properties":[{"value": value,"name": name}]})
		)
		return jsonify(response.json())

	def get_deals(self):
		response = requests.get(
			"https://api.hubapi.com/deals/v1/deal/recent/created?hapikey=" + self.api_key,
			verify = False,  # Verify SSL certificate
		)
		deals_list = response.json()['results']
		return deals_list

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

	def search_contacts(self):
		query = request.form['query']
		response = requests.get(
			"https://api.hubapi.com/contacts/v1/search/query?hapikey="+self.api_key+"&q="+query,
			headers = {
			    "Authorization": "Bearer "+self.access_token,
			},
			verify = False,  # Verify SSL certificate
		)
		contacts_list = response.json()['contacts']
		return jsonify({'contacts':contacts_list})

	def create_contact(self):
		form_guid = "3a58aefb-3ded-4b10-b0cf-5d23921fec53"
		response = requests.post(
			"https://forms.hubspot.com/uploads/form/v2/"+self.portal_id+"/"+form_guid,
			headers = {
				"Authorization": "Bearer "+self.access_token
			},
			verify = False,  # Verify SSL certificate
			data = {
				"firstname":request.form['first_name'],
				"lastname":request.form['last_name'],
				"email":request.form['email']
			}
		)
		return redirect("/hubspot/contacts")

	def get_workflows(self):
		response = requests.get(
			"https://api.hubapi.com/automation/v3/workflows?hapikey="+self.api_key+"&count=20",
			verify = False,  # Verify SSL certificate
		)
		workflows_list = response.json()['workflows']
		return jsonify({'workflows':workflows_list})

	def create_workflow(self):
		name = request.form['name']
		params = {
			"enabled": False,
			"allowContactToTriggerMultipleTimes": True,
			"name": name,
			"onlyExecOnBizDays": False,
			"canEnrollFromSalesforce": False,
			"type": "DRIP_DELAY",
			"nurtureTimeRange": {
			    "enabled": False,
			    "startHour": 9,
			    "stopHour": 17
			},
			"unenrollmentSetting": {
			    "excludedWorkflows": [],
			    "type": "NONE"
			},
			"actions": [
			    {
			        "newValue": "HubSpot",
			        "propertyName": "company",
			        "type": "SET_CONTACT_PROPERTY"
			    }
			],
			"goalListIds": [],
			"listening": False
		}
		response = requests.post(
			"https://api.hubapi.com/automation/v3/workflows?hapikey=" + self.api_key,
			headers = {
				"Content-Type": 'application/json'
			},
			verify = False,  # Verify SSL certificate
			data = json.dumps(params)
		)
		return jsonify(response.json())