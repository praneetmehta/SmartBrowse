import datetime
import tldextract
import pickle
import os
import re
import operator

class URLValidator:
	def __init__(self):
		self.validator = regex = re.compile(
											r'^(?:http|ftp)s?://' # http:// or https://
											r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
											r'localhost|' # localhost...
											r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ...or ipv4
											r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # ...or ipv6
											r'(?::\d+)?' # optional port
											r'(?:/?|[/?]\S+)$', re.IGNORECASE
											)
	def validate(self, URL):
		return self.validator.search(URL)

class Dump:
	def __init__(self, filepath):
		self.filepath = filepath
		if os.path.isfile(self.filepath):
			with open(self.filepath, 'rb') as file:
				self.Store = pickle.load(file)
		else:
			self.Store = {}
			self.dump()
		self.validator = URLValidator()

	def getDomain(self):
		ext = tldextract.extract(self.url)
		return ext

	def add(self, URL):
		self.url = URL
		if(self.validator.validate(URL)):
			ext = self.getDomain()
			thisTime = datetime.datetime.now()
			if ext.domain in self.Store.keys():
				self.Store[ext.domain].append((URL,thisTime))
			else:
				self.Store[ext.domain] = []
				self.Store[ext.domain].append((URL,thisTime))
			self.notify(URL, ext.domain, thisTime)
		else:
			print('Invalid URL')

	def notify(self, URL, domain, time):
		print('->Domain Name = {}\n->URL = {}\n->Time = {}'.format(domain, URL, time))

	def dump(self):
		with open(self.filepath, 'wb') as file:
			pickle.dump(self.Store, file)


class BookmarkDump(Dump):
	def __init__(self):
		super().__init__('bookmarks.pkl')

	def add(self, URL, title):
		if(self.validator.validate(URL)):
			if URL in self.Store.keys():
				return True
			else:
				self.Store[URL] = title
			self.notify(URL, None, title)
			return True
		else:
			print('Invalid URL')
			return False

class HistoryDump(Dump):
	def __init__(self):
		super().__init__('history.pkl')


class HTMLWriter():
	def __init(self):
		pass

	def historyWriter(self, historyObject):
		self.html = '<title>History</title><h2><strong>History</strong><h2>'
		for key in historyObject:
			self.html += '<h3><strong>'+key.upper()+'</strong></h3><table><tbody>'
			for entry in sorted(historyObject[key], key = operator.itemgetter(1), reverse = True):
				self.html += 	'<tr><td style="padding:3px 25px">{}</td><td style="padding:5px 15px"><a href="{}">{}</a></td></tr>'.format(entry[1], entry[0], entry[0])
			self.html += '</tbody><table><br><hr>'
		return self.html

	def bookmarkWriter(self, bookmarkObject):
		self.html = '<title>Bookmarks</title><h2><strong>Bookmarks</strong><h2>'
		for key in bookmarkObject:
			self.html += '<table><tbody><tr><td style="padding:3px 25px">{}</td><td style="padding:5px 15px"><a href="{}">{}</a></td></tr>'.format(bookmarkObject[key], key, key)
			self.html += '</tbody><table><br><hr>'
		return self.html