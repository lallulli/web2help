###############################################################
# Name:			 MyTestBed.py
# Purpose:	 Testbed for Python extracting functions
# Author:		 Luca Allulli (luca@skeed.it)
# Created:	 2009-08-24
# Copyright: Luca Allulli (http://www.skeed.it/songpress.html)
# License:	 GNU GPL v2
##############################################################

from TestBed import *
import wx.lib.delayedresult as delayedresult
import urllib2
import BeautifulSoup

class MyTestBed(TestBed):
	def __init__(self, parent, project):
		TestBed.__init__(self, parent)
		self.project = project
		self.ec = project.extractContent
		self.et = project.extractTitle
		self.code.SetText(self.et)
		self.modeTitle = True
		
	def UpdateAll(self):
		if self.modeTitle:
			self.et = self.code.GetText()
		else:
			self.ec = self.code.GetText()
		
	def Consume(self, dr):
		try:
			result = dr.get()
			self.html.SetText(result)
		except Exception, exc:
			self.html.SetText("ERROR:\n" + str(exc))
			
	def Load(self):
		u = self.url.GetValue()
		if u[:4] != 'http':
			u = 'http://' + u
		s = urllib2.urlopen(u)
		raw = s.read()
		s.close()
		soup = BeautifulSoup.BeautifulSoup(raw)
		return soup
			
	def ProduceLoad(self):
		return self.Load().prettify()
		
	def ProduceParse(self):
		# define extracting methods
		m = "def extract(html):\n"
		for l in self.code.GetText().splitlines():
			m += "\t" + l + "\n"
		exec m
		# load web page
		soup = self.Load()
		s = extract(soup)
		return str(s)	
		
	def OnLoad(self, evt):
		delayedresult.startWorker(self.Consume, self.ProduceLoad)
		evt.Skip()
		
	def OnParse(self, evt):
		delayedresult.startWorker(self.Consume, self.ProduceParse)
		evt.Skip()
		
	def OnTitle(self, evt):
		self.UpdateAll()
		self.code.SetText(self.et)
		self.modeTitle = True
		evt.Skip()

	def OnContent(self, evt):
		self.UpdateAll()
		self.code.SetText(self.ec)
		self.modeTitle = False
		evt.Skip()
		
