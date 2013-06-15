#!/usr/bin/env python3
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from datetime import datetime, timedelta
import re
from tweetcntd import config
from tweetcntd.models.database import Database
from tweetcntd.models.twitter import TwitterClient, TwitterError, TwitterUser
from tweetcntd.views import Templates

class Post():
    def __init__(self):
        self.database = Database(config.DATABASE_HOST, config.DATABASE_PORT,
            config.DATABASE_DATABASE, config.DATABASE_TABLE, config.DATABASE_ISINNODB,
            config.DATABASE_USERNAME, config.DATABASE_PASSWORD)
        self.client = TwitterClient(config.CONSUMER_KEY, config.CONSUMER_SECRET)
        
        self.PATTERN_RE=re.compile(r'^(@\w+)\b.*$')
        self.PATTERN_RT=re.compile(r'^.*?(RT ?@\w+)\b.*$')
        self.MONTH2NUMBER={'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
        
        ''' Init formatted start_time and end_time. '''
        delta = timedelta(hours=config.TIMEZONE)
        now_tz = datetime.utcnow() + delta
        post_str = now_tz.strftime('%Y-%m-%d ') + config.POST_TIME
        post_utc = datetime.strptime(post_str, '%Y-%m-%d %H:%M') - delta
        self.end_time = post_utc.strftime("%Y%m%d%H%M%S")
        self.start_time = (post_utc-timedelta(hours=24)).strftime("%Y%m%d%H%M%S")
        
    def run(self):
        li = self.database.query_all()
        for user in li:
            if not user.enabled: continue
            try:
                oauth_user = TwitterUser(user.token, user.secret)
                (sum, re, rt, rto) = self.count_user(oauth_user)
                
                if sum>config.TWEET_MIN and sum>0:
                    status = Templates.TWITTER_TWEET.replace('{{name}}', user.name) % \
                        ( sum, re, float(re)/sum*100 , rt, float(rt)/sum*100, rto, float(rto)/sum*100 )
                    self.client.tweet(oauth_user, status)
                
            except TwitterError as e:
                if e.code==1: continue
                if e.code==2: break
                if e.code==3: self.database.disable_user(user.id)
                if e.code==4: continue  # How to Retry?
                if e.code==5: break
    
    def count_user(self, user):
        # init
        max_id = 0
        timeline = []
        block = [{"created_at":"Tue Feb 14 00:00:00 +0000 9999"}]    ## Magic
        
        # Generate user's new tweets' blocks
        while self.format_time(block[len(block)-1]["created_at"]) > self.start_time:
            block = self.client.load_usrtl(user, max_id)
            timeline.extend(block)
            max_id = block[len(block)-1]["id"]
        
        # Count user's tweets
        (sum, re, rt, rto) = (0,0,0,0)
        for tweet in timeline:
            tweet_time = self.format_time(tweet["created_at"])
            if tweet_time > self.end_time:
                continue
            elif tweet_time > self.start_time:
                sum +=1
                if tweet.get('retweeted_status', False):
                    rto += 1
                elif self.PATTERN_RE.match(tweet["text"]):
                    re += 1
                elif self.PATTERN_RT.match(tweet["text"]):
                    rt +=1
            else:
                break # for
        
        return sum, re, rt, rto
    
    def format_time(self, ss):
        return ''.join(( ss[26:30], self.MONTH2NUMBER[ss[4:7]],ss[8:10],ss[11:13],ss[14:16],ss[17:19] ))
        
    def close(self):
        self.database.close()

if __name__ == '__main__':
    app = Post()
    app.run()
    app.close()
