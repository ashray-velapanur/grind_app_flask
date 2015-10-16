from flask import Flask, render_template, request, redirect, json, session, jsonify
from third_party.hubspot import HubspotAPI

def hubspot_auth_handler():
	api = HubspotAPI()
	return redirect(api.auth_url())

def hubspot_callback_handler():
	access_token = request.args.get('access_token', None)
	refresh_token = request.args.get('refresh_token', None)
	print access_token, refresh_token

def hubspot_contacts_handler():
	api = HubspotAPI()
	return api.get_contacts()

def hubspot_search_handler():
	api = HubspotAPI()
	return api.search_contacts()

def hubspot_create_contact_handler():
	api = HubspotAPI()
	return api.create_contact()

def hubspot_deal_create_handler():
	return HubspotAPI().create_deal()

def hubspot_deal_update_handler():
	return HubspotAPI().update_deal()

def hubspot_deal_list_handler():
	return jsonify({'results':HubspotAPI().get_deals()})

def hubspot_workflows_list_handler():
	return HubspotAPI().get_workflows()

def hubspot_workflows_create_handler():
	return HubspotAPI().create_workflow()