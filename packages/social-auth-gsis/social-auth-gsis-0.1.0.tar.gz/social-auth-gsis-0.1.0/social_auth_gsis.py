from social_core.backends.oauth import BaseOAuth2

class GSISOAuth2(BaseOAuth2):
	"""GSIS OAuth 2.0 authentication backend"""
	name = 'gsis'
	AUTHORIZATION_URL = 'https://www1.gsis.gr/oauth2server/oauth/authorize'
	ACCESS_TOKEN_URL = 'https://www1.gsis.gr/oauth2server/oauth/token'
	ACCESS_TOKEN_METHOD = 'POST'
	SCOPE_SEPARATOR = ','
	

	def get_user_details(self, response):
		pass

	def user_data(self, access_token, *args, **kwargs):
		pass