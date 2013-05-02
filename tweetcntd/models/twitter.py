from hmac import new as hmac
from base64 import b64encode as base64
import urllib.parse
import hashlib, random, time

class OAuthClient():
	def __init__(self, consumer_key, consumer_secret, request_url, access_url, callback_url=None):
		''' Constructor '''
		self.consumer_key = consumer_key
		self.consumer_secret = consumer_secret
		self.request_url = request_url
		self.access_url = access_url
		self.callback_url = callback_url
	
	def quote(text):
		return urllib.parse.quote(text, '')
	
	def normalize_params(self, params):
		return '&'.join([ '%s=%s' % (self.quote(k), self.quote(params[k])) for k in sorted(params) ])
	
	def form_signed_params(self, url, method, token="", secret="", addition_params={}):
		''' Form Signed Params
		'''
		
		# Create a params.
		params = {
			"oauth_consumer_key": self.consumer_key,
			"oauth_signature_method": "HMAC-SHA1",
			"oauth_timestamp": str(int(time.time())),
			"oauth_nonce": str(random.getrandbits(64)),
			"oauth_version": "1.0"
		}
		params.update(additional_params)
		
		if token:	params["oauth_token"] = token
		else 		params["oauth_callback"] = self.callback_url
		
		# Create a message of the params.
		params_str = self.normalize_params(params)
		message = ('&'.join([ self.quote(method), self.quote(url), self.quote(params_str) ])).encode('utf-8')
		
		# Create a HMAC-SHA1 signature of the message.
		key = ('%s&%s' % (self.consumer_secret, secret)).encode('utf-8')
		signature = hmac(key, message, hashlib.sha1)
		params["oauth_signature"] = base64(signature.digest()).strip()
		
		return self.normalize_params(params)
	
	