from django.db import models

class CTS_URN(models.Model):
	urnstring = models.CharField(max_length=100)
	def __unicode__(self):
		return self.urnstring
		
class CTS_provider(models.Model):
	name = models.CharField(max_length=100)
	url = models.URLField(True)
	added_by = models.CharField(max_length=100)
	def __unicode__(self):
		return "%s @ %s (added by %s)"%(self.name,self.url,self.added_by)