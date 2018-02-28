from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebEngineCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineSettings
from util import *
import sys

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
		if(val >= 100 or complete == True):
			val = 0
		elif(val == 100 and complete == False):
			val = 95
		self.setValue(val)

class Button(QPushButton):
	''' 
		Button Class for creating push buttons. Inherited from QPushButton
	'''
	buttons = []
	defultStyle = """ """
	customStyle = """
						QPushButton {
							border: 1px solid #aaa;
							border-radius:14px;
							padding:6px;
						}

						QPushButton:hover
						{
							border: 1px solid #ccc;
							background-color: #ccc;
						}

					"""

	def __init__(self, icon, name, parent):
		super().__init__(QIcon(icon), name, parent)
		self.name = name
		self.icon = icon
		self.parent = parent
		self.setStyleSheet(Button.defultStyle)
		self.resize(self.minimumSizeHint())
		Button.buttons.append(self)

	def setStyle(self, style):
		self.setStyleSheet(style)

	@classmethod
	def setStyleAll(cls):
		for b in cls.buttons:
			b.setStyle(cls.customStyle)


class TextInput(QComboBox):
	fields = []
	defultStyle = """ """
	customStyle = """
						QComboBox {
							border: 1px solid #aaa;
							border-radius:14px;
							padding:5px;
							font: 14px;
							background-color: #fff;
							color: #777;
						}

						QComboBox:focus
						{
							border: 1px solid #ccc;
							color:black;
						}
						QComboBox::drop-down 
						{
						    border: 0px; /* This seems to replace the whole arrow of the combo box */
						    margin-left: -10px;
						}

						/* Define a new custom arrow icon for the combo box */
						QComboBox::down-arrow {
						    image: url(img/down.png);
						    width: 14px;
						    height: 14px;
						}

					"""
	def __init__(self, font, fsize):
		super().__init__()
		self.setStyleSheet('QComboBox {border-radius : 5px}')
		self.setStyleSheet(TextInput.defultStyle)
		self.setEditable(True)
		# self.lineEdit().setFont(QFont(font,fsize))

		# self.lineEdit().setMaxLength(45)
		TextInput.fields.append(self)

	def updateFont(self, font, fsize):
		self.setFont(QFont(font,fsize))

	def setStyle(self, style):
		self.setStyleSheet(TextInput.customStyle)

	def text(self):
		return self.currentText()

	def setText(self, text):
		self.lineEdit().setText(text)

	def setCursorPos(self, pos):
		print('cursor pos')
		self.lineEdit().setCursorPosition(pos)

	@classmethod
	def setStyleAll(cls):
		for b in cls.fields:
			b.setStyle(cls.customStyle)


class NavControls(QHBoxLayout):
	def __init__(self, window, bookmarks):
		super().__init__()
		self._w = window
		self._bookmarks = bookmarks
		self._createWidgets()
		self.currTab = None
		self.tabWidget = None
		self.navController()

	def operateOn(self, tabWidget):
		self.tabWidget = tabWidget
	
	def _createWidgets(self):
		self.btn_back = Button('img/arrowback.png', '', self._w)
		self.btn_forward = Button('img/arrowforward.png', '', self._w)
		self.btn_reload = Button('img/reload.png', '', self._w)
		self.btn_newtab = Button('img/newtab.png', '', self._w)
		self.btn_pref = Button('img/pref.png', '', self._w)
		self.btn_bookmark = Button('img/bookmarked.png', '', self._w)
		self.URLinput = TextInput('Arial',12)
		self.searchEngine = TextInput('Arial',10)
		# self.URLinput = QComboBox()
		
		self._add()

	def _add(self):
		self.addWidget(self.btn_back, 1)
		self.addWidget(self.btn_forward, 1)
		self.addWidget(self.btn_reload, 1)
		self.addWidget(self.URLinput, 120)
		self.addWidget(self.searchEngine, 20)
		self.addWidget(self.btn_newtab, 1)
		self.addWidget(self.btn_bookmark, 1)	
		self.addWidget(self.btn_pref, 1)

	def navController(self):
		self.btn_newtab.clicked.connect(self.newTabController)
		self.btn_forward.clicked.connect(self.forwardController)
		self.btn_back.clicked.connect(self.backwardController)
		self.btn_reload.clicked.connect(self.reloadController)
		self.btn_bookmark.clicked.connect(self.bookmarkController)
		self.URLinput.lineEdit().returnPressed.connect(self.visitPageController)
	
	def bookmarkController(self):
		title = self.tabWidget.current.pageTitle
		status = self._bookmarks.add(self.URLinput.text(), title)
		if status:
			print('Bookmark added')

	def newTabController(self):
		self.tabWidget.addNewTab()
		self.URLinput.setText(self.tabWidget.current.URL)

	def forwardController(self):
		tab = self.tabWidget.current
		tab.forward()

	def backwardController(self):
		tab = self.tabWidget.current
		tab.back()

	def reloadController(self):
		tab = self.tabWidget.current
		tab.reload()

	def visitPageController(self):
		tab = self.tabWidget.current
		tab.URL = self.URLinput.text()
		tab.loadURL()

class Tab(QWebEngineView):
	html = 	'''	<html>
				<head>
					<title>Home</title>
				</head>
				<body>
					<h1>Hello, World!</h1>
					<hr />
					I have nothing to say.
				</body>
				</html>
			'''
	
	def __init__(self, parent, id, webhistory, home=True, URL='http://', html = None):
		super().__init__()
		self.parent = parent
		self._id = id
		self.webhistory = webhistory
		# WebEngine Configuration
		self.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
		self.settings().setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
		self.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
		self.settings().setAttribute(QWebEngineSettings.AutoLoadImages, True)
		self.settings().setAttribute(QWebEngineSettings.AutoLoadIconsForPage, True)
		self.settings().setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)
		self.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)


		# self.setMovable(True)
		if home:
			if html is None:
				self.setHtml(Tab.html)
			else:
				self.setHtml(html)
		self.URL = URL
		self.controller()
		self.pageTitle = 'Home'
		self.progress = 0

	@property
	def id(self):
		return self._id

	def controller(self):
		self.titleChanged.connect(self.adjustTitle)
		self.iconChanged.connect(self.adjustIcon)
		self.loadProgress.connect(self.setProgress)
		self.loadFinished.connect(self.finishLoading)
		self.page().fullScreenRequested.connect(lambda request: request.accept())

	def adjustTitle(self):
		self.pageTitle = self.title()
		self.parent.update(self)

	def adjustIcon(self):
		self.favicon = self.icon()
		self.faviconURL = self.iconUrl()
		print('ICON UPDATE')
		if self.favicon:
			self.parent.updateIcon(self)

	def finishLoading(self):
		print('PAGE LOADED')
		self.URL = self.url().toString()
		self.progress = 100
		self.webhistory.add(self.URL)
		self.resetProgress()

	def setProgress(self, p):
		self.progress = p
		self.parent.updateProgress(self)

	def resetProgress(self):
		self.progress = 0
		self.parent.updateProgress(self, True)

	def loadURL(self):
		if self.URL[:4] != 'http':
			self.URL = 'https://'+self.URL
		self.load(QUrl(self.URL))
		print('Loading ', self.URL)

class HomeTab(Tab):
	def __init__(self, parent):
		super().__init__(parent)


class TabWidget(QTabWidget):
	defultStyle = 	""" """
	customStyle = 	"""

						QTabBar::tab{
							background: #DFE2DD;
							padding:5px;
							width: 130px;
							height: 20px;
							border-bottom:none;
							margin-right: 1px;
							border: 1px solid #aaa;
							border-bottom:0px solid #000;
						}
						QTabBar::tab:selected{
							background: #fff;
							color:black;
							padding:5px;
							border: 1px solid #aaa;
							border-bottom:0px solid #000;
						}
						QTabBar::close-button {
						    image: url(img/tabclose.png);
						    subcontrol-origin: padding;
						    subcontrol-position: right; 
						    padding-right: 5px;
						}
						QTabBar::close-button:hover {
						    image: url(img/tabclosehover.png);
						}


					"""
	tabCount = 0
	tabs = []
	def __init__(self, parent, nav, progressBar, history, bookmarks):
		super().__init__()
		self.webhistory = history
		self.bookmarks = bookmarks
		self.setTabsClosable(True)
		home = Tab(self, 0, self.webhistory)
		self.parent = parent
		self.progressBar = progressBar
		self.addTab(home, 'Home')
		self.currentTabIndex = 0
		self.currentTab = home
		self.setStyleSheet(TabWidget.customStyle)
		self.controller = nav
		self.currentURL = ''
		self.setCornerWidget(nav.btn_newtab)
		self.tabController()

		TabWidget.tabCount+=1
		TabWidget.tabs.append(home)

	def onChange(self, i):
		self.currentTabIndex = i
		self.currentTab = self.getCurrent()
		self.currentURL = self.currentTab.URL
		self.controller.URLinput.setText(self.currentURL)
		self.progressBar.update(self.currentTab.progress)
		self.controller.URLinput.setCursorPos(6)

	@property
	def current(self):
		return self.currentTab	

	def tabController(self):
		self.currentChanged.connect(self.onChange)
		self.tabCloseRequested.connect(self.closeTab)

	def getCurrent(self):
		return TabWidget.tabs[self.currentTabIndex]
	
	def tabIndex(self, tab):
		return TabWidget.tabs.index(tab)

	def getTab(self, tabid):
		return TabWidget.tabs[tabid]

	def updateIcon(self, thisTab):
		tabid = self.tabIndex(thisTab)
		self.setTabIcon(tabid, QIcon(thisTab.favicon))

	def updateProgress(self, tab, status=False):
		if self.tabIndex(tab) == self.currentTabIndex:
			self.progressBar.update(tab.progress, status)

	def update(self, thisTab):
		temptitle = ''
		tabid = self.tabIndex(thisTab)
		if len(thisTab.pageTitle) > 12:
			temptitle = thisTab.pageTitle[:12]+'...'
		else:
			temptitle = thisTab.pageTitle[:12]
		self.setTabText(tabid, temptitle)
		self.setTabToolTip(tabid, thisTab.pageTitle)
		if(self.current == thisTab):
			print('YES')
			self.currentURL = thisTab.URL
			self.controller.URLinput.setText(self.currentURL)
		self.controller.URLinput.setCursorPos(6)

	def closeTab(self, index=None):
		if TabWidget.tabCount <= 1 :
			sys.exit()
		if index == None:
			index = self.currentTabIndex
		TabWidget.tabCount-=1
		tab = TabWidget.tabs.pop(index)
		tab.deleteLater()
		self.removeTab(index)
		

	def addNewTab(self, url = 'http://', home = True, html = None):
		newTab = Tab(self, TabWidget.tabCount, self.webhistory, home, url, html)
		self.addTab(newTab, newTab.pageTitle)
		TabWidget.tabCount+=1
		TabWidget.tabs.append(newTab)
		self.currentTab = newTab
		self.currentTabIndex = len(TabWidget.tabs)-1
		self.setCurrentIndex(self.currentTabIndex)
		self.setTabShape(1)

	def showHistory(self):
		self.addNewTab(html = HTMLWriter().historyWriter(self.webhistory.Store))

	def showBookmarks(self):
		self.addNewTab(html = HTMLWriter().bookmarkWriter(self.bookmarks.Store))

