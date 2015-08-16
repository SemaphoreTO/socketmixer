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

BUTTONSTYLEHIGHLIGHT = 'background-color: gray; border: 1px solid black'

class Socketmixer(QMainWindow):

	def __init__(self):
		QMainWindow.__init__(self)

		uic.loadUi('socketmixer.ui', self)

		self.step_buttons = [
			self.s1_button, self.s2_button, self.s3_button, self.s4_button,
			self.s5_button, self.s6_button
		]

		self.step1_buttons = [
			self.s1_a, self.s1_b, self.s1_c, self.s1_d, self.s1_e, self.s1_f,
			self.s1_g, self.s1_h, self.s1_i, self.s1_j
		]

		self.step2_buttons = [
			self.s2_a, self.s2_b, self.s2_c, self.s2_d, self.s2_e, self.s2_f
		]
		
		self.step3_buttons = [
			self.s3_a, self.s3_b, self.s3_c, self.s3_d, self.s3_e, self.s3_f
		]

		self.step4_buttons = [
			self.s4_a, self.s4_b, self.s4_c, self.s4_d, self.s4_e, self.s4_f,
			self.s4_g
		]

		self.step5_buttons = [
			self.s5_a, self.s5_b, self.s5_c, self.s5_d, self.s5_e
		]

		self.step6_buttons = [
			self.s6_a, self.s6_b, self.s6_c, self.s6_d, self.s6_e, self.s6_f
		]

		self.steps = {
			0 : (self.s1page, self.step1_buttons),
			1 : (self.s2page, self.step2_buttons),
			2 : (self.s3page, self.step3_buttons),
			3 : (self.s4page, self.step4_buttons),
			4 : (self.s5page, self.step5_buttons),
			5 : (self.s6page, self.step6_buttons)
		}
		
		self.icons = {
			'arrow_double_left': QIcon('/Users/bge/socketmixer/static/icons/arrow_double_left.png'),
			'zoom_out': QIcon('/Users/bge/socketmixer/static/icons/zoom_out.png'),
			'zoom_in': QIcon('/Users/bge/socketmixer/static/icons/zoom_in.png'),
			'play': QIcon('/Users/bge/socketmixer/static/icons/play.png'),
			'fullscreen_off': QIcon('/Users/bge/socketmixer/static/icons/fullscreen_off.png'),
			'thumbs': QIcon('/Users/bge/socketmixer/static/icons/thumbs.png')
		}

		self.actionScanning.setIcon(self.icons['zoom_out'])
		self.actionModeling.setIcon(self.icons['play'])
		self.actionPrinting.setIcon(self.icons['fullscreen_off'])
		self.actionExit.setIcon(self.icons['arrow_double_left'])
		self.actionContact.setIcon(self.icons['thumbs'])

		self.s1_button.clicked.connect(lambda: self.setSteps(0, self.s1_button))
		self.s2_button.clicked.connect(lambda: self.setSteps(1, self.s2_button))
		self.s3_button.clicked.connect(lambda: self.setSteps(2, self.s3_button))
		self.s4_button.clicked.connect(lambda: self.setSteps(3, self.s4_button))
		self.s5_button.clicked.connect(lambda: self.setSteps(4, self.s5_button))
		self.s6_button.clicked.connect(lambda: self.setSteps(5, self.s6_button))

		# STEP 1 BUTTONS
		self.s1_a.clicked.connect(lambda: self.setStep(1, self.s1_a, 0))
		self.s1_b.clicked.connect(lambda: self.setStep(2, self.s1_b, 0))
		self.s1_c.clicked.connect(lambda: self.setStep(3, self.s1_c, 0))
		self.s1_d.clicked.connect(lambda: self.setStep(4, self.s1_d, 0))
		self.s1_e.clicked.connect(lambda: self.setStep(5, self.s1_e, 0))
		self.s1_f.clicked.connect(lambda: self.setStep(6, self.s1_f, 0))
		self.s1_g.clicked.connect(lambda: self.setStep(7, self.s1_g, 0))
		self.s1_h.clicked.connect(lambda: self.setStep(8, self.s1_h, 0))
		self.s1_i.clicked.connect(lambda: self.setStep(9, self.s1_i, 0))
		self.s1_j.clicked.connect(lambda: self.setStep(10, self.s1_j, 0))

		# STEP 2 BUTTONS
		self.s2_a.clicked.connect(lambda: self.setStep(1, self.s2_a, 1))
		self.s2_b.clicked.connect(lambda: self.setStep(2, self.s2_b, 1))
		self.s2_c.clicked.connect(lambda: self.setStep(3, self.s2_c, 1))
		self.s2_d.clicked.connect(lambda: self.setStep(4, self.s2_d, 1))
		self.s2_e.clicked.connect(lambda: self.setStep(5, self.s2_e, 1))
		self.s2_f.clicked.connect(lambda: self.setStep(6, self.s2_f, 1))

		# STEP 3 BUTTONS
		self.s3_a.clicked.connect(lambda: self.setStep(1, self.s3_a, 2))
		self.s3_b.clicked.connect(lambda: self.setStep(2, self.s3_b, 2))
		self.s3_c.clicked.connect(lambda: self.setStep(3, self.s3_c, 2))
		self.s3_d.clicked.connect(lambda: self.setStep(4, self.s3_d, 2))
		self.s3_e.clicked.connect(lambda: self.setStep(5, self.s3_e, 2))
		self.s3_f.clicked.connect(lambda: self.setStep(6, self.s3_f, 2))

		# STEP 4 BUTTONS
		self.s4_a.clicked.connect(lambda: self.setStep(1, self.s4_a, 3))
		self.s4_b.clicked.connect(lambda: self.setStep(2, self.s4_b, 3))
		self.s4_c.clicked.connect(lambda: self.setStep(3, self.s4_c, 3))
		self.s4_d.clicked.connect(lambda: self.setStep(4, self.s4_d, 3))
		self.s4_e.clicked.connect(lambda: self.setStep(5, self.s4_e, 3))
		self.s4_f.clicked.connect(lambda: self.setStep(6, self.s4_f, 3))
		self.s4_g.clicked.connect(lambda: self.setStep(7, self.s4_g, 3))

		# STEP 5 BUTTONS
		self.s5_a.clicked.connect(lambda: self.setStep(1, self.s5_a, 4))
		self.s5_b.clicked.connect(lambda: self.setStep(2, self.s5_b, 4))
		self.s5_c.clicked.connect(lambda: self.setStep(3, self.s5_c, 4))
		self.s5_d.clicked.connect(lambda: self.setStep(4, self.s5_d, 4))
		self.s5_e.clicked.connect(lambda: self.setStep(5, self.s5_e, 4))

		# STEP 6 BUTTONS
		self.s6_a.clicked.connect(lambda: self.setStep(1, self.s6_a, 5))
		self.s6_b.clicked.connect(lambda: self.setStep(2, self.s6_b, 5))
		self.s6_c.clicked.connect(lambda: self.setStep(3, self.s6_c, 5))
		self.s6_d.clicked.connect(lambda: self.setStep(4, self.s6_d, 5))
		self.s6_e.clicked.connect(lambda: self.setStep(5, self.s6_e, 5))
		self.s6_f.clicked.connect(lambda: self.setStep(6, self.s6_f, 5))

		self.s1_p1_button_importFile.clicked.connect(self.importFile)
		self.s1_p2_button_planeCut.clicked.connect(self.planeCut)
		self.s1_p2_button_planeCut_accept.clicked.connect(self.acceptPlaneCut)
		self.s1_p2_button_planeCut_cancel.clicked.connect(self.cancel)
		self.s1_p3_button_selectResidual.clicked.connect(lambda: self.selectTool(30.2))
		self.s1_p3_button_selectResidual_accept.clicked.connect(self.expandToConnected)
		self.s1_p4_button_invert.clicked.connect(self.invertTool)
		self.s1_p4_button_discard.clicked.connect(self.discard)
		self.s1_p4_button_discard_accept.clicked.connect(self.accept)
		self.s1_p5_button_inspector.clicked.connect(self.inspector)
		self.s1_p6_button_remesh.clicked.connect(self.remesh)
		self.s1_p6_button_remesh_accept.clicked.connect(self.accept)
		self.s1_p7_button_autoAlign.clicked.connect(self.autoAlign)
		self.s1_p7_button_autoAlign_accept.clicked.connect(self.accept)
		self.s1_p8_button_recenter.clicked.connect(self.recenter)
		self.s1_p9_button_manualAlign.clicked.connect(self.manualAlign)
		self.s1_p9_button_manualAlign_accept.clicked.connect(self.accept)
		self.s1_p10_button_duplicate.clicked.connect(self.duplicate)

		self.s2_p1_button_brushSize.clicked.connect(lambda: self.selectTool(self.s2_p1_value_brushSize.value()))
		self.s2_p2_button_smoothBoundary.clicked.connect(self.smoothBoundary)
		self.s2_p2_button_smoothBoundary_accept.clicked.connect(self.accept)
		self.s2_p3_button_generateOffset.clicked.connect(self.generateOffset)
		self.s2_p3_button_generateOffset_accept.clicked.connect(self.accept)
		self.s2_p4_button_smoothOffset.clicked.connect(self.smoothOffset)
		self.s2_p4_button_smoothOffset_accept.clicked.connect(self.accept)
		self.s2_p5_button_yes.clicked.connect(lambda: self.setStep(1, self.s2_a, 1))
		self.s2_p5_button_no.clicked.connect(lambda: self.setStep(6, self.s2_f, 1))
		self.s2_p6_button_clearFaceGroups.clicked.connect(self.clearFaceGroups)

		self.s3_p1_button_brushSize.clicked.connect(lambda: self.selectTool(self.s3_p1_value_brushSize.value(), True))
		self.s3_p2_button_smoothTrimLine.clicked.connect(self.smoothBoundary)
		self.s3_p3_button_createFaceGroup.clicked.connect(self.createFaceGroup)
		self.s3_p4_button_selectFaceGroup.clicked.connect(self.selectTool)
		self.s3_p5_button_expand.clicked.connect(self.expand)
		self.s3_p5_button_contract.clicked.connect(self.contract)
		self.s3_p6_button_remeshTrimLine.clicked.connect(self.remeshSpecial)
		self.s3_p6_button_remeshTrimLine_accept.clicked.connect(self.accept)

	# ============== API CALLS ==================
	def accept(self):
		accept()
		saveLatest()

	def cancel(self):
		cancel()

	def importFile(self):
		MeshWrapper.importFile()

	def planeCut(self):
		planeCut()

	def acceptPlaneCut(self):
		acceptPlaneCut()
		saveLatest()

	def expandToConnected(self):
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
		exportTempModel()
		reOrientModel()

	def recenter(self):
		alignZCam(1)

	def manualAlign(self):
		alignTransform()

	def duplicate(self):
		exportTempModel()
		duplicateAndRenameAndHide('scan', 'rectifiedLimb')

	def selectTool(self, size=1.3, symmetry=False):
		selectToolSymmetry(size, symmetry)

	def smoothBoundary(self):
		smoothBoundary()

	def generateOffset(self):
		connected = self.s2_p3_value_isConnected.isChecked()
		soft_value = self.s2_p3_value_softTransition.value()
		distance = self.s2_p3_value_distance.value()

		offsetDistance(distance, connected)
		softTransition(soft_value)

	def smoothOffset(self):
		smooth_value = self.s2_p4_value_selectSize.value()
		deformSmooth(smooth_value)

	def createFaceGroup(self):
		createFaceGroup()

	def clearFaceGroups(self):
		selectAll()
		clearAllFaceGroup()

	def expand(self):
		expandByOneRing()

	def contract(self):
		contractByOneRing()

	def remeshSpecial(self):
		remeshSpecial()

	# =============== PAGE CHANGES ==================

	def unHighlight(self, clickedButton, d):

		for button in d:
			if not (button == clickedButton):
				button.setStyleSheet('background-color: None')

	def setSteps(self, index, button):
		self.stackedWidget.setCurrentIndex(index)
		self.s1page.setCurrentIndex(0)
		self.s2page.setCurrentIndex(0)
		self.s3page.setCurrentIndex(0)
		self.s4page.setCurrentIndex(0)
		self.s5page.setCurrentIndex(0)
		self.s6page.setCurrentIndex(0)
		button.setStyleSheet(BUTTONSTYLEHIGHLIGHT)
		self.unHighlight(button, self.step_buttons)

	def setStep(self, index, button, page):
		self.stackedWidget.setCurrentIndex(page)
		self.steps[page][0].setCurrentIndex(index)
		button.setStyleSheet(BUTTONSTYLEHIGHLIGHT)
		self.unHighlight(button, self.steps[page][1])

if __name__ == "__main__":
	app = QApplication(sys.argv)
	main = Socketmixer()
	main.show()
	sys.exit(app.exec_())		

