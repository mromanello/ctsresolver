from django.http import HttpResponse
import ctsresolver.populate as p

def list_providers(request):
	"""
	List all of the CTS providers being harvested by the ctsresolver
	"""
	return HttpResponse('<br/>'.join([s for s in p.list()]))