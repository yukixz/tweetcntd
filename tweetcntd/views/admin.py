from django.conf.urls import patterns, url
from tweetcntd import config

def list(request):
	pass


if config.ADMIN_ENABLED:
	urlpatterns = patterns('tweetcntd.views',
	url(r'^list/$', 'admin.list'),
)
