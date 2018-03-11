from guielements import *

class TabWidget(QTabWidget):
	tabCount = 0
	tabs = []
	def __init__(self, parent):
		super().__init__()
		self.parent = parent
		self.webhistory = self.parent.history
		self.bookmarks = self.parent.bookmarks
		self.controller = self.parent.nav
		self.progressBar = self.parent.loadProgress
		self.setTabsClosable(True)
		home = Tab(self)
		TabWidget.tabCount+=1
		TabWidget.tabs.append(home)
		home.loadURL()
		self.addTab(home, 'Home')
		self.currentTabIndex = 0
		self.currentTab = home
		self.currentURL = ''
		# self.setCornerWidget(self.controller.btn_newtab)
		self.tabController()	

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
		print('Updating icon')
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
		else:
			print("NO")
		self.controller.URLinput.setCursorPos(0)

	def closeTab(self, index=None):
		if TabWidget.tabCount <= 1 :
			sys.exit()
		if index == None:
			index = self.currentTabIndex
		TabWidget.tabCount-=1
		tab = TabWidget.tabs.pop(index)
		tab.deleteLater()
		self.removeTab(index)
		

	def addNewTab(self, html=None, url=None):
		newTab = Tab(self)
		if(url is not None):
			newTab.URL = url
		self.addTab(newTab, newTab.pageTitle)
		TabWidget.tabCount+=1
		TabWidget.tabs.append(newTab)
		newTab.loadURL()
		self.currentTab = newTab
		self.currentTabIndex = len(TabWidget.tabs)-1
		self.setCurrentIndex(self.currentTabIndex)
		self.setTabShape(1)

	def showHistory(self):
		self.addNewTab(html = HTMLWriter().historyWriter(self.webhistory.Store))

	def showBookmarks(self):
		self.addNewTab(html = HTMLWriter().bookmarkWriter(self.bookmarks.Store))
