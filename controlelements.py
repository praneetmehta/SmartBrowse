from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread

class Shortcut(QAction):

	def __init__(self, name, keyseq, trigger, parent, *args):
		super().__init__((name), parent)
		self.parent = parent
		self.name = name
		self.keyseq = keyseq
		self.trigger = trigger
		self.extra = args
		self.createShortcut()

	def createShortcut(self):
		self.setShortcut(QKeySequence(self.keyseq))
		self.parent.addAction(self)
		self.triggered.connect(lambda : self.trigger())


class GifThread(QThread):
	def __init__(self, tab, progress, gif):
		QThread.__init__(self)
		self.tab = tab
		print(progress)
		self.loadingGif = gif

	def __del__(self):
		self.wait()
	
	def frameChange(self, int):
		print('changing frame')
		self.tab.favicon = self.loadingGif.currentPixmap()

	def run(self):
		print('RUnning')
		self.tab.favicon = self.loadingGif.currentPixmap()
		self.loadingGif.frameChanged.connect(self.frameChange)
		self.loadingGif.setPaused(False)
		self.tab.parent.updateIcon(self.tab)
			

class NewTabThread(QThread):
	def __init__(self, func):
		QThread.__init__(self)
		self.func = func

	def __del__(self):
		self.wait()

	def run(self):
		self.func.addNewTab()
		
			