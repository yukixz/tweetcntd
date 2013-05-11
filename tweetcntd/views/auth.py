from django.conf.urls import patterns, url
from django.http import HttpResponse
from tweetcntd import config
from tweetcntd.models.database import Database
from tweetcntd.models.twitter import TwitterClient
from tweetcntd.views import Templates

def authorize(request):
	client = TwitterClient()
	oauth = TwitterClient.OAuth(config.CONSUMER_KEY, config.CONSUMER_SECRET,
			callback_url="%s/auth/verify" % config.HOST)
	url = client.get_authorize_url(oauth)
	
	response = HttpResponse()
	response.status_code = 302
	response['Location'] = url
	response.content = Templates.HTML_REDIRECT.replace("{{url}}", url)
	return response

def verify(request):
	auth_token = request.GET["oauth_token"]
	auth_verifier = request.GET["oauth_verifier"]
	
	# Request Access Token & Secret
	client = TwitterClient()
	oauth = TwitterClient.OAuth(config.CONSUMER_KEY, config.CONSUMER_SECRET,)
	user_id, screen_name, access_token, access_secret = client.get_access_token(oauth, auth_token, auth_verifier)
	
	# Save to Database
	database = Database(config.DATABASE_HOST, config.DATABASE_PORT,
		config.DATABASE_DATABASE, config.DATABASE_TABLE, config.DATABASE_ISINNODB,
		config.DATABASE_USERNAME, config.DATABASE_PASSWORD)
	database.insert_user(user_id, screen_name, access_token, access_secret)
	database.close()
	
	# Redirect to success page.
	url = "%s/auth/success?name=%s" % (config.HOST, screen_name)
	response = HttpResponse()
	response.status_code = 302
	response['Location'] = url
	response.content = Templates.HTML_REDIRECT.replace("{{url}}", url)
	return response

def success(request):
	response = HttpResponse()
	response.content = Templates.HTML_AUTH_SUCCESS.replace("{{screen_name}}", request.GET['name'])
	return response


urlpatterns = patterns('tweetcntd.views',
    url(r'^authorize/$', 'auth.authorize'),
    url(r'^verify/$', 'auth.verify'),
    url(r'^success/$', 'auth.success'),
)
