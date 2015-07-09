import sys

sys.path.append('/Users/bge/socketmixer')
sys.path.append('/Users/bge/.env/ariane_mail/lib/python3.4/site-packages')

from PyQt5.QtWidgets import (
        QMessageBox, QPushButton, QApplication, QWidget, QDesktopWidget, QAction, qApp, QMainWindow
        )
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication

class Socketmixer(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        # ACTION: Exit
        exitAction = QAction(QIcon('static/icons/arrow_double_left.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit')
        exitAction.triggered.connect(qApp.quit)

        # ACTION: Scanning
        scanning = QAction(QIcon('static/icons/zoom_out.png'), '&Open', self)
        scanning.setShortcut('Ctrl+S')
        scanning.setStatusTip('Scanning')
        scanning.triggered.connect(self.changeFilePath)

        # ACTION: Modeling
        modeling = QAction(QIcon('static/icons/play.png'), '&Open', self)
        modeling.setShortcut('Ctrl+M')
        modeling.setStatusTip('Modeling')
        modeling.triggered.connect(self.changeFilePath)

        # ACTION: Printing
        printing = QAction(QIcon('static/icons/fullscreen_off.png'), '&Open', self)
        printing.setShortcut('Ctrl+P')
        printing.setStatusTip('Printing')
        printing.triggered.connect(self.changeFilePath)

        # FEATURE: Menu Bar
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(scanning)
        fileMenu.addAction(modeling)
        fileMenu.addAction(printing)
        fileMenu.addAction(exitAction)

        # FEATURE: Tool Bar
        self.toolbar = self.addToolBar('Modeling')
        self.toolbar.addAction(exitAction)
        self.toolbar.addAction(scanning)
        self.toolbar.addAction(modeling)
        self.toolbar.addAction(printing)
        
        # FEATURE: Status Bar
        self.statusBar().showMessage('Ready')
        
        # SET UP: window dimensions
        self.resize(600, 400)
        self.setWindowTitle('Socketmixer')
        self.center()
        self.show()

    ''' Center the socketmixer application on the screen. '''
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        
        reply = QMessageBox.question(self,
                'Quit',
                'Are you sure you want to exit?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def changeFilePath(self):
        print('changeFilePath')

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    ex = Socketmixer()
    sys.exit(app.exec_())
