from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

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
