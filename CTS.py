# -*- coding: UTF-8 -*-

from xml.etree import ElementTree
from xml.etree.ElementTree import XML
from xml.parsers.expat import ExpatError
import urllib,re,logging

_get_capab_req = "CTS?request=GetCapabilities"
_cts_ns = "{http://chs.harvard.edu/xmlns/cts3/ti}"

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - [%(levelname)s] %(message)s',datefmt='%a, %d %b %Y %H:%M:%S')
logger = logging.getLogger('CTS')

class TextInventory():
	def __init__(self):
		self.version = None
		self.content = []
		return
	
	def set_version(self,v):
		self.version = v
		
	def get_version(self):
		return self.version
		
	def textgroups(self):
		return self.content
	
class TextGroup():
	def __init__(self,id=None,name="",works={}):
		self.id = id
		self.name = name
		self.works = works
		self.xml = ""
		return
		
	def set_id(self,id):
		self.id = id
		
	def set_name(self,name):
		self.name = name
		
	def add(self,w):
		self.works[w.id]=w
		
class Work():
	def __init__(self,id="",lang=""):
		self.id=id
		self.lang=lang

class TextInventoryHarvester():
	def __init__(self):
		return
		
	def parse(self,url):
		ti = TextInventory()
		logger.info("Parsing CTS @ %s"%url)
		try:
			xml_ti = XML(urllib.urlopen(url+_get_capab_req).read())
					
			# retrieve and store the TI version
			for node in xml_ti.findall('.//%sTextInventory'%_cts_ns):
				ti.set_version(node.attrib.get('tiversion'))
				logger.info("TextInventory version: %s"%ti.get_version())
			# retrieve and store the textgroups
			for node in xml_ti.findall('.//%stextgroup'%_cts_ns):
				tg = TextGroup(id=node.attrib.get('projid'))
				tg.xml = ElementTree.tostring(node)
				ti.content.append(tg)
				
				# retrieve and store the works
				for child in node:
					if(child.tag=="%s%s"%(_cts_ns,"groupname")):
						tg.set_name(re.sub(r'\s\s+',"",child.text))
						logger.info("Found TextGroup: \"%s\""%tg.name)
					elif(child.tag=="%s%s"%(_cts_ns,"work")):
						w = Work(child.attrib.get('projid'))
						tg.add(w)
						logger.info("Found Work: %s"%w.id)
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
	for l in f.read().split('\n'):
		info = l.split('\t')
		if(len(info)==3):
			ti = tih.parse(info[1])
	
	return

if __name__ == "__main__":
    main()