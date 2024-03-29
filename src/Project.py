###############################################################
# Name:			 Project.py
# Purpose:	 Project properties
# Author:		 Luca Allulli (luca@skeed.it)
# Created:	 2009-08-24
# Copyright: Luca Allulli (http://www.skeed.it/songpress.html)
# License:	 GNU GPL v2
##############################################################

from Globals import *
import xml.etree.ElementTree as ET


class Project(object):
	def __init__(self):
		object.__init__(self)
		self.template = glb.AddPath('template/template.html')
		self.name = ""
		self.extractTitle = """return html.h1.string"""
		self.extractContent = """return html.find('div', {'id': 'main'})"""
		self.grabJavascript = False

	def Serialize(self):
		e = ET.Element('project')
		template = ET.SubElement(e, 'template')
		template.text = self.template
		name = ET.SubElement(e, 'name')
		name.text = self.name
		extractTitle = ET.SubElement(e, 'extractTitle')
		extractTitle.text = self.extractTitle
		extractContent = ET.SubElement(e, 'extractContent')
		extractContent.text = self.extractContent
		#grabJavascript = ET.SubElement(e, 'grabJavascript')
		#grabJavascript.text = str(self.grabJavascript)
		return e
			
	def Unserialize(self, e):
		e = e.find('project')
		
		def get(name):
			n = e.find(name)
			if n is None:
				return ""
			else:
				v = n.text
				return "" if v is None else v 
	
		self.template = get('template')
		self.name = get('name')
		self.extractTitle = get('extractTitle')
		self.extractContent = get('extractContent')
		#self.grabJavascript = True #bool(get('grabJavascript'))
