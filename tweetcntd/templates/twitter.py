#from tweetcntd import config

TWITTER_TWEET = "%s 本日共发 %d 推，其中回复 %d (%.1f%%)、引用 %d (%.1f%%)、转发 %d (%.1f%%)，最多提及 %s 。"
def tweet(name, sum, re, rt, rto, most_mentions):
    name = '@'+name
    if most_mentions: mentions = '@' + ', @'.join(most_mentions)
    else: mentions = '0x0'
    return TWITTER_TWEET % (
        name, 
        sum,  re, float(re)/sum*100 , rt, float(rt)/sum*100, rto, float(rto)/sum*100,
        mentions
        )
