
from tweetcntd import config

def list(request):
	pass

urlpatterns = patterns('tweetcntd.views',
    url(r'^list/$', 'admin.list'),
)
