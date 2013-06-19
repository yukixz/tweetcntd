from django.conf.urls import patterns, url
from tweetcntd import templates

def main(request):
    return templates.home()


urlpatterns = patterns('tweetcntd.views',
    url(r'^$', 'home.main'),
)
