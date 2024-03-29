###############################################################
# Name:			 Grabber.py
# Purpose:	 Grab html files and compiles them into chm
# Author:		 Luca Allulli (webmaster@roma21.it)
# Created:	 2009-08-24
# Copyright: Luca Allulli (http://www.skeed.it/songpress.html)
# License:	 GNU GPL v2
##############################################################

from Globals import *
from Project import *
import BeautifulSoup
import urllib2
import urlparse
import tempfile
import os
import os.path
import shutil
import subprocess
import wx
import wx.lib.newevent
import threading
import traceback
from genshi.template import TemplateLoader
from genshi.builder import tag

EventTextMessage, EVT_TEXT_MESSAGE = wx.lib.newevent.NewEvent()
EventCompleted, EVT_COMPLETED = wx.lib.newevent.NewEvent()


class Repository(object):
	def __init__(self):
		object.__init__(self)
		self.i = 1
		self.d = {}

	def __getitem__(self, s):
		if s not in self.d:
			p, e = os.path.splitext(s)
			self.d[s] = str(self.i) + e
			self.i += 1
		return self.d[s]

	def SetItemWithExt(self, s, ext):
		if s not in self.d:
			self.d[s] = str(self.i) + ext
			self.i += 1
		return self.d[s]

	def __iter__(self):
		for k in self.d:
			yield k

	def __in__(self, k):
		return k in self.d

class Grabber(threading.Thread):
	def __init__(self, tree, project, owner, keepOutput = False):
		threading.Thread.__init__(self)
		self.tree = tree
		self.project = project
		self.owner = owner
		self.stop = False
		self.keepOutput = keepOutput

	def Send(self, msg):
		evt = EventTextMessage(message=msg)
		wx.PostEvent(self.owner, evt)

	def Load(self, url, text=None):
		try:
			fn = os.path.join(self.dir, self.repo[url])
			if text is None:
				if not os.path.isfile(os.path.join(self.tpldir, url)):
					s = urllib2.urlopen(url)
				else:
					s = open(os.path.join(self.tpldir, url), "rb")
				text = s.read()
				s.close()
			f = open(fn, "wb")
			f.write(text)
			f.close()
		except Exception, exc:
			msg = "\nWARNING: could not open %s\n%s" % (url, str(exc))
			self.Send(msg)

	def TransformUrl(self, baseurl, node, attrib, load=False):
		try:
			url = node[attrib]
		except:
			return
		if url[:7].lower() == "http://" and url not in self.repo:
			return
		if not os.path.isfile(os.path.join(self.tpldir, url)):
			url = urlparse.urljoin(baseurl, url)
		node[attrib] = self.repo[url]
		if load:
			self.Load(url)

	def InsertIntoRepository(self):
		for k in self.treeList:
			self.repo.SetItemWithExt(k[1], '.htm')

	def GetPrevItem(self, item):
		prev = self.tree.GetPrevItem(item)
		if item.IsOk():
			return prev.GetItemUrl()
		parent = self.tree.GetItemParent(item)
		if parent != self.tree.GetRootItem():
			prev = self.tree.GetNextItem(item)
			if item.IsOk():
				return next.GetItemUrl()
		return False

	def Grab(self):
		i = 0
		nn = len(self.treeList)
		for k in self.treeList:
			# grab page and extract content
			u = k[1]
			self.Send("Grabbing %s" % (u,))
			s = urllib2.urlopen(u)
			h = s.headers
			soup = BeautifulSoup.BeautifulSoup(s)
			s.close()
			title = unicode(self.extractTitle(soup.html))
			self.tree.SetItemText(k[0], glb.Join(title, u))
			content = self.extractContent(soup.html)
			if type(content) != list and type(content) != BeautifulSoup.ResultSet:
				content = [content]
			c = "".join([unicode(x) for x in content])
			next = self.treeList[i + 1][1] if i + 1 < nn else False
			prev = self.treeList[i - 1][1] if i - 1 >= 0 else False
			parent = k[2] if k[2] != "" else False
			# apply template
			text = self.tpl.generate(
				title=title,
				content=c,
				next=next,
				prev=prev,
				parent=parent
			).render('html', encoding='utf-8')
			# re-parse generated html, and "normalize" urls
			soup = BeautifulSoup.BeautifulSoup(text)
			a = soup.findAll('a')
			img = soup.findAll('img')
			link = soup.findAll('link')
			for el in a:
				self.TransformUrl(u, el, 'href')
			for el in img:
				self.TransformUrl(u, el, 'src', True)
			for el in link:
				self.TransformUrl(u, el, 'href', True)
			if self.project.grabJavascript:
				script = soup.findAll('script')
				for el in script:
					self.TransformUrl(u, el, 'src', True)
			self.Load(u, soup.renderContents())
			i += 1


	def GenerateTocItem(self, item, e):
		t, u = glb.Split(self.tree.GetItemText(item))
		li = tag.li
		e.append(li)
		object = tag.object(type='text/sitemap')
		li.append(object)
		object.append(tag.param(name="Name", value=t))
		object.append(tag.param(name="Local", value=self.repo[u]))
		object.append(tag.param(name="ImageNumber", value='0'))
		if self.tree.ItemHasChildren(item):
			ul = tag.ul
			li.append(ul)
			self.DoWithChildren(
				item,
				lambda i: self.GenerateTocItem(i, ul)
			)

	def GenerateTreeList(self, item):
		t, u = glb.Split(self.tree.GetItemText(item))
		p = self.tree.GetItemParent(item)
		if p != self.tree.GetRootItem():
			pt, pu = glb.Split(self.tree.GetItemText(p))
		else:
			pu = ""
		self.treeList.append((item, u, pu))
		if self.tree.ItemHasChildren(item):
			self.DoWithChildren(
				item,
				self.GenerateTreeList
			)

	def DoWithChildren(self, item, what):
		el, cookie = self.tree.GetFirstChild(item)
		while el.IsOk():
			self.CheckStop()
			pos = what(el)
			el, cookie = self.tree.GetNextChild(item, cookie)

	def GenerateToc(self):
		self.tocFile = os.path.join(self.dir, "toc.hhc")
		loader = TemplateLoader('.')
		toctpl = loader.load(glb.AddPath('toc-template.hhc'))
		ul = tag.ul
		self.DoWithChildren(
			self.tree.GetRootItem(),
			lambda i: self.GenerateTocItem(i, ul)
		)
		f = open(self.tocFile, "w")
		f.write(toctpl.generate(list=ul).render('html').decode('utf-8').encode('utf-16'))
		f.close()

	def GenerateProjectFile(self):
		self.projFile = os.path.join(self.dir, "project.hhp")
		f = open(self.projFile, "w")
		i = """[OPTIONS]
Default Font=Arial,8,0
Title=%s
Full-text search=Yes
Compatibility=1.1
Auto Index=Yes
Compiled file=%s
Contents file=toc.hhc

[FILES]
""" % (
			os.path.splitext(self.name)[0],
			self.name
		)
		f.write(i)
		for k in self.treeList:
			f.write(self.repo[k[1]] + "\n")
		f.close()

	def Compile(self):
		try:

			# create temp dir and repository
			self.dir = tempfile.mkdtemp()
			self.repo = Repository()

			self.path, self.name = os.path.split(self.project.name)

			# define extracting methods
			m = "def extractTitle(html):\n"
			for l in self.project.extractTitle.splitlines():
				m += "\t" + l + "\n"
			exec m
			self.extractTitle = extractTitle

			m = "def extractContent(html):\n"
			for l in self.project.extractContent.splitlines():
				m += "\t" + l + "\n"
			exec m
			self.extractContent = extractContent

			# load template
			loader = TemplateLoader('.')
			self.tpl = loader.load(self.project.template)
			self.tpldir, f = os.path.split(self.project.template)

			# generate tree list
			self.treeList = []
			self.DoWithChildren(self.tree.GetRootItem(), self.GenerateTreeList)

			# insert urls into repository
			self.InsertIntoRepository()

			# grab documents
			self.Grab()

			# generate project files
			self.GenerateToc()
			self.GenerateProjectFile()

			# launch help compiler
			self.Send("\nLaunching MS Help Compiler...")
			hc = os.path.join(os.environ['PROGRAMFILES'], "HTML Help Workshop\\hhc.exe")
			os.chdir(self.dir)
			proc = subprocess.Popen(("%s project.hhp" % (hc,)), stdout=subprocess.PIPE)
			for l in proc.stdout:
				self.CheckStop()
				self.Send(l.strip("\n"))

			# copy output file in project dir
			#d, f = os.path.split(self.project.)
			source = os.path.join(self.dir, self.name)
			dest = os.path.join(self.path, self.name)
			if os.path.isfile(dest):
				os.remove(dest)
			shutil.move(source, dest)
		except Exception, ex:
			#msg = "\nERROR:\n" + traceback.format_exc()
			msg = "\nERROR:\n" + str(ex)
			self.Send(msg)

		# delete temp dir
		os.chdir(os.environ['PROGRAMFILES'])
		if self.keepOutput:
			self.Send("HTML Workshop files: %s" % (self.dir,))
		else:
			try:
				for root, dirs, files in os.walk(self.dir, topdown=False):
					for name in files:
						os.remove(os.path.join(root, name))
					for name in dirs:
						os.rmdir(os.path.join(root, name))
				os.rmdir(self.dir)
			except Exception, ex:
				self.Send("\nCould not remove temporary dir: %s\n%s" % (self.dir, str(ex)))

	def Stop(self):
		self.stop = True

	def CheckStop(self):
		if self.stop:
			raise Exception("Stopped")

	def run(self):
		self.Compile()
		evt = EventCompleted()
		wx.PostEvent(self.owner, evt)

