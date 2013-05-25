from base64 import b64encode
from hmac import new as hmac
import urllib.parse
import hashlib, random, time
import requests

class RequestError(Exception):
	def __init__(self, r):
		self.request = r

class OAuthClient():
	def __init__(self, consumer_key, consumer_secret, callback_url=''):
		self.consumer_key = consumer_key
		self.consumer_secret = consumer_secret
		self.callback_url = callback_url
		
		self.oauth_headers = {'Authorization': 'OAuth'}
	
	#@private_method:
	def _quote(self, text):
		return urllib.parse.quote(str(text), '')
	
	def _normalize_parameters(self, params):
		return '&'.join([ '%s=%s' % (self._quote(k), self._quote(params[k])) for k in sorted(params) ])
	
	def _form_signed_params(self, method, url, token='', secret='', additional_params={}):
		''' Form Signed Params
		'''
		# Add OAuth parameters.
		params = {
			'oauth_consumer_key': self.consumer_key,
			'oauth_signature_method': 'HMAC-SHA1',
			'oauth_timestamp': str(int(time.time())),
			'oauth_nonce': str(random.getrandbits(64)),
			'oauth_version': '1.0'
		}
		params.update(additional_params)
		if token:	params['oauth_token'] = token
		else: 		params['oauth_callback'] = self.callback_url
		
		# Create a message of the params.
		params_string = self._normalize_parameters(params)
		message = ('&'.join([ self._quote(method), self._quote(url), self._quote(params_string) ])).encode('utf-8')
		
		# Create a HMAC-SHA1 signature of the message.
		key = ('%s&%s' % (self.consumer_secret, secret)).encode('utf-8')
		signature = hmac(key, message, hashlib.sha1)
		params['oauth_signature'] = b64encode(signature.digest()).strip()
		
		return params
	
	#@public_method:
	def get (self, url, params={}, token='', secret=''):
		params = self._form_signed_params('GET', url, token, secret, params)
		r = requests.get(url=url, headers=self.oauth_headers, params=params)
		if r.status_code==200: return r
		else: raise RequestError(r)
	
	def post(self, url, params={}, token='', secret=''):
		params = self._form_signed_params('POST', url, token, secret, params)
		r = requests.post(url=url, headers=self.oauth_headers, params=params)
		if r.status_code==200: return r
		else: raise RequestError(r)
	