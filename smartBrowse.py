from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout
from PyQt5.QtCore import Qt, QCoreApplication, QPropertyAnimation, QRect
from PyQt5.QtGui import QIcon
from controlelements import Shortcut
from navcontrols import NavControls
from tabBar import TabWidget
from util import HistoryDump, BookmarkDump, HTMLWriter
import atexit
import pyautogui
import sys
from guielements import Button, CompositeWidget

class MainWindow(QWidget):

    def __init__(self, history, bookmarks):
        super().__init__()
        self.history = history
        self.bookmarks = bookmarks
        self.initUI()
        self.initShortcuts()

    def initUI(self):
        self.setGeometry(100, 100, 1280, 720)
        self.setWindowTitle('SmartBrowse v1.0alpha')
        # self.setWindowFlags(Qt.Desktop)
        # self.setWindowFlags(Qt.CustomizeWindowHint)
        # self.setWindowFlags(Qt.FramelessWindowHint)

        # self.create_webprofile()
        self.nav = NavControls(self)
        # self.loadProgress = ProgressBar(self)
        self.tabs = TabWidget(self)
        # hbox = QHBoxLayout()
        # hbox.addStretch()
        # hbox.addStretch()
        # hbox.addWidget(self.loadProgress)
        self.nav.operateOn(self.tabs)
        vbox = QVBoxLayout()
        vbox.addLayout(self.nav)
        vbox.addWidget(self.tabs)
        # vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.layout().setContentsMargins(0,0,0,0)
        # self.setCornerButtons()
        # self.showMaximized()
        self.show()

    def setCornerButtons(self):
        # self.closeButton = ToggleSwitchComposite()
        self.compositeWidgetHolder = CompositeWidget()

        self.minimizeButton = Button(icon = 'img/min.png', parent = self.tabs)
        self.minimizeButton.setStyleSheet("QPushButton{ border : none; margin-bottom:6px; padding:13px 6px 13px 6px;border-radius:0 }")
        self.minimizeButton.clicked.connect(self.showNormal)
        self.compositeWidgetHolder.addWidget(self.minimizeButton)

        self.maxmimizeButton = Button(icon = 'img/max.png', parent = self.tabs)
        self.maxmimizeButton.setStyleSheet("QPushButton{ border : none; margin-bottom:6px; padding:13px 6px 13px 6px; border-radius:0}")
        self.maxmimizeButton.clicked.connect(self.handleMaximize)
        self.compositeWidgetHolder.addWidget(self.maxmimizeButton)

        self.closeButton = Button(icon = 'img/close.png', parent = self.tabs)
        self.closeButton.setStyleSheet("QPushButton{ border : none; margin-bottom:6px; padding:13px 6px 13px 6px; border-radius:0 } QPushButton:hover{ background-color: #ff2121}")
        self.closeButton.clicked.connect(QCoreApplication.quit)
        self.compositeWidgetHolder.addWidget(self.closeButton)

        self.tabs.setCornerWidget(self.compositeWidgetHolder)

    def handleMaximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showNormal()
            self.showMaximized()
    # def create_webprofile(self):
    #     webprofile = QWebEngineProfile.defaultProfile()
    #     self.webprofile = webprofile

    def initShortcuts(self):
        newTabShortcut = Shortcut('NewTab', 'Ctrl+T', self.tabs.addNewTab, self)
        closeTabShortcut = Shortcut('Close Tab', 'Ctrl+W', self.tabs.closeTab, self)
        showHistory = Shortcut('History', 'Ctrl+H', self.tabs.showHistory, self)
        showBookmarks = Shortcut('Bookmarks', 'Ctrl+B', self.tabs.showBookmarks, self)
        reopenTab = Shortcut('Reopen CLosed Tab', 'Ctrl+Shift+T', self.tabs.reopenTab, self)

def dumphistory(hist, book):
    hist.dump()
    book.dump()

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('img/smart.png'))
    with open('public/stylesheet', 'r') as file:
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