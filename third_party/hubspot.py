from config import HUBSPOT

class HubspotAPI(object):
	def __init__(self, config=HUBSPOT):
		self.client_id = config['client_id']
		self.scope = config['scope']
		self.redirect_uri = config['redirect_uri']
		self.portal_id = config['portal_id']

	def auth_url(self):
		return "https://app.hubspot.com/auth/authenticate?client_id=%s&portalId=%s&redirect_uri=%s&scope=%s"%(self.client_id, self.portal_id, self.redirect_uri, self.scope)