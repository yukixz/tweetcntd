

def pull(request):
	pass

def post(request):
	pass


def main(request, mode):
	if mode=='pull':
		return pull(request)
	elif mode=='post':
		return post(request)
