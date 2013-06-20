from urllib.parse import parse_qs
from tweetcntd.models.oauth import OAuthClient

class TwitterUser():
    def __init__(self, token, secret):
        self.access_token = token
        self.access_secret = secret
    

ERROR_MESSAGE = {
    0: 'Anything is OK.',
    1: 'Skip the User.',
    2: 'Skip the Rest User.',
    3: 'Disable the User.',
    4: 'Retry.',
    5: 'Critical!',
}
class TwitterError(Exception):
    def __init__(self, code=0, http_status=None, error_code=None):
        self.code = code
        self.message = ERROR_MESSAGE.get(code, 'Invalid Error Code.')
        self.http_status = http_status
        self.error_code = error_code
    

class TwitterClient():
    def __init__(self, consumer_key, consumer_secret, callback_url=''):
        self.client = OAuthClient(
            consumer_key = consumer_key,
            consumer_secret = consumer_secret,
            callback_url = callback_url
        )
    
    
    def request(self, method, url, params, token, secret):
        r = self.client.request(method, url, params, token, secret)
        
        status_code = r.status_code
        try:    error_code = r.json()['errors'][0]['code']
        except: error_code = 0
        
        # https://dev.twitter.com/docs/error-codes-responses
        if status_code==200:    # 200 OK
            return r
        if status_code==304:    # 304 Not Modified
            return r
        if status_code==400:    # 400 Bad Requests
            pass # Below
        if status_code==401:    # 401 Unauthorized
            pass # Below
        if status_code==403:    # 403 Forbidden
            pass # Below
        if status_code==404:    # 404 Not Found
            pass # Below
        if status_code==406:    # 406 Not Acceptable
            pass
        if status_code==408:    #### 408 Request Timeout
            raise TwitterError(4, status_code,error_code)
        if status_code==410:    # 410 Gone
            pass
        if status_code==422:    # 422 Unprocessable Entity
            pass
        if status_code==429:    # 429 Too Many Requests
            raise TwitterError(1, status_code,error_code)
        if status_code==500:    # 500 Internal Server Error
            raise TwitterError(2, status_code,error_code)
        if status_code==502:    # 502 Bad Gateway
            raise TwitterError(2, status_code,error_code)
        if status_code==503:    # 503 Service Unavailable
            raise TwitterError(2, status_code,error_code)
        if status_code==504:    # 504 Gateway timeout
            raise TwitterError(2, status_code,error_code)
        
        ## Error Code corresponded with HTTP Status Code above are ignored.
        if error_code==32:  # 32 Could not authenticate you
            raise TwitterError(3, status_code,error_code)
        if error_code==34:  # 34 Sorry, that page does not exist
            raise TwitterError(3, status_code,error_code)
        if error_code==64:  # 64 Your account is suspended and is not permitted to access this feature
            raise TwitterError(3, status_code,error_code)
        #if error_code==88: # 88 Rate limit exceeded
        if error_code==89:  # 89 Invalid or expired token
            raise TwitterError(3, status_code,error_code)
        #if error_code==130:# 130 Over capacity
        #if error_code==131:# 131 Internal error
        if error_code==135: # 135 Could not authenticate you
            raise TwitterError(1, status_code,error_code)
        if error_code==187: # 187 Status is a duplicate
            raise TwitterError(1, status_code,error_code)
        if error_code==215: # 215 Bad authentication data
            raise TwitterError(2, status_code,error_code)
        
        raise TwitterError(-1, status_code,error_code)
    
    def get (self, url, params={}, token='', secret=''):
        return self.request('GET', url, params, token, secret)
    
    def post(self, url, params={}, token='', secret=''):
        return self.request('POST', url, params, token, secret)
    
    
    def get_authorize_url(self):
        request_url = "https://api.twitter.com/oauth/request_token"
        authorize_url = "https://api.twitter.com/oauth/authorize"
        r = self.post(request_url)
        
        token = parse_qs(r.text)['oauth_token'][0]
        authorize_url += "?oauth_token=%s" % token
        return authorize_url
    
    def get_access_token(self, token, verifier):
        access_url = "https://api.twitter.com/oauth/access_token"
        params = {'oauth_verifier': verifier}
        r = self.post(access_url, params=params, token=token)
        
        result = parse_qs(r.text)
        return int(result["user_id"][0]), result["screen_name"][0], result["oauth_token"][0], result["oauth_token_secret"][0]
    
    
    def load_usrtl(self, user, max_id=0, count=100):
        url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
        params = {'trim_user':1}
        # if since_id: params['since_id'] = since_id
        if max_id>0: params['max_id'] = max_id
        if count>0: params['count'] = count
        r = self.get(url, params=params,
                    token=user.access_token, secret=user.access_secret)
        return r.json()
    
    def tweet(self, user, status):
        url = "https://api.twitter.com/1.1/statuses/update.json"
        params = {'status':  status}
        r = self.post(url, params,
                    token=user.access_token, secret=user.access_secret)
        # return r.json()
    
