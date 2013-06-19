from tweetcntd import config

TWITTER_TWEET = "@{{name}} 本日共发 %d 推，其中 @ %d 推（%.1f%%）、RT @ %d 推（%.1f%%）、Retweet %d 推（%.1f%%）"
def tweet(name, sum, re, rt, rto):
    status = TWITTER_TWEET.replace('{{name}}', name)
    status = status % ( sum, re, float(re)/sum*100 , rt, float(rt)/sum*100, rto, float(rto)/sum*100 )
    return status