'''
 Templates
'''

REDIRECT = '''\
<HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">
<TITLE>302 Found</TITLE></HEAD><BODY>
<A HREF="{{url}}">Click here to continue.</A>
</BODY></HTML>
'''

AUTH_SUCCESS = '''\
<HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">
<TITLE>Success</TITLE></HEAD><BODY>
<P>You have authorize this app. <br/>Your screen name: {{screen_name}}</P>
</BODY></HTML>
'''