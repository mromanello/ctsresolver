from ctsresolver.cts.models import CTS_provider

def populate():
	path = "/Users/56k/phd/code/ctsresolver/data/service_providers.dat"
	f = open(path,'r')
	for l in f.read().split('\n'):
		info = l.split('\t')
		if(len(info)==3):
			ws = CTS_provider(name=info[0],url=info[1],added_by=info[2])
			ws.save()
			print ws
			
def list():
	o = [str(o) for o in CTS_provider.objects.all()]
	return o
	
class TextInventoryHarvester():
	def __init__(self):
		return