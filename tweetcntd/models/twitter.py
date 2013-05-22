from cgi import parse_qs
from tweetcntd.models.oauth import OAuthClient

class TwitterUser():
	def __init__(self, token, secret):
		self.access_token = token
		self.access_secret = secret
	

class TwitterClient():
	def __init__(self, consumer_key, consumer_secret, callback_url=''):
		self.client = OAuthClient(
			consumer_key = consumer_key,
			consumer_secret = consumer_secret,
			callback_url = callback_url
		)
	
	
	def get_authorize_url(self):
		request_url = "https://api.twitter.com/oauth/request_token"
		authorize_url = "https://api.twitter.com/oauth/authorize"
		r = self.client.get(request_url)
		
		token = parse_qs(r.text)['oauth_token'][0]
		authorize_url += "?oauth_token=%s" % token
		return authorize_url
	
	def get_access_token(self, token, verifier):
		access_url = "https://api.twitter.com/oauth/access_token"
		params = {'oauth_verifier': verifier}
		r = self.client.post(access_url, params, token=token)
		
		result = parse_qs(r.text)
		return int(result["user_id"][0]), result["screen_name"][0], result["oauth_token"][0], result["oauth_token_secret"][0]
	
	
	def load_usrtl(self, user, max_id=0, count=200):
		''' Load User Timeline
		return a loaded json object.
		'''
		url = "https://api.twitter.com/1.1/statuses/user_timeline.json?trim_user=1"
		# url += '&since_id=%s' % since_id  if since_id else ''
		url += '&max_id=%d' % max_id  if max_id>0 else ''
		url += '&count=%d' % count  if count>0 else ''
		r = self.client.get(url,
					user.access_token, user.access_secret)
		return r.json()
	
	def tweet(self, user, status):
		''' Post Tweet
		'''
		url = "https://api.twitter.com/1.1/statuses/update.json"
		params = {'status':  status}
		r = self.client.post(url, params,
					user.access_token, user.access_secret)
	
