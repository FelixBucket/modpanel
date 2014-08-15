from django.conf import settings
import pyjsonrpc

class RPC(object):

	def __init__(self, url=settings.RPC_ENDPOINT, username=settings.RPC_USERNAME, password=settings.RPC_PASSWORD):
		self.client = pyjsonrpc.HttpClient(url=url, username=username, password=password)
