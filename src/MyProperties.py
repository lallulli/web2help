###############################################################
# Name:			 MyProperties.py
# Purpose:	 Project properties dialog
# Author:		 Luca Allulli (luca@skeed.it)
# Created:	 2009-08-24
# Copyright: Luca Allulli (http://www.skeed.it/songpress.html)
# License:	 GNU GPL v2
##############################################################

from Properties import *
from Project import *

class MyProperties(Properties):
	def __init__(self, parent, project):
		Properties.__init__(self, parent)
		
		self.project = project
		self.template.SetPath(project.template)
		self.title.SetText(project.extractTitle)
		self.content.SetText(project.extractContent)
		self.name.SetPath(project.name)	
	
	def OnOk(self, evt):
		p = self.project
		p.template = self.template.GetPath()
		p.extractTitle = self.title.GetText()
		p.extractContent = self.content.GetText()
		p.name = self.name.GetPath()
		evt.Skip()
		