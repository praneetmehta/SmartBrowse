from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QUrl
from adfilter import Filter
from logUtil import Log

logger = Log()
class NetworkManager(QNetworkAccessManager):
	def __init__(self):
		super().__init__()
		# self.adblocker = Filter(open('easylist.txt', encoding="utf8"))
		self.finished.connect(self._finished)

	# def createRequest(self, op, request, device=None):
	# 		url = request.url().toString()
	# 		if self.adblocker.match(url):
	# 			print('blocking url, ', url)
	# 			return QNetworkAccessManager.createRequest(self, self.GetOperation, QNetworkRequest(QUrl()))
	# 		else:
	# 			print('good to go', url)
	# 			return QNetworkAccessManager.createRequest(self, op, request, device)

	def examine(self, url):
		self.get(QNetworkRequest(QUrl(url)))

	def _finished(self, reply):
		headers = reply.rawHeaderPairs()
		headers = {str(k):str(v) for k,v in headers}
		content_type = headers.get("Content-Type")
		url = reply.url().toString()
		status = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
		cookies = headers.get("Set-Cookie")
		logger.log('{} --- {} --- {}'.format(str(status), url, content_type), 2)