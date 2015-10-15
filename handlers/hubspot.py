from third_party.hubspot import HubspotAPI

def auth_handler():
	api = HubspotAPI()
	return redirect(api.auth_url())

def callback_handler():
	access_token = request.args.get('access_token', None)
	refresh_token = request.args.get('refresh_token', None)
	print access_token, refresh_token