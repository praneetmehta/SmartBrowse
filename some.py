from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtCore import *

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.initUI()

    def initUI(self):
        # self.CentralWidget = QStackedWidget()
        # self.CentralWidget.setFixedHeight(600)
        # self.setCentralWidget(self.CentralWidget)
        # self.Main = Main(self)
        # self.CentralWidget.addWidget(self.Main)
        #Set Current Widgets
        # self.CentralWidget.setCurrentWidget(self.Main)
        #Set Background
        # self.show()

        self.setWindowFlags(Qt.CustomizeWindowHint)
        self.setStyleSheet("QMainWindow { background-color: \
        rgb(0, 0, 0); }")
        self.setGeometry(0, 0, 850, 600)
        self.setWindowTitle("Folder Locker")
        self.Center()

        Font = QFont()
        Font.setPointSize(12)

        TitleBar = QDockWidget()

        Actions = QGroupBox()

        Title = QLabel("Folder Locker")
        Title.setFont(Font)
        Title.setStyleSheet('color: white')
        Title.setAlignment(Qt.AlignCenter)

        Fake = QPushButton()
        Fake.setFixedWidth(25)
        Fake.setFixedHeight(25)
        Fake.setStyleSheet("QPushButton { background-color: \
        rgb(0, 0, 0); }")
        Fake1 = QPushButton()
        Fake1.setFixedWidth(25)
        Fake1.setFixedHeight(25)
        Fake1.setStyleSheet("QPushButton { background-color: \
        rgb(0, 0, 0); }")

        Font = QFont()
        Font.setPointSize(12)

        Font2 = QFont()
        Font2.setPointSize(18)

        Exit = QPushButton("X")
        Exit.setFixedWidth(35)
        Exit.setFixedHeight(25)
        Exit.clicked.connect(self.ExitM)
        Exit.setStyleSheet('QPushButton {background-color: \
        rgb(0, 0, 0); color: grey;}')
        Exit.setFont(Font)

        Minimize = QPushButton("-")
        Minimize.setFixedWidth(25)
        Minimize.setFixedHeight(25)
        Minimize.clicked.connect(self.MinimizeM)
        Minimize.setStyleSheet('QPushButton {background-color: \
        rgb(0, 0, 0); color: grey;}')
        Minimize.setFont(Font2)

        Grid = QGridLayout()

        Grid.addWidget(Fake, 1, 1)
        Grid.addWidget(Fake1, 1, 2)
        Grid.addWidget(Title, 1, 3)
        Grid.addWidget(Exit, 1, 5)
        Grid.addWidget(Minimize, 1, 4)

        Actions.setLayout(Grid)

        TitleBar.setWidget(Actions)
        TitleBar.setFixedHeight(40)
        TitleBar.setFloating(False)
        TitleBar.setTitleBarWidget(QWidget(None))
        TitleBar.setStyleSheet("QGroupBox { background-color: \
        rgb(0, 0, 0); border: 0px solid rgb(0, 0, 0); }")

        self.addDockWidget(Qt.TopDockWidgetArea, TitleBar)
        self.oldPos = self.pos()
        self.show()

    def Center(self):
        self.Resolution = QDesktopWidget().screenGeometry()
        self.move((self.Resolution.width() / 2) - (self.frameSize().width() / 2),
                  (self.Resolution.height() / 2) - (self.frameSize().height() / 2))

    def MinimizeM(self):
        self.showNormal()
        self.showMinimized()

    def ExitM(self):
        sys.exit(0)

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        #print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    app.exec_()


if __name__ == '__main__':
    main()