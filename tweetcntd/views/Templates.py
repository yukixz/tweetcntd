from tweetcntd import config

'''
 Templates: HTML
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
.replace("{{version}}", config.VERSION)\
.replace("{{tweet_min}}", str(config.TWEET_MIN))

HTML_REDIRECT = '''\
<HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">
<TITLE>302 Found</TITLE></HEAD><BODY>
<A HREF="{{url}}">Click here to continue.</A>
</BODY></HTML>'''

'''
 Templates: SQL
'''

# CREATE
SQL_CREATE_TABLE = '''CREATE TABLE {{table}} \
(id BIGINT Unsigned NOT NULL, token CHAR(50) NOT NULL, secret CHAR(41) NOT NULL,\
 name CHAR(15),\
 t_sum INT Unsigned, t_re INT Unsigned, t_rt INT Unsigned, t_rto INT Unsigned,\
 t_last BIGINT Unsigned,\
 PRIMARY KEY (id) )'''\
.replace('{{table}}', config.DATABASE_TABLE)

# DELETE
SQL_DELETE_USER = '''DELETE FROM {{table}} WHERE id={{id}}'''\
.replace('{{table}}', config.DATABASE_TABLE)

# INSERT
SQL_INSERT_USER = '''INSERT INTO {{table}} \
(id, name, token, secret, t_sum, t_re, t_rt, t_rto, t_last) \
VALUES ({{id}}, "{{name}}", "{{token}}", "{{secret}}", 0, 0, 0, 0, 0)'''\
.replace('{{table}}', config.DATABASE_TABLE)

# QUERY
SQL_QUERY_ALL = '''SELECT * FROM {{table}}'''\
.replace('{{table}}', config.DATABASE_TABLE)

# UPDATE
SQL_UPDATE_COUNT = '''UPDATE {{table}} SET t_sum={{sum}}, t_re={{re}}, t_rt={{rt}}, t_rto={{rto}, t_last={{last}} WHERE id={{id}}'''\
.replace('{{table}}', config.DATABASE_TABLE)

SQL_UPDATE_NAME = '''UPDATE {{table}} SET name={{name}} WHERE id={{id}}'''\
.replace('{{table}}', config.DATABASE_TABLE)
