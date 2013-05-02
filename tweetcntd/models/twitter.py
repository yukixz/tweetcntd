from cgi import parse_qs
from requests_oauthlib import OAuth1
import requests

class TwitterClient():
	def __init__(self, consumer_key, consumer_secret, callback_url=None, access_key=None, access_secret=None):
		''' Constructor '''
		self.oauth = OAuth1(
		client_key = consumer_key,
		client_secret = consumer_secret,
		callback_uri = callback_url,
		resource_owner_key = access_key,
		resource_owner_secret = access_secret
		)
	
	def get(url):
		r = requests.get(url=url, auth=self.oauth)
		if r.status_code==200: return r
		else:
			raise
	
	def post(url, data):
		r = requests.get(url=url, data=data, auth=self.oauth)
		if r.status_code==200: return r
		else:
			raise
	
	def get_authorize_url(self):
		request_url = "https://api.twitter.com/oauth/request_token"
		authorize_url = "https://api.twitter.com/oauth/authorize"
		r = self.get(request_url)
		
		token = parse_qs(r.text)['oauth_token'][0]
		authorize_url += "?oauth_token=%s" % token
	
	def load_usrtl(self, since_id, count=200):
		''' Load User Timeline 
		response will contain one tweet at least( since_id ).
		'''
		url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
		url += "?trim_user=1"
		url += "&since_id=%s" % since_id  if since_id else ''
		url += "&max_id=%s" % max_id  if max_id else ''
		url += "&count=%s" % count  if count>0 else ''
		r = self.get(url)
	
	def tweet(self, status):
		''' Post Tweet
		'''
		url = "https://api.twitter.com/1.1/statuses/update.json"
		data = {'status':  status}
		r = self.post(url, data)
	
