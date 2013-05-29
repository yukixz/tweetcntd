from django.conf.urls import patterns, url
from django.http import HttpResponse
from tweetcntd.views import Templates

def main(request):
    return HttpResponse(Templates.HTML_HOME)


urlpatterns = patterns('tweetcntd.views',
    url(r'^$', 'home.main'),
)
