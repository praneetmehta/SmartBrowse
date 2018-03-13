from PyQt5.QtGui import QIcon, QMovie,QFont
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QUrl
from PyQt5.QtWidgets import *
from webengine import WebViewer, WebPage
import sys
import pyautogui
from threading import Thread
from util import *
from logUtil import Log
from controlelements import GifThread
validator = URLValidator()
logger = Log()
HomePageURL = None

class ProgressBar(QProgressBar):
	bars = []
	count = 0
	def __init__(self, parent):
		super().__init__(parent)
		self.id = ProgressBar.count
		self.setValue(0)
		ProgressBar.count += 1

	def setGeom(self, x, y, w, h):
		self.setGeometry(x,y,w,h)

	def update(self, val, complete=False):
		self.show()
		if(val >= 100 or complete == True):
			val = 0
			self.hide()
		elif(val == 100 and complete == False):
			val = 95
		self.setValue(val)

class Button(QPushButton):

	buttons = []
	def __init__(self, icon="", name="", parent=None):
		super().__init__(QIcon(icon), name, parent)
		self.name = name
		self.icon = icon
		self.parent = parent
		self.resize(self.minimumSizeHint())
		Button.buttons.append(self)

class TextInput(QComboBox, QLineEdit):

	fields = []
	def __init__(self, font, fsize):
		super().__init__()
		self.setEditable(True)
		self.completer().setCompletionMode(QCompleter.PopupCompletion)
		self.maxCount = 6
		TextInput.fields.append(self)

	def text(self):
		return self.currentText()

	def setText(self, text):
		self.lineEdit().setText(text)

	def setCursorPos(self, pos):
		self.lineEdit().setCursorPosition(pos)
	
	# def focusInEvent(self, e):
	# 	print('Focused')
		# pyautogui.click(clicks = 3)

class Tab(WebViewer):
	def __init__(self, parent, title='Home', URL=HomePageURL, html = None):
		super().__init__(parent, URL, html)
		self.webhistory = self.parent.webhistory
		self.controller()
		self.progress = 0
		self.pageTitle = title
		self.bookmarkStatus = [False, False]
		self.loadingGif = QMovie('img/loader.gif')
		self.loadingGif.setCacheMode(QMovie.CacheAll) 
		self.loadingGif.setSpeed(50)
		self.loadingGif.start()
		self.loadingGif.setPaused(True)
		self.loadingGif.frameChanged.connect(self.nextFrame)
		self.favicon = self.loadingGif.currentPixmap()
		# self.loadingMovie = QMovie('img/loading.gif')
	# 	self.newTabAction = QAction('Open in new tab', self)
	# 	self.newTabAction.triggered.connect(self.requestInNewTab)
	
	# def contextMenuEvent(self, event):
	# 	menu = self.page().createStandardContextMenu()
	# 	hit = self.page().mainFrame().hitTestContent(event.pos())
	# 	url = hit.linkUrl()
	# 	if url.isValid():
	# 		self.newTabAction.setData(url)
	# 		menu.addAction(self.newTabAction)
	# 	menu.exec_(event.globalPos())

	# def requestInNewTab(self):
	# 	url = self.newTabAction.data()
	# 	self.parent.addNewTab(URL = url)

	def controller(self):
		self.titleChanged.connect(self.adjustTitle)
		self.iconChanged.connect(self.adjustIcon)
		self.loadProgress.connect(self.setProgress)
		self.loadFinished.connect(self.finishLoading)
		# self.page().linkHovered.connect(self.linkHoverController)
		self.page().fullScreenRequested.connect(self.requestFS)

	@pyqtSlot()
	def restartLoader(self):
		logger.log(self.progress)
		if self.progress != 100:
			logger.log('EVENT CATCHED. NOW RESTARTING', 1)
			self.loadingGif.setPaused(False)
			# loadingThread = GifThread(self, self.progress, self.loadingGif)
			# loadingThread.start()

	def requestFS(self, req):
		logger.log("FULL SCREEN REQUESTED", 1)
		self.showFullScreen()
		req.accept()

	def adjustTitle(self):
		logger.log("INSIDE ADJUSTTITLE")
		self.bookmarkStatus = [False, False]
		self.pageTitle = self.title()
		self.parent.update(self)

	def adjustIcon(self):
		logger.log('INSIDE FUNCTION ADJUSTICON')
		self.favicon = self.icon()
		self.faviconURL = self.iconUrl()
		if self.favicon:
			self.parent.updateIcon(self)

	def finishLoading(self):
		logger.log('INSIDE FUNCTION FINISH LOADING', 1)
		self.URL = self.url().toString()
		self.progress = 100
		self.webhistory.add(self.URL, self.pageTitle)
		self.resetProgress()
		self.loadingGif.setPaused(True)

	def setProgress(self, p):
		logger.log('INSIDE FUNCTION SETPROGRESS')
		self.progress = p
		self.URL = self.url().toString()
		
		# self.parent.updateProgress(self)

	def resetProgress(self):
		logger.log('INSIDE FUNCTION RESET PROGRESS')
		self.parent.update(self, True)
		# self.parent.updateProgress(self, True)
	
	def nextFrame(self, int):
		self.favicon = self.loadingGif.currentPixmap()
		self.parent.updateIcon(self)

	def showHome(self):
		if self.html is not None:
			self.setHtml(self.html)
	# def acceptNavigationRequest(self, frame, request, type):
	# 	print(request)
	
	def loadURL(self):
		if(validator.validate(self.URL) == False):
			self.showHome()
			return
		logger.log('LOADING URL '+self.URL, 2)
		self.parent.updateIcon(self)

		if self.URL[:4] != 'http':
			self.URL = 'http://'+self.URL
		self.load(QUrl(self.URL))
		print('Loading ', self.URL)

class CompositeWidget(QWidget):

	def __init__(self):
		super().__init__()
		self.vbox = QVBoxLayout()
		self.setLayout(self.vbox)
		(left, right, top, bottom) = self.vbox.getContentsMargins()
		self.vbox.setContentsMargins(0, 0, 0, 0)

		self.hbox = QHBoxLayout()
		self.vbox.addLayout(self.hbox)

		self.widgets = []

	def addWidget(self, widget):
		try:
			self.hbox.addWidget(widget)
			self.widgets.append(widget)
		except:
			pass


class ToggleSwitchComposite(QWidget):
	toggled_signal = pyqtSignal(bool)

	def __init__(self):
		super().__init__()

		self.updating_gui_bool = False

		vbox = QVBoxLayout()
		self.setLayout(vbox)
		(left, right, top, bottom) = vbox.getContentsMargins()
		vbox.setContentsMargins(0, 0, 5, 5)

		hbox = QHBoxLayout()
		vbox.addLayout(hbox)

		self.on_qpb = Button(name = "On")
		hbox.addWidget(self.on_qpb)
		self.on_qpb.setFixedWidth(40)
		self.on_qpb.setCheckable(True)
		self.on_qpb.toggled.connect(self.on_on_toggled)

		self.off_qpb = Button(name = "Off")
		hbox.addWidget(self.off_qpb)
		self.off_qpb.setFixedWidth(40)
		self.off_qpb.setCheckable(True)
		self.off_qpb.toggled.connect(self.on_off_toggled)

		self.state_qll = QLabel("Enabled")
		hbox.addWidget(self.state_qll)
		new_font = QFont()
		new_font.setBold(True)
		self.state_qll.setFont(new_font)

	def on_on_toggled(self, i_checked: bool):
		if self.updating_gui_bool:
			return
		if i_checked:
			self.toggled_signal.emit(True)
			self.update_gui(True)

	def on_off_toggled(self, i_checked: bool):
		if self.updating_gui_bool:
			return
		if i_checked:
			self.toggled_signal.emit(False)
			self.update_gui(False)

	def update_gui(self, i_enabled: bool):
		self.updating_gui_bool = True

		if i_enabled:
			self.on_qpb.setChecked(True)
			self.off_qpb.setChecked(False)
			self.state_qll.setText("Enabled")
		else:
			self.on_qpb.setChecked(False)
			self.off_qpb.setChecked(True)
			self.state_qll.setText("Disabled")

		self.updating_gui_bool = False

