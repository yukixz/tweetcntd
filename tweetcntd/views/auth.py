from django.conf.urls import patterns, url
from django.http import HttpResponse
from tweetcntd import config
from tweetcntd.models.database import Database
from tweetcntd.models.twitter import TwitterClient
from tweetcntd.models.twitter import TwitterUser
from tweetcntd.views import utils
from tweetcntd.views import Templates

def authorize(request):
	if request.GET.get('key') != config.AUTH_KEY:
		return utils.Redirect2HomePage()
	
	client = TwitterClient(config.CONSUMER_KEY, config.CONSUMER_SECRET,
				callback_url="%s/auth/verify/" % config.HOST)
	url = client.get_authorize_url()
	
	return utils.Redirect2URL(url)

def verify(request):
	auth_token = request.GET.get('oauth_token')
	auth_verifier = request.GET.get('oauth_verifier')
	
	if not auth_token or not auth_verifier:
		return utils.Redirect2HomePage()
	
	# Request Access Token & Secret
	client = TwitterClient(config.CONSUMER_KEY, config.CONSUMER_SECRET)
	user_id, screen_name, access_token, access_secret = client.get_access_token(auth_token, auth_verifier)
	
	# Save to Database
	database = Database(config.DATABASE_HOST, config.DATABASE_PORT,
		config.DATABASE_DATABASE, config.DATABASE_TABLE, config.DATABASE_ISINNODB,
		config.DATABASE_USERNAME, config.DATABASE_PASSWORD)
	database.insert_user(user_id, screen_name, access_token, access_secret)
	database.close()
	
	# Redirect to success page.
	url = "%s/auth/success/?name=%s" % (config.HOST, screen_name)
	return utils.Redirect2URL(url)

def success(request):
	name = request.GET.get('name')
	
	if not name:
		return utils.Redirect2HomePage()
	
	response = HttpResponse()
	response.content = Templates.HTML_AUTH_SUCCESS.replace("{{screen_name}}", name)
	return response


urlpatterns = patterns('tweetcntd.views',
    url(r'^authorize/$', 'auth.authorize'),
    url(r'^verify/$', 'auth.verify'),
    url(r'^success/$', 'auth.success'),
)
