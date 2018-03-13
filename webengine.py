from PyQt5.QtWebEngineWidgets import QWebEngineSettings, QWebEnginePage, QWebEngineView
from PyQt5.QtCore import pyqtSignal
from networkManager import NetworkManager
from logUtil import Log

logger = Log()

class WebPage(QWebEnginePage):
	restart_loader = pyqtSignal()
	
	def __init__(self, parent=None):
		super().__init__(parent)
		self.netmanager = NetworkManager()
		

	def acceptNavigationRequest(self, url,  _type, isMainFrame):
		# if (_type == QWebEnginePage.NavigationTypeLinkClicked or \
		# _type == QWebEnginePage.NavigationTypeOther or \
		# _type == QWebEnginePage.NavigationTypeFormSubmitted ):
		if(1):
			logger.log("TYPE", _type)
			self.netmanager.examine(url)
			self.restart_loader.emit()
			return True
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