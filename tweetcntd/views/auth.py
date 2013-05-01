

def auth(request):
	pass

def verify(request):
	pass

def success(request):
	pass


def main(request, mode):
	if mode=='auth':
		return auth(request)
	elif mode=='verify':
		return verify(request)
	elif mode=='success':
		return success(request)
