from django.http import HttpResponse
from tweetcntd import config


#### 2xx
HTML200_HOME ='''\
<html><head><meta http-equiv="content-type" content="text/html;charset=utf-8">
<title>tweetcntd</title></head><body>
<h1>tweetcntd {{version}}</h1>
<p>Source code <a href="https://github.com/dazzyd/tweetcntd">here</a>.</p>
<p><i>统计时段：-0:30~23:30、推数 {{tweet_min}} 以下不发统计<br/></i></p>
</body></html>'''

HTML200_SUCCESS = '''\
<html><head><meta http-equiv="content-type" content="text/html;charset=utf-8">
<title>success</title></head><body>
<p>You have authorized this app.<br/>Your screen name: {{name}}</p>
</body></html>'''

def home():
    response = HttpResponse(status=200)
    response.content = HTML200_HOME\
        .replace("{{version}}", config.VERSION)\
        .replace("{{tweet_min}}", config.TWEET_MIN)
    return response

def auth_success(name):
    response = HttpResponse(status=200)
    response.content = HTML200_HOME\
        .replace("{{name}}", name)
    return response


#### 3xx
HTML302_REDIRECT = '''\
<html><head><meta http-equiv="content-type" content="text/html;charset=utf-8">
<title>302 Found</title></head><body>
<p><a href="{{url}}">Click here to continue.</a></p>
</body></html>'''

def redirect_to_home():
    response = HttpResponse(status=302)
    response['Location'] = config.HOST
    response.content = HTML302_REDIRECT.replace("{{url}}", config.HOST)
    return response

def redirect(url=''):
    if not url:
        return internal_server_error()
    response = HttpResponse(status=302)
    response['Location'] = url
    response.content = HTML302_REDIRECT.replace("{{url}}", url)
    return response


#### 5xx
HTML500_ERROR = '''\
<html><head><meta http-equiv="content-type" content="text/html;charset=utf-8">
<title>500 Internal Server Error</title></head><body>
<p>Something bad happened. (so sad...)</p>
</body></html>'''

def internal_server_error():
    response = HttpResponse(status=500)
    response.content = HTML500_ERROR
    return response
