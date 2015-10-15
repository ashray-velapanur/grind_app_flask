from config import HUBSPOT

class HubspotAPI(object):
	def __init__(self, config=HUBSPOT):
		self.client_id = config['client_id']
		self.scope = config['scope']
		self.redirect_uri = config['redirect_uri']
		self.portal_id = config['portal_id']