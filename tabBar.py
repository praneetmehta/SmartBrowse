from guielements import *
from PyQt5.QtCore import QCoreApplication
import copy

class TabWidget(QTabWidget):
	tabCount = 0
	tabs = []
	tabdump = []
	def __init__(self, parent):
		super().__init__()
		self.home = None
		with open('Home/google.html', 'r') as file:
			self.home = file.read()
			pass
		hbox = QHBoxLayout()
		hbox.setContentsMargins(0,0,0,0)
		self.setLayout(hbox)
		self.parent = parent
		self.webhistory = self.parent.history
		self.bookmarks = self.parent.bookmarks
		self.controller = self.parent.nav
		self.setTabsClosable(True)
		home = Tab(self, html = self.home)
		TabWidget.tabCount+=1
		TabWidget.tabs.append(home)
		if(home.URL is not None):
			logger.log(home.URL, 2)
			home.loadURL()
		else:
			home.showHome()
		self.addTab(home, 'Home')
		self.currentTabIndex = 0
		self.currentTab = home
		self.currentURL = ''
		# self.setCornerWidget(self.controller.btn_pref)
		self.tabController()

	def onChange(self, i):
		logger.log('TAB CHANGED')
		self.currentTabIndex = i
		self.currentTab = self.getCurrent()
		self.currentURL = self.currentTab.URL
		self.controller.URLinput.setText(self.currentURL)
		# self.progressBar.update(self.currentTab.progress)
		self.controller.URLinput.setCursorPos(6)

	def checkBookmarks(self):
		logger.log('CHECKING FOR BOOKMARKS', 1)
		tab = self.currentTab
		if tab.bookmarkStatus[1] == False:
			logger.log('URL NOT CHECKED')
			tab.bookmarkStatus = [self.bookmarks.find(tab.URL), True]
			logger.log(tab.bookmarkStatus)
		logger.log('TAB URL ' + tab.URL)
		if tab.bookmarkStatus[0] == True:
			logger.log('EXISTS IN BOOKMARKS')
			self.controller.btn_bookmark.setIcon(QIcon('img/bookmarked.png'))
		else:
			logger.log('NOT IN BOOKMARKS')
			self.controller.btn_bookmark.setIcon(QIcon('img/addtobookmark.png'))

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
		logger.log('INSIDE FUNCTION UPDATE ICON')
		tabid = self.tabIndex(thisTab)
		self.setTabIcon(tabid, QIcon(thisTab.favicon))

	# def updateProgress(self, tab, status=False):
	# 	# print('INSIDE FUNCTION UPDATE PROGRESS')
	# 	if self.tabIndex(tab) == self.currentTabIndex:
	# 		self.progressBar.update(tab.progress, status)

	def update(self, thisTab, complete = False):
		logger.log('INSIDE FUNCTION UPDATE')
		temptitle = ''
		tabid = self.tabIndex(thisTab)
		if len(thisTab.pageTitle) > 12:
			temptitle = thisTab.pageTitle[:12]+'...'
		else:
			temptitle = thisTab.pageTitle[:12]
		self.setTabText(tabid, temptitle)
		self.setTabToolTip(tabid, thisTab.pageTitle)
		if(self.current == thisTab):
			logger.log('YES')
			self.currentURL = thisTab.URL
			self.controller.URLinput.setText(self.currentURL)
		else:
			logger.log("NO")
		self.controller.URLinput.setCursorPos(0)
		t = Thread(target = self.checkBookmarks)
		t.start()

	def closeTab(self, index=None):
		logger.log('CLOSING TAB', 1)
		if TabWidget.tabCount <= 1 :
			QCoreApplication.quit()
			return
		if index == None:
			index = self.currentTabIndex
		TabWidget.tabCount-=1
		tab = TabWidget.tabs.pop(index)
		self.dumpTab(tab.history(), tab.URL)
		tab.deleteLater()
		self.removeTab(index)
	
	def dumpTab(self, history, url):
		TabWidget.tabdump.append((history, url))
		if len(TabWidget.tabdump) > 10:
			tabToDie = tabdump.pop(0)

	def reopenTab(self):
		if len(TabWidget.tabdump) > 0:
			tabToRevive = TabWidget.tabdump.pop(-1)
			self.addNewTab(url = tabToRevive[1], history = tabToRevive[0])
			# TabWidget.tabCount+=1
			# TabWidget.tabs.append(tabToRevive)
			# if tabToRevive.URL is not None or tabToRevive.URL != 'about:blank':
			# 	print(tabToRevive.URL)
			# 	tabToRevive.loadURL()
			# else:
			# 	tabToRevive.showHome()
			# self.currentTab = tabToRevive
			# self.currentTabIndex = len(TabWidget.tabs)-1
			# self.setCurrentIndex(self.currentTabIndex)
			# self.setTabShape(1)
		else:
			logger.log("NO TAB TO REOPEN", 2)

	def addNewTab(self, html=None, url=None, history = None):
		newTab = Tab(self)
		if html is not None:
			newTab.html = html
		else:
			newTab.html = self.home
		if url is not None:
			newTab.URL = url
		self.addTab(newTab, newTab.pageTitle)
		TabWidget.tabCount+=1
		TabWidget.tabs.append(newTab)
		if history is not None:
			self.history = history
		if newTab.URL is not None:
			newTab.loadURL()
		else:
			newTab.showHome()
		self.currentTab = newTab
		self.currentTabIndex = len(TabWidget.tabs)-1
		self.setCurrentIndex(self.currentTabIndex)
		logger.log(self.current, 2)
		self.setTabShape(1)

	def showHistory(self):
		self.addNewTab(html = HTMLWriter().historyWriter(self.webhistory.Store))

	def showBookmarks(self):
		self.addNewTab(html = HTMLWriter().bookmarkWriter(self.bookmarks.Store))
