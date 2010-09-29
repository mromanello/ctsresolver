from django.http import HttpResponse
import ctsresolver.cts.populate as p

def list_providers(request):
    return HttpResponse('<br/>'.join([s for s in p.list()]))