# -*- coding: UTF-8 -*-

from xml.etree import ElementTree
from xml.etree.ElementTree import XML
from xml.parsers.expat import ExpatError
import urllib2,re,logging

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - [%(levelname)s] %(message)s',datefmt='%a, %d %b %Y %H:%M:%S')
logger = logging.getLogger('CTS')

def normalize(inp_string):
	"""docstring for normalize"""
	return re.sub(r'\s\s+',"",inp_string)

class CTS_URN():
	"""Object representing a CTS URN"""
	def __init__(self, urn_sring):
		self.urn = urn_sring
		
	def __str__(self):
			return self.urn
	

class TextInventory():
	"""
	A class representing a CTS TextInventory
	"""
	global _get_capab_req,_cts_ns,_xml_ns
	_get_capab_req = "CTS?request=GetCapabilities"
	_cts_ns = "{http://chs.harvard.edu/xmlns/cts3/ti}"
	_xml_ns="{http://www.w3.org/XML/1998/namespace}"
	def __init__(self):
		## the TI version
		self.version = None
		self.content = []
		## the TextGroups contained in the TI
		self.textgroups = {}
		self.works = {}
		self.editions={}
		return
			
	def set_version(self,v):
		self.version = v
		
	def get_version(self):
		return self.version

	## Function add
	# @param self
	# @param type the type of object being added to the TI
	# @param obj the object to be added
	def add(self,type,obj):
		"""
		bla bla	
		"""
		if(type=="tg"):
			self.textgroups[obj.id]=obj
		elif(type=="wk"):
			self.works[obj.id]=obj
			logger.debug("The work %s/%s was added to the TI"%(obj.title,obj.urn()))
		elif(type=="ed"):
			self.editions[obj.id]=obj
			logger.debug("The edition %s (for Work %s) was added to the TI"%(obj.id,obj.work))
		return
	
	def count(self,type):
		if(type=="tg"):
			return len(self.textgroups)
		elif(type=="wk"):
			return len(self.works)
		elif(type=="ed"):
			return len(self.editions)
	
	def textgroups(self):
		return self.content
	

class TextGroup():
	def __init__(self,id=None,name="",works={}):
		self.id = id
		self.names = {}
		self.works = works
		self.xml = ""
		return
	
	def get_name(self, lang=None):
		return self.names[lang]
	
	def set_id(self,id):
		self.id = id
	
	def set_name(self,lang,name):
		self.names[lang]=name
	
	def add(self,w):
		self.works[w.id]=w
	
	def load_from_XML(self):
		# TODO implement
		pass
	
class Collection():
	pass
	
class Work():
	def __init__(self,id="",lang="",title="",tg=""):
		self.textgroup=tg
		self.id=id
		self.lang=lang
		self.title=title
		self.editions=[]
		
	def set_title(self, title):
		self.title = normalize(title)	
	
	def add_edition(ed):
		self.editions.append(ed)
		
	def get_id(self, remove_prefix=True):
		if(remove_prefix):
			return re.sub(r'.*?:',"",self.id)
		else:
			return self.id
	# Get the CTS URN for this Work
	# @return the URN
	def urn(self, urn_ns="urn:cts"):
		return CTS_URN("%s:%s.%s"%(urn_ns,self.textgroup,self.get_id()))

class Edition():
	def __init__(self,id="",label="",work=""):
		self.id=id
		self.desc = {}
		self.label=""
		self.doc = None
		self.work = work
		
	def add_desc(self,lang,desc):
		self.desc[lang]=normalize(desc)
		logger.debug("Added description \"%s\""%self.desc[lang])
		
	def get_desc(self,lang):
		return self.desc[lang]
		
class Resource():
	class Citation():
		def __init__(label="",scope="",xpath=""):
			self.label=label
			self.scope=scope
			self.xpath=xpath
		
	def __init__(self,docname=""):
		self.docname = docname
		self.citation_mapping = []
	
	def add_citation(self,cit):
		self.citation_mapping.append(cit)
		
	def get_citation_levels(self):
		return len(self.citation_mapping)
		
class TextInventoryHarvester():
	def __init__(self):
		return
		
	def parse(self,url):
		ti = TextInventory()
		logger.info("Parsing CTS service @ %s"%url)
		try:
			# TODO: separate this line in order to raise separate errors!
			xml_ti = XML(urllib2.urlopen(url+_get_capab_req).read())
					
			# retrieve and store the TI version
			for node in xml_ti.findall('.//%sTextInventory'%_cts_ns):
				ti.set_version(node.attrib.get('tiversion'))
				logger.info("TextInventory version: %s"%ti.get_version())
			# retrieve and store the textgroups
			for node in xml_ti.findall('.//%stextgroup'%_cts_ns):
				tg = TextGroup(id=node.attrib.get('projid'))
				tg.xml = ElementTree.tostring(node)
				ti.add('tg',tg)
				
				# retrieve and store the works
				for child in node:
					# parse groupname elem
					if(child.tag=="%s%s"%(_cts_ns,"groupname")):
						tg.set_name(child.attrib.get("%slang"%_xml_ns),re.sub(r'\s\s+',"",child.text))
						logger.debug("Found TextGroup: \"%s\""%tg.get_name(child.attrib.get("%slang"%_xml_ns)))
					#parse work elem
					elif(child.tag=="%s%s"%(_cts_ns,"work")):
						w = Work(id=child.attrib.get('projid'),tg=tg.id)
						for title in child.findall('.//%stitle'%_cts_ns):
							w.set_title(title.text)
						ti.add('wk',w)
						logger.debug("Found Work: %s"%w.id)
						# parse edition elem
						for node in child.findall('.//%sedition'%_cts_ns):
							e = Edition(id=node.attrib.get('projid'),work=w.id)
							for child in node:
								if(child.tag=="%s%s"%(_cts_ns,"label")):
									e.label=child.text
								elif(child.tag=="%s%s"%(_cts_ns,"description")):
									lang=child.attrib.get("%slang"%_xml_ns)
									desc=child.text
									e.add_desc(lang,desc)
								elif(child.tag=="%s%s"%(_cts_ns,"online")):
									pass
									# 
							ti.add('ed',e)
								
		except ExpatError as error:
			logger.error("Parsing of %s failed with error \"%s\""%(url,str(error)))
			
		return ti

def dumb_test():
	parsed = xml.XML('''
	<root>
	  <group>
		<child id="a">This is child "a".</child>
		<child id="b">This is child "b".</child>
	  </group>
	  <group>
		<child id="c">This is child "c".</child>
	  </group>
	</root>
	''')
	for node in parsed.findall('.//child'):
		print "%s has id %s"%(node,node.attrib.get('id'))

def main():
	#dumb_test()
	tih = TextInventoryHarvester()
	path = "/Users/56k/phd/code/ctsresolver/data/service_providers.dat"
	f = open(path,'r')
	count = 0
	stop_at = 2
	for l in f.read().split('\n'):
		if(count<stop_at):
			info = l.split('\t')
			if(len(info)==3):
				ti = tih.parse(info[1])
				#print ti.count('tg')
				#print ti.count('wk')
				#print ti.count('ed')
				count+=1
	
	return

if __name__ == "__main__":
    main()