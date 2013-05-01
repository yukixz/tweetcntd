
from tweetcntd.models import config

def list(request):
	pass

def main(request, mode):
	if mode=='list':
		return auth(request)
