from django.http import HttpResponse
from tweetcntd import config
from tweetcntd.views import Templates
from tweetcntd.models.twitter import TwitterClient

def authorize(request):
	client = TwitterClient()
	oauth = TwitterClient.OAuth(config.CONSUMER_KEY, config.CONSUMER_SECRET,
			callback_url="%s/auth/verify" % config.HOST)
	url = client.get_authorize_url(oauth)
	
	response = HttpResponse()
	response.status_code = 302
	response['Location'] = url
	response.content = Templates.REDIRECT.replace("{{url}}", url)
	return response

def verify(request):
	auth_token = request.GET["oauth_token"]
	auth_verifier = request.GET["oauth_verifier"]
	
	client = TwitterClient()
	oauth = TwitterClient.OAuth(config.CONSUMER_KEY, config.CONSUMER_SECRET,)
	user_id, screen_name, access_token, access_secret = client.get_access_token(oauth, auth_token, auth_verifier)
	
	# Save to database
	
	url = "%s/auth/success?name=%s" % (config.HOST, screen_name)
	response = HttpResponse()
	response.status_code = 302
	response['Location'] = url
	response.content = Templates.REDIRECT.replace("{{url}}", url)
	return response

def success(request):
	response = HttpResponse()
	response.content = Templates.AUTH_SUCCESS.replace("{{screen_name}}", request.GET['name'])
	return response


def main(request, mode):
	if mode=='authorize':
		return authorize(request)
	elif mode=='verify':
		return verify(request)
	elif mode=='success':
		return success(request)
