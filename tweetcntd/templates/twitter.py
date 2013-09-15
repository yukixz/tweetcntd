#from tweetcntd import config
from random import choice

TWITTER_TWEET = \
"%s 本日共发 %d 推，其中回复 %d (%.1f%%)、引用 %d (%.1f%%)、转发 %d (%.1f%%)，\
最多提及 %s。"
EMOTIONS = [
'0x0', '0v0', '0w0', '=x=', '=w=', '=3=', 'Orz',
'(￣o￣)', '(￣3￣)', '(￣﹏￣)', '(=￣ω￣=)', '(┬＿┬)'
'm( _　_ )m', '(＞﹏＜)', '(⊙ˍ⊙)',
]
def tweet(name, sum, re, rt, rto, most_mentions):
    name = '@'+name
    if most_mentions:
        mentions = '@' + ', @'.join(most_mentions)
    else:
        mentions = choice(EMOTIONS)
    return TWITTER_TWEET % (
        name, 
        sum, 
        re, float(re)/sum*100, 
        rt, float(rt)/sum*100, rto, 
        float(rto)/sum*100,
        mentions
        )
