#!/usr/bin/env python3
import sys
sys.path.append(sys.argv[1])

from datetime import datetime, timedelta
import re
from tweetcntd import config
from tweetcntd.models.database import Database
from tweetcntd.models.twitter import TwitterClient
from tweetcntd.models.twitter import TwitterUser
from tweetcntd.views import Templates

def post():
	database = Database(config.DATABASE_HOST, config.DATABASE_PORT,
		config.DATABASE_DATABASE, config.DATABASE_TABLE, config.DATABASE_ISINNODB,
		config.DATABASE_USERNAME, config.DATABASE_PASSWORD)
	client = TwitterClient(config.CONSUMER_KEY, config.CONSUMER_SECRET)
	
	start_time, end_time = get_time()
	li = database.query_all()
	for user in li:
		oauth_user = TwitterUser(user.token, user.secret)
		(sum, re, rt, rto) = count_user(client, oauth_user, start_time, end_time)
		if sum>config.TWEET_MIN and sum>0:
			status = Templates.TWITTER_TWEET.replace('{{name}}', user.name) % \
				( sum, re, float(re)/sum*100 , rt, float(rt)/sum*100, rto, float(rto)/sum*100 )
			client.tweet(oauth_user, status)
	
	database.close()

def count_user(client, user, start_time, end_time,
		PATTERN_RE=re.compile(r'^(@\w+)\b.*$'), PATTERN_RT=re.compile(r'^.*?(RT ?@\w+)\b.*$')):
	# init
	max_id = 0
	timeline = []
	block = [{"created_at":"Tue Feb 14 00:00:00 +0000 9999"}]	## Magic
	
	# Generate user's new tweets' blocks
	while format_time(block[len(block)-1]["created_at"]) > start_time:
		block = client.load_usrtl(user, max_id)
		timeline.extend(block)
		max_id = block[len(block)-1]["id"]
	
	# Count user's tweets
	(sum, re, rt, rto) = (0,0,0,0)
	for tweet in timeline:
		tweet_time = format_time(tweet["created_at"])
		if tweet_time > end_time:
			continue
		elif tweet_time > start_time:
			sum +=1
			if 'retweeted_status' in tweet:
				rto += 1
			elif PATTERN_RE.match(tweet["text"]):
				re += 1
			elif PATTERN_RT.match(tweet["text"]):
				rt +=1
		else:
			break # for
	
	# return
	return sum, re, rt, rto

def format_time(ss, MONTH2NUMBER={'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',
		'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}):
	return ''.join(( ss[26:30],MONTH2NUMBER[ss[4:7]],ss[8:10],ss[11:13],ss[14:16],ss[17:19] ))

def get_time():
	''' Returns formatted start_time and end_time. '''
	delta = timedelta(hours=config.TIMEZONE)
	now_tz = datetime.utcnow() + delta
	post_str = now_tz.strftime('%Y-%m-%d ') + config.POST_TIME
	post_utc = datetime.strptime(post_str, '%Y-%m-%d %H:%M') - delta
	end = post_utc.strftime("%Y%m%d%H%M%S")
	start = (post_utc-timedelta(hours=24)).strftime("%Y%m%d%H%M%S")
	return start, end

if __name__ == '__main__':
	post()