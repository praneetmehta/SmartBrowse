from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebEngineCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineSettings
from util import *
import sys


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


class TextInput(QComboBox):
	fields = []
	def __init__(self, font, fsize):
		super().__init__()
		self.setEditable(True)
		# self.completer().setCompletionMode(QCompleter.PopupCompletion)
		self.maxCount = 6
		TextInput.fields.append(self)

	def text(self):
		return self.currentText()

	def setText(self, text):
		self.lineEdit().setText(text)

	def setCursorPos(self, pos):
		self.lineEdit().setCursorPosition(pos)

class WebViewer(QWebEngineView):
	def __init__(self, parent, URL, html):
		super().__init__()
		self.parent = parent
		self._URL = URL
		self.html = html
		self.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
		self.settings().setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
		self.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
		self.settings().setAttribute(QWebEngineSettings.AutoLoadImages, True)
		self.settings().setAttribute(QWebEngineSettings.AutoLoadIconsForPage, True)
		self.settings().setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)
		self.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)


	@property
	def URL(self):
		return self._URL
	
	@URL.setter
	def URL(self, value):
		self._URL = value

	@property
	def HTML(self):
		return self.html
	
	@HTML.setter
	def HTML(self, value):
		self.html = value

	def loadURL(self):
		print('Loading URL')
		self.favicon = QIcon('img/loading_basic.png')
		self.parent.updateIcon(self)
		if self.html is None:
			if self.URL[:4] != 'http':
				self.URL = 'http://'+self.URL
			self.load(QUrl(self.URL))
			print('Loading ', self.URL)
		else:
			self.setHtml(self.html)
		return

class Tab(WebViewer):
	def __init__(self, parent, title='Home', URL='http://google.com', html = None):
		super().__init__(parent, URL, html)
		self.webhistory = self.parent.webhistory
		self.controller()
		self.progress = 0
		self.pageTitle = title
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

	def linkHoverController(self, link):
		print(link)

	def requestFS(self, req):
		req.accept()

	def adjustTitle(self):
		self.pageTitle = self.title()
		self.parent.update(self)

	def adjustIcon(self):
		self.favicon = self.icon()
		self.faviconURL = self.iconUrl()
		if self.favicon:
			self.parent.updateIcon(self)

	def finishLoading(self):
		self.URL = self.url().toString()
		self.progress = 100
		self.webhistory.add(self.URL)
		self.resetProgress()

	def setProgress(self, p):
		self.progress = p
		self.URL = self.url().toString()
		self.parent.updateProgress(self)

	def resetProgress(self):
		self.progress = 0
		self.parent.update(self)
		self.parent.updateProgress(self, True)


