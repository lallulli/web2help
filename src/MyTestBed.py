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
		self.SetStyling()
		
	def SetStyling(self):
		#############################################
		# Styling code from etelos-opendev          #
		# http://code.google.com/p/etelos-opendev/  #
		#############################################
		self.html.SetStyleBits( 7 )
		self.html.StyleSetSpec( stc.STC_STYLE_DEFAULT, "size:9,face:Lucida Console")
		self.html.SetEOLMode( stc.STC_EOL_LF )
		self.html.SetLexer( stc.STC_LEX_HTML )
		self.html.SetStyleBits( 7 )
		self.html.SetMargins( 0, 0 )
		#self.html.SetMarginType( 2, stc.STC_MARGIN_NUMBER )
		#self.html.SetMarginSensitive( 2, True )
		self.html.SetMarginWidth( 0, 0 )
		self.html.SetMarginWidth( 1, 0 )
		self.html.SetMarginWidth( 2, 0 )
		self.html.SetBufferedDraw( 1 )
		self.html.SetEdgeMode( stc.STC_EDGE_LINE )
		self.html.SetEdgeColumn( 80 )
		self.html.SetTabWidth( 4 )
		self.html.SetUseTabs( True )
		self.html.SetTabIndents( 4 )
		self.html.SetIndent( 4 )
		self.html.SetIndentationGuides( True )
		#self.html.SetCaretPeriod( 100 )
		self.html.SetCaretWidth( 4 )
		self.html.SetCaretForeground( "#FF0000" )
		self.html.StyleSetSpec( stc.STC_STYLE_LINENUMBER, "back:#404040")
		self.html.StyleSetSpec( stc.STC_STYLE_BRACELIGHT, "fore:#FFFFFF,back:#0000FF, bold" )
		self.html.StyleSetSpec( stc.STC_STYLE_BRACEBAD  , "fore:#FFFFFF,back:#FF0000, bold" )
		# normal html
		self.html.StyleSetSpec( stc.STC_H_DEFAULT, "fore:#000000" )
		self.html.StyleSetSpec( stc.STC_H_TAG, "fore:#4433CC,bold" )
		self.html.StyleSetSpec( stc.STC_H_TAGUNKNOWN, "fore:#CC0055,bold")
		self.html.StyleSetSpec( stc.STC_H_ATTRIBUTE, "fore:#336655" )
		self.html.StyleSetSpec( stc.STC_H_ATTRIBUTEUNKNOWN, "fore:#CC0055" )
		self.html.StyleSetSpec( stc.STC_H_DOUBLESTRING, "fore:#888822" )
		self.html.StyleSetSpec( stc.STC_H_NUMBER, "fore:#992299" )
		self.html.StyleSetSpec( stc.STC_H_COMMENT, "fore:#11AA33,back:#EEFFEE" )
		# javascript
		self.html.StyleSetSpec( stc.STC_HJ_DEFAULT, "back:#ffefef,fore:#004A7F,eol" )
		self.html.StyleSetSpec( stc.STC_HJ_SYMBOLS, "back:#ffefef,fore:#7F0000,bold" )
		self.html.StyleSetSpec( stc.STC_HJ_WORD, "back:#ffefef,fore:#4433CC,bold" )
		self.html.StyleSetSpec( stc.STC_HJ_REGEX, "fore:#CC0055,back:#FFE97F,bold" )
		self.html.StyleSetSpec( stc.STC_HJ_SINGLESTRING, "back:#ffefef,fore:#336655" )
		self.html.StyleSetSpec( stc.STC_HJ_KEYWORD, "fore:#7F0000,back:#FFE97F,bold" )
		self.html.StyleSetSpec( stc.STC_HJ_DOUBLESTRING, "back:#ffefef,fore:#888822" )
		self.html.StyleSetSpec( stc.STC_HJ_NUMBER, "back:#ffefef,fore:#992299" )
		self.html.StyleSetSpec( stc.STC_HJ_COMMENT, "fore:#11aa44,back:#ffefef,eol" )
		self.html.StyleSetSpec( stc.STC_HJ_COMMENTLINE, "fore:#11aa44,back:#ffefef,eol" )
		self.html.StyleSetSpec( stc.STC_HJ_COMMENTDOC, "fore:#11aa44,back:#ffefef,eol" )	
		htmlKeywords = (
			"a abbr acronym address applet area b base basefont bdo big blockquote"
			" body br button caption center cite code col colgroup dd del dfn dir"
			" div dl dt em fieldset font form frame frameset h1 h2 h3 h4 h5 h6"
			" head hr html i iframe img input ins isindex kbd label legend li link"
			" map menu meta noframes noscript object ol optgroup option p param"
			" pre q s samp script select small span strike strong style sub sup"
			" table tbody td textarea tfoot th thead title tr tt u ul var xml"
			" xmlns abbr accept-charset accept accesskey action align alink alt"
			" archive axis background bgcolor border cellpadding cellspacing char"
			" charoff charset checked cite class classid clear codebase codetype"
			" color cols colspan compact content coords data datafld dataformatas"
			" datapagesize datasrc datetime declare defer dir disabled enctype"
			" event face for frame frameborder headers height href hreflang hspace"
			" http-equiv id ismap label lang language leftmargin link longdesc"
			" marginwidth marginheight maxlength media method multiple name nohref"
			" noresize noshade nowrap object onblur onchange onclick ondblclick"
			" onfocus onkeydown onkeypress onkeyup onload onmousedown onmousemove"
			" onmouseover onmouseout onmouseup onreset onselect onsubmit onunload"
			" profile prompt readonly rel rev rows rowspan rules scheme scope"
			" selected shape size span src standby start style summary tabindex"
			" target text title topmargin type usemap valign value valuetype"
			" version vlink vspace width text password checkbox radio submit reset"
			" file hidden image public !doctype"
		)
		self.html.SetKeyWords(0, htmlKeywords)
		
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
		
	def OnOk(self, evt):
		self.UpdateAll()
		self.project.extractTitle = self.et
		self.project.extractContent = self.ec
		evt.Skip()
		
