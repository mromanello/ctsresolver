from django.http import HttpResponse
import ctsresolver.populate as p
from ctsresolver.CTS import *
import urllib2

def list_providers(request):
	"""
	List all of the CTS providers being harvested by the ctsresolver
	"""
	return HttpResponse('<br/>'.join([s for s in p.list()]))
	
def ping(request,url):
	"""
	Ping a CTS repository: ideally it would output some info about the repository.
	And in some way it does so
	"""
	tih = TextInventoryHarvester()
	# check if it does have a trailing slash or not
	ti=tih.parse("http://%s/"%url)
	return HttpResponse(ti.count('wk'))