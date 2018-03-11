import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from guielements import *
from controlelements import *
from navcontrols import NavControls
from tabBar import TabWidget
from util import HistoryDump, BookmarkDump, HTMLWriter
import atexit

class MainWindow(QWidget):

    def __init__(self, history, bookmarks):
        super().__init__()
        self.history = history
        self.bookmarks = bookmarks
        self.initUI()
        self.initShortcuts()

    def initUI(self):
        self.setGeometry(100, 100, 1280, 720)
        self.setWindowTitle('BITNET v1.0alpha')
        self.create_webprofile()
        self.nav = NavControls(self)
        self.loadProgress = ProgressBar(self)
        self.tabs = TabWidget(self)
        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addStretch()
        hbox.addWidget(self.loadProgress)
        self.nav.operateOn(self.tabs)
        vbox = QVBoxLayout()
        vbox.addLayout(self.nav)
        vbox.addWidget(self.tabs)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.layout().setContentsMargins(0,10,0,0)
        self.showMaximized()

    def create_webprofile(self):
        webprofile = QWebEngineProfile.defaultProfile()
        self.webprofile = webprofile

    def initShortcuts(self):
        newTabShortcut = Shortcut('NewTab', 'Ctrl+T', self.tabs.addNewTab, self)
        closeTabShortcut = Shortcut('Close Tab', 'Ctrl+W', self.tabs.closeTab, self)
        showHistory = Shortcut('History', 'Ctrl+H', self.tabs.showHistory, self)
        showBookmarks = Shortcut('Bookmarks', 'Ctrl+B', self.tabs.showBookmarks, self)

def dumphistory(hist, book):
    hist.dump()
    book.dump()

def main():
    app = QApplication(sys.argv)
    with open('stylesheet', 'r') as file:
        app.setStyleSheet(file.read())
    writer = HTMLWriter()
    history = HistoryDump()
    writer.historyWriter(history.Store)
    bookmarks = BookmarkDump()
    writer.bookmarkWriter(bookmarks.Store)
    w = MainWindow(history, bookmarks)
    p = w.palette()
    p.setColor(w.backgroundRole(), Qt.white)
    w.setPalette(p)
    atexit.register(dumphistory, hist = history, book = bookmarks)
    app.exec_()


if __name__ == '__main__':
    main()