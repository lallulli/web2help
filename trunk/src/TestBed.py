# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Aug 25 2009)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
from wx.stc import *
from PythonSTC import *

###########################################################################
## Class TestBed
###########################################################################

class TestBed ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__  ( self, parent, id = wx.ID_ANY, title = u"web2help testbed", pos = wx.DefaultPosition, size = wx.Size( 433,438 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.RESIZE_BORDER )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer8 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_splitter1 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter1.Bind( wx.EVT_IDLE, self.m_splitter1OnIdle )
		
		self.pannelloSuperiore = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer13 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText6 = wx.StaticText( self.pannelloSuperiore, wx.ID_ANY, u"URL", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		bSizer11.Add( self.m_staticText6, 0, wx.ALL, 5 )
		
		self.url = wx.TextCtrl( self.pannelloSuperiore, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11.Add( self.url, 1, wx.ALL, 5 )
		
		self.load = wx.Button( self.pannelloSuperiore, wx.ID_ANY, u"Load", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11.Add( self.load, 0, wx.ALL, 5 )
		
		self.parse = wx.Button( self.pannelloSuperiore, wx.ID_ANY, u"Parse", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11.Add( self.parse, 0, wx.ALL, 5 )
		
		bSizer13.Add( bSizer11, 0, wx.EXPAND, 5 )
		
		
		self.html =StyledTextCtrl(self.pannelloSuperiore, wx.ID_ANY)
		bSizer13.Add( self.html, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.pannelloSuperiore.SetSizer( bSizer13 )
		self.pannelloSuperiore.Layout()
		bSizer13.Fit( self.pannelloSuperiore )
		self.pannelloInferiore = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer14 = wx.BoxSizer( wx.VERTICAL )
		
		
		self.code = PythonSTC(self.pannelloInferiore, wx.ID_ANY)
		bSizer14.Add( self.code, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer15 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.title = wx.RadioButton( self.pannelloInferiore, wx.ID_ANY, u"Title", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.title.SetValue( True ) 
		bSizer15.Add( self.title, 0, wx.ALL, 5 )
		
		self.content = wx.RadioButton( self.pannelloInferiore, wx.ID_ANY, u"Content", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer15.Add( self.content, 0, wx.ALL, 5 )
		
		bSizer14.Add( bSizer15, 0, wx.EXPAND, 5 )
		
		bSizer16 = wx.BoxSizer( wx.HORIZONTAL )
		
		m_sdbSizer1 = wx.StdDialogButtonSizer()
		self.m_sdbSizer1OK = wx.Button( self.pannelloInferiore, wx.ID_OK )
		m_sdbSizer1.AddButton( self.m_sdbSizer1OK )
		self.m_sdbSizer1Cancel = wx.Button( self.pannelloInferiore, wx.ID_CANCEL )
		m_sdbSizer1.AddButton( self.m_sdbSizer1Cancel )
		m_sdbSizer1.Realize();
		bSizer16.Add( m_sdbSizer1, 1, wx.EXPAND, 5 )
		
		bSizer14.Add( bSizer16, 0, wx.EXPAND, 5 )
		
		self.pannelloInferiore.SetSizer( bSizer14 )
		self.pannelloInferiore.Layout()
		bSizer14.Fit( self.pannelloInferiore )
		self.m_splitter1.SplitHorizontally( self.pannelloSuperiore, self.pannelloInferiore, 0 )
		bSizer8.Add( self.m_splitter1, 1, wx.EXPAND, 5 )
		
		self.SetSizer( bSizer8 )
		self.Layout()
		
		# Connect Events
		self.load.Bind( wx.EVT_BUTTON, self.OnLoad )
		self.parse.Bind( wx.EVT_BUTTON, self.OnParse )
		self.title.Bind( wx.EVT_RADIOBUTTON, self.OnTitle )
		self.content.Bind( wx.EVT_RADIOBUTTON, self.OnContent )
		self.m_sdbSizer1OK.Bind( wx.EVT_BUTTON, self.OnOk )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnLoad( self, event ):
		event.Skip()
	
	def OnParse( self, event ):
		event.Skip()
	
	def OnTitle( self, event ):
		event.Skip()
	
	def OnContent( self, event ):
		event.Skip()
	
	def OnOk( self, event ):
		event.Skip()
	
	def m_splitter1OnIdle( self, event ):
		self.m_splitter1.SetSashPosition( 0 )
		self.m_splitter1.Unbind( wx.EVT_IDLE )
	

