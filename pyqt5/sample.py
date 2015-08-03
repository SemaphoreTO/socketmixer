import sys, numpy as np
from numpy import linalg

root = '/Users/bge/socketmixer'
sys.path.append(root)
sys.path.append(root + '/extensionController')
sys.path.append(root + '/meshController')
sys.path.append(root + '/meshController/mm')
sys.path.append(root + '/meshController/pythonApi')
sys.path.append(root + '/extensions')

from extensionController import *
import MeshWrapper
from connector import *
from orientedBoundingBox import *
from extraFunctions import *

from PyQt5.QtWidgets import (
	QApplication, QWidget, QAction, qApp, QMainWindow, QTextEdit,
	QTabWidget, QStackedWidget,QCommandLinkButton
	)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication, QSize
from PyQt5 import uic, QtCore

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

class Socketmixer(QMainWindow):

	def __init__(self):
		QMainWindow.__init__(self)

		uic.loadUi('socketmixer.ui', self)

		# self.currentIndex = None
		# self.currentWidget = None

		self.step_buttons = {
			'connect': self.stackedWidget,
			self.s1_button: 0,
			self.s2_button: 1,
			self.s3_button: 2,
			self.s4_button: 3, 
			self.s5_button: 4, 
		}

		self.step1_buttons = {
			'connect': self.s1page,
			self.s1_a: 1,
			self.s1_b: 2,
			self.s1_c: 3,
			self.s1_d: 4,
			self.s1_e: 5,
			self.s1_f: 6,
			self.s1_g: 7,
			self.s1_h: 8,
			self.s1_i: 9,
			self.s1_j: 10
		}
		
		self.icons = {
			'arrow_double_left': QIcon('/Users/bge/socketmixer/static/icons/arrow_double_left.png'),
			'zoom_out': QIcon('/Users/bge/socketmixer/static/icons/zoom_out.png'),
			'play': QIcon('/Users/bge/socketmixer/static/icons/play.png'),
			'fullscreen_off': QIcon('/Users/bge/socketmixer/static/icons/fullscreen_off.png'),
			'thumbs': QIcon('/Users/bge/socketmixer/static/icons/thumbs.png')
		}

		self.actionScanning.setIcon(self.icons['zoom_out'])
		self.actionModeling.setIcon(self.icons['play'])
		self.actionPrinting.setIcon(self.icons['fullscreen_off'])
		self.actionExit.setIcon(self.icons['arrow_double_left'])
		self.actionContact.setIcon(self.icons['thumbs'])

		self.s1_button.clicked.connect(self.setStep1Page)
		self.s2_button.clicked.connect(self.setStep2Page)
		self.s3_button.clicked.connect(self.setStep3Page)
		self.s4_button.clicked.connect(self.setStep4Page)
		self.s5_button.clicked.connect(self.setStep5Page)

		self.s1_a.clicked.connect(self.setStep1PageA)
		self.s1_b.clicked.connect(self.setStep1PageB)
		self.s1_c.clicked.connect(self.setStep1PageC)
		self.s1_d.clicked.connect(self.setStep1PageD)
		self.s1_e.clicked.connect(self.setStep1PageE)
		self.s1_f.clicked.connect(self.setStep1PageF)
		self.s1_g.clicked.connect(self.setStep1PageG)
		self.s1_h.clicked.connect(self.setStep1PageH)
		self.s1_i.clicked.connect(self.setStep1PageI)
		self.s1_j.clicked.connect(self.setStep1PageJ)

		self.s1_p6_label_remesh.setStyleSheet('background-color: None; border: 0px')
		self.s1_p6_label_smooth.setStyleSheet('background-color: None; border: 0px')

		self.s1_p1_button_importFile.clicked.connect(self.importFile)
		self.s1_p2_button_planeCut.clicked.connect(self.planeCut)
		self.s1_p2_button_planeCut_accept.clicked.connect(self.acceptPlaneCut)
		self.s1_p3_button_selectResidual.clicked.connect(self.selectResidual)
		self.s1_p3_button_selectResidual_accept.clicked.connect(self.accept)
		self.s1_p4_button_invert.clicked.connect(self.invertTool)
		self.s1_p4_button_discard.clicked.connect(self.discard)
		self.s1_p4_button_discard_accept.clicked.connect(self.accept)
		self.s1_p5_button_inspector.clicked.connect(self.inspector)
		self.s1_p6_button_remesh.clicked.connect(self.remesh)
		self.s1_p6_button_remesh_accept.clicked.connect(self.accept)
		self.s1_p7_button_autoAlign.clicked.connect(self.autoAlign)
		self.s1_p7_button_autoAlign_accept.clicked.connect(self.accept)
		self.s1_p8_button_recenter.clicked.connect(self.recenter)
		self.s1_p8_button_recenter_accept.clicked.connect(self.accept)
		self.s1_p9_button_manualAlign.clicked.connect(self.manualAlign)
		self.s1_p9_button_manualAlign_accept.clicked.connect(self.accept)
		self.s1_p10_button_duplicate.clicked.connect(self.duplicate)

	# def buttonConnect(self, d):
	# 	self.currentWidget = d['connect']
	# 	for button, i in d.items():
	# 		if not (button == 'connect'):
	# 			self.index = i
	# 			print(self.index)
	# 			button.clicked.connect(self.changePages)

	# def changePages(self):

	# 	self.currentWidget.setCurrentIndex(self.currentIndex)

	# ============== API CALLS ==================
	def accept(self):
		accept()
		saveLatest()

	def acceptSelect(self):
		acceptSelect()
		saveLatest()

	def importFile(self):
		MeshWrapper.importFile()

	def planeCut(self):
		planeCut()

	def acceptPlaneCut(self):
		acceptPlaneCut()
		saveLatest()

	def selectResidual(self):
		selectTool(30.2)
		expandToConnected()

	def invertTool(self):
		invertTool()

	def discard(self):
		discard()

	def inspector(self):
		inspector()
		repairAll()

	def remesh(self):
		selectAll()
		remesh(1, self.s1_p6_value_remesh.value())
		remesh(2, self.s1_p6_value_smooth.value())

	def autoAlign(self):
		reOrientModel()

	def recenter(self):
		alignZCam(1)

	def manualAlign(self):
		alignTransform()

	def duplicate(self):
		duplicateAndRenameAndHide('scan', 'rectifiedLimb')

	# =============== PAGE CHANGES ==================

	def unHighlight(self, clickedButton, d):

		for button in d.keys():
			if not (button == 'connect' or button == clickedButton):
				button.setStyleSheet('background-color: None')

	def setStep1Page(self):
		self.stackedWidget.setCurrentIndex(0)
		self.s1page.setCurrentIndex(0)
		self.s1_button.setStyleSheet('background-color: gray; border: 1px solid black')
		self.unHighlight(self.s1_button, self.step_buttons)

	def setStep2Page(self):
		self.stackedWidget.setCurrentIndex(1)
		self.s2_button.setStyleSheet('background-color: gray; border: 1px solid black')
		self.unHighlight(self.s2_button, self.step_buttons)

	def setStep3Page(self):
		self.stackedWidget.setCurrentIndex(2)
		self.s3_button.setStyleSheet('background-color: gray; border: 1px solid black')
		self.unHighlight(self.s3_button, self.step_buttons)

	def setStep4Page(self):
		self.stackedWidget.setCurrentIndex(3)
		self.s4_button.setStyleSheet('background-color: gray; border: 1px solid black')
		self.unHighlight(self.s4_button, self.step_buttons)

	def setStep5Page(self):
		self.stackedWidget.setCurrentIndex(4)
		self.s5_button.setStyleSheet('background-color: gray; border: 1px solid black')
		self.unHighlight(self.s5_button, self.step_buttons)

	def setStep1PageA(self):
		self.s1page.setCurrentIndex(1)
		self.s1_a.setStyleSheet('background-color: gray; border: 1px solid black')
		self.unHighlight(self.s1_a, self.step1_buttons)

	def setStep1PageB(self):
		self.s1page.setCurrentIndex(2)
		self.s1_b.setStyleSheet('background-color: gray; border: 1px solid black')
		self.unHighlight(self.s1_b, self.step1_buttons)

	def setStep1PageC(self):
		self.s1page.setCurrentIndex(3)
		self.s1_c.setStyleSheet('background-color: gray; border: 1px solid black')
		self.unHighlight(self.s1_c, self.step1_buttons)
	
	def setStep1PageD(self):
		self.s1page.setCurrentIndex(4)
		self.s1_d.setStyleSheet('background-color: gray; border: 1px solid black')
		self.unHighlight(self.s1_d, self.step1_buttons)

	def setStep1PageE(self):
		self.s1page.setCurrentIndex(5)
		self.s1_e.setStyleSheet('background-color: gray; border: 1px solid black')
		self.unHighlight(self.s1_e, self.step1_buttons)
	
	def setStep1PageF(self):
		self.s1page.setCurrentIndex(6)
		self.s1_f.setStyleSheet('background-color: gray; border: 1px solid black')
		self.unHighlight(self.s1_f, self.step1_buttons)

	def setStep1PageG(self):
		self.s1page.setCurrentIndex(7)
		self.s1_g.setStyleSheet('background-color: gray; border: 1px solid black')
		self.unHighlight(self.s1_g, self.step1_buttons)
	
	def setStep1PageH(self):
		self.s1page.setCurrentIndex(8)
		self.s1_h.setStyleSheet('background-color: gray; border: 1px solid black')
		self.unHighlight(self.s1_h, self.step1_buttons)

	def setStep1PageI(self):
		self.s1page.setCurrentIndex(9)
		self.s1_i.setStyleSheet('background-color: gray; border: 1px solid black')
		self.unHighlight(self.s1_i, self.step1_buttons)

	def setStep1PageJ(self):
		self.s1page.setCurrentIndex(10)
		self.s1_j.setStyleSheet('background-color: gray; border: 1px solid black')
		self.unHighlight(self.s1_j, self.step1_buttons)


if __name__ == "__main__":
	app = QApplication(sys.argv)
	main = Socketmixer()
	main.show()
	sys.exit(app.exec_())		

