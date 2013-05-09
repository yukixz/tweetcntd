from django.http import HttpResponse
from tweetcntd.views import Templates

def main(request):
	return HttpResponse(Templates.HTML_HOME)
