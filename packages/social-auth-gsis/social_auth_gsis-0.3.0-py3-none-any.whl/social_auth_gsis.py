from django.conf import settings
from social_core.backends.oauth import BaseOAuth2


class GSISOAuth2(BaseOAuth2):
	"""GSIS OAuth 2.0 authentication backend"""
	name = 'gsis'
	AUTHORIZATION_URL = 'https://www1.gsis.gr/oauth2server/oauth/authorize'
	ACCESS_TOKEN_URL = 'https://www1.gsis.gr/oauth2server/oauth/token'
	ACCESS_TOKEN_METHOD = 'POST'
	SCOPE_SEPARATOR = ','


class GSISOAuth2Testing(GSISOAuth2):
	AUTHORIZATION_URL = 'https://test.gsis.gr/oauth2server/oauth/authorize'
	ACCESS_TOKEN_URL = 'https://test.gsis.gr/oauth2server/oauth/token'
