from guielements import *

class NavControls(QHBoxLayout):
	def __init__(self, window):
		super().__init__()
		self._w = window
		self._bookmarks = self._w.bookmarks
		self._createWidgets()
		self.currTab = None
		self.tabWidget = None
		self.layout().setContentsMargins(5,0,5,0)
		self.navController()

	def operateOn(self, tabWidget):
		self.tabWidget = tabWidget
	
	def _createWidgets(self):
		self.btn_back = Button(QIcon('img/back.png'), '', self._w)
		self.btn_forward = Button(QIcon('img/next.png'), '', self._w)
		self.btn_reload = Button(QIcon('img/reload.png'), '', self._w)
		self.btn_newtab = Button(QIcon('img/new.png'), '', self._w)
		self.btn_pref = Button(QIcon('img/setting.png'), '', self._w)
		self.btn_bookmark = Button(QIcon('img/addtobookmark.png'), '', self._w)
		self.btn_home = Button(QIcon('img/home.png'), '', self._w)
		self.URLinput = TextInput('Arial',12)
		self.searchEngine = TextInput('Arial',10)
		# self.injectURL()
		self._add()

	def injectURL(self):
		toinject = []
		for key in self._w.history.Store:
			for entry in self._w.history.Store[key]:
				toinject.append(entry[0])
		self.URLinput.insertItems(0,toinject)

	def _add(self):
		self.addWidget(self.btn_back, 1)
		self.addWidget(self.btn_forward, 1)
		self.addWidget(self.btn_reload, 1)
		self.addWidget(self.btn_home, 1)
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
		self.btn_home.clicked.connect(self.homeController)
		self.btn_bookmark.clicked.connect(self.bookmarkController)
		self.URLinput.lineEdit().returnPressed.connect(self.visitPageController)
		self.searchEngine.lineEdit().returnPressed.connect(self.searchEngineSearchController)

	def bookmarkController(self):
		title = self.tabWidget.current.pageTitle
		status = self._bookmarks.add(self.URLinput.text(), title)
		if status:
			logger.log('changing bookmark status', 2)
			self.btn_bookmark.setIcon(QIcon('img/bookmarked.png'))
		else:
			logger.log('removing bookmark', 2)
			self.btn_bookmark.setIcon(QIcon('img/addtobookmark.png'))

	def homeController(self):
		self.tabWidget.current.showHome()

	def newTabController(self):
		self.tabWidget.addNewTab()

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
		logger.log(tab.URL, 2)
		tab.loadURL()

	def searchEngineSearchController(self, se = '-g'):
		self.newTabController()
		tab = self.tabWidget.current
		tab.URL = 'https://google.com/search?q='+self.searchEngine.text().replace(' ', '+')
		tab.loadURL()

