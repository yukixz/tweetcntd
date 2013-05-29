from django.http import HttpResponse
from tweetcntd import config
from tweetcntd.views import Templates

def Redirect2HomePage():
    response = HttpResponse(status=302)
    response['Location'] = config.HOST
    response.content = Templates.HTML_REDIRECT.replace("{{url}}", config.HOST)
    return response

def Redirect2URL(url=''):
    if not url:
        return HttpResponse(status=500)
    response = HttpResponse(status=302)
    response['Location'] = url
    response.content = Templates.HTML_REDIRECT.replace("{{url}}", url)
    return response
