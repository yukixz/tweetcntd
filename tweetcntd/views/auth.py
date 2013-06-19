from django.conf.urls import patterns, url
from tweetcntd import config
from tweetcntd import templates
from tweetcntd.models.log import log
from tweetcntd.models.database import Database
from tweetcntd.models.twitter import *
from urllib.parse import urljoin

def authorize(request):
    if request.GET.get('key') != config.AUTH_KEY:
        return templates.redirect_to_home()
    
    client = TwitterClient(config.CONSUMER_KEY, config.CONSUMER_SECRET,
                callback_url=urljoin(config.HOST, '/auth/verify/') )
    try: url = client.get_authorize_url()
    except TwitterError as e:
        log.error('%d %d' % (e.http_status, e.error_code))
        return templates.internal_server_error()
    
    return templates.redirect(url)

def verify(request):
    auth_token = request.GET.get('oauth_token')
    auth_verifier = request.GET.get('oauth_verifier')
    
    if not auth_token or not auth_verifier:
        return templates.redirect_to_home()
    
    # Request Access Token & Secret
    client = TwitterClient(config.CONSUMER_KEY, config.CONSUMER_SECRET)
    try: user_id, screen_name, access_token, access_secret = client.get_access_token(auth_token, auth_verifier)
    except TwitterError as e:
        log.error('%d %d' % (e.http_status, e.error_code))
        return templates.internal_server_error()
    
    # Save to Database
    try:
        database = Database(config.DATABASE_HOST, config.DATABASE_PORT,
            config.DATABASE_DATABASE, config.DATABASE_TABLE, config.DATABASE_ISINNODB,
            config.DATABASE_USERNAME, config.DATABASE_PASSWORD)
        database.insert_user(user_id, screen_name, access_token, access_secret)
        database.close()
    except Exception as e:
        log.error(e)
        return templates.internal_server_error()
    
    # Show success page.
    return templates.auth_success(name)


urlpatterns = patterns('tweetcntd.views',
    url(r'^authorize/$', 'auth.authorize'),
    url(r'^verify/$', 'auth.verify'),
)
