from cgi import parse_qs
from requests_oauthlib import OAuth1
import requests

class RequestError(Exception):
	def __init__(self, r):
		self.request = r
	

class TwitterClient():
	@staticmethod
	def OAuth(consumer_key, consumer_secret, access_key=None, access_secret=None, callback_url=None):
		''' Construct a OAuth Object '''
		return OAuth1(
		client_key = consumer_key,
		client_secret = consumer_secret,
		resource_owner_key = access_key,
		resource_owner_secret = access_secret,
		callback_uri = callback_url
		)
	
	
	def get(self, oauth, url):
		r = requests.get(url=url, auth=oauth)
		if r.status_code==200: return r
		else:
			raise RequestError(r)
	
	def post(self, oauth, url, data):
		r = requests.get(url=url, data=data, auth=oauth)
		if r.status_code==200: return r
		else:
			raise RequestError(r)
	
	
	def get_authorize_url(self, oauth):
		request_url = "https://api.twitter.com/oauth/request_token"
		authorize_url = "https://api.twitter.com/oauth/authorize"
		r = self.get(oauth, request_url)
		
		token = parse_qs(r.text)['oauth_token'][0]
		authorize_url += "?oauth_token=%s" % token
		return authorize_url
	
	def get_access_token(self, oauth, token, verifier):
		access_url = "https://api.twitter.com/oauth/access_token"
		oauth.client.resource_owner_key = token
		data = {'oauth_verifier': verifier}
		r = self.post(oauth, access_url, data) 
		result = parse_qs(r.text)
		return result["user_id"][0], result["oauth_token"][0], result["oauth_token_secret"][0]
	
	
	def load_usrtl(self, oauth, since_id, count=200):
		''' Load User Timeline 
		response will contain one tweet at least( since_id ).
		'''
		url = "https://api.twitter.com/1.1/statuses/user_timeline.json?trim_user=1"
		url += "&since_id=%s" % since_id  if since_id else ''
		url += "&max_id=%s" % max_id  if max_id else ''
		url += "&count=%s" % count  if count>0 else ''
		r = self.get(oauth, url)
	
	def tweet(self, status):
		''' Post Tweet
		'''
		url = "https://api.twitter.com/1.1/statuses/update.json"
		data = {'status':  status}
		r = self.post(oauth, url, data)
	
