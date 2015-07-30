import sys
sys.path.append('/Users/bge/socketmixer')


from PyQt5 import QtCore, QtGui, uic

from PyQt5.QtWidgets import QApplication, QMainWindow

class Socketmixer(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        uic.loadUi('socketmixer.ui', self)

        self.show()

if __name__ == "__main__":

    app = QApplication(sys.argv)
    ex = Socketmixer()
    sys.exit(app.exec_())
