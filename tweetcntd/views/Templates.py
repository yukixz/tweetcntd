from tweetcntd import config


VERSION = '0.2.1'

'''
 Template: HTML
'''

HTML_AUTH_SUCCESS = '''\
<HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">
<TITLE>Success</TITLE></HEAD><BODY>
<P>You have authorized this app. <br/>Your screen name: {{screen_name}}</P>
</BODY></HTML>'''

HTML_HOME ='''\
<html><head><meta http-equiv="content-type" content="text/html;charset=utf-8">
<title>tweetcntd</title></head><body>
<h2>tweetcntd ver {{version}}</h2>
<p>See source <a href="https://github.com/dazzyd/tweetcntd">here</a>.</p>
<p><i>统计时段：-0:30~23:30、推数 {{tweet_min}} 以下不发统计<br/></i></p>
</body></html>'''\
.replace("{{version}}", VERSION)\
.replace("{{tweet_min}}", str(config.TWEET_MIN))

HTML_REDIRECT = '''\
<HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">
<TITLE>302 Found</TITLE></HEAD><BODY>
<A HREF="{{url}}">Click here to continue.</A>
</BODY></HTML>'''


'''
 Template: TWITTER
'''
TWITTER_TWEET = "@{{name}} 本日共发 %d 推，其中 @ %d 推（%.1f%%）、RT @ %d 推（%.1f%%）、Retweet %d 推（%.1f%%）"
