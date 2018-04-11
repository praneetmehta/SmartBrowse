from PyQt5.QtWebEngineWidgets import QWebEngineSettings, QWebEnginePage, QWebEngineView
from PyQt5.QtCore import pyqtSignal
# from networkManager import NetworkManager
from logUtil import Log
from adfilter import Filter
import os
import pickle

logger = Log()

class WebPage(QWebEnginePage):
	restart_loader = pyqtSignal()
	adblocker = None
	# if not os.path.exists('adblocker'):
	# 	os.makedirs('adblocker')
	# if os.path.isfile('adblocker/adfilter.pkl'):
	# 	logger.log("Loading AdBlock Rules", 2)
	# 	with open('adblocker/adfilter.pkl', 'rb') as file:
	# 		adblocker = pickle.load(file)
	# else:
	# 	adblocker = Filter(open('easylist.txt', encoding="utf8"))
	# 	with open('adblocker/adfilter.pkl', 'wb') as file:
	# 		pickle.dump(self.adblocker, file)

	def __init__(self, parent=None):
		super().__init__(parent)
		# self.netmanager = NetworkManager()

	def acceptNavigationRequest(self, url,  _type, isMainFrame):
		# if (_type == QWebEnginePage.NavigationTypeLinkClicked or \
		# _type == QWebEnginePage.NavigationTypeOther or \
		# _type == QWebEnginePage.NavigationTypeFormSubmitted ):
		# urlString = url.toString()
		# resp = False
		# if urlString[-1] == '/':
		# 	resp = WebPage.adblocker.match(url.toString()[:-1])
		# else:
		# 	resp = WebPage.adblocker.match(url.toString())

		# if 0:
		# 	logger.log("Blocking url --- "+url.toString(), 2)
		# 	return False
		# else:
		# 	logger.log("TYPE", _type)
		# 	self.restart_loader.emit()
		# 	return True
		return QWebEnginePage.acceptNavigationRequest(self, url,  _type, isMainFrame)

class WebViewer(QWebEngineView):
	def __init__(self, parent, URL, html): 
		super().__init__()
		self.parent = parent
		self.URL = URL
		self.html = html
		self.pg = WebPage(self)
		self.pg.restart_loader.connect(self.restartLoader)
		self.setPage(self.pg)
		self.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
		self.settings().setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
		self.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
		self.settings().setAttribute(QWebEngineSettings.AutoLoadImages, True)
		self.settings().setAttribute(QWebEngineSettings.AutoLoadIconsForPage, True)
		self.settings().setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)
		self.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)

	def createWindow(self, mode):
		self.parent.addNewTab()
		return self.parent.current