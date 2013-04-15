from ctsresolver.resolv.models import CTS_provider

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
	if(len(CTS_provider.objects.all())==0):
		populate()
	o = [str(o) for o in CTS_provider.objects.all()]
	return o

def main():
	return

if __name__ == "__main__":
    main()
		