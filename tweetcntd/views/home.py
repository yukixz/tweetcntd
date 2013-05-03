from django.http import HttpResponse
from tweetcntd import config

HOME = '''
<html>
	<head><title>tweetcntd</title></head>
	<body>
		<h2>tweetcntd #VERSION#</h2>
		<p>Non-Public, but <a href="https://github.com/dazzyd/tweetcntd">Open Source</a>.</p>
		<p><i>统计时段：-0:30~23:30、推数 #TWEET_MIN# 以下不发统计<br/></i></p>
	</body>
</html>
'''\
.replace("#VERSION#", config.VERSION)\
.replace("#TWEET_MIN#", str(config.TWEET_MIN))

def main(request):
	return HttpResponse(HOME)
