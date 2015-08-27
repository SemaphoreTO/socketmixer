import sys, numpy as np
from numpy import linalg
import os
import string

root = os.path.normpath(os.getcwd() + os.sep + os.pardir) 
sys.path.append(root)
sys.path.append(root + '/extensionController')
sys.path.append(root + '/meshController')
sys.path.append(root + '/meshController/mm')
sys.path.append(root + '/meshController/pythonApi')
sys.path.append(root + '/extensions')
sys.path.append(root + '/socket')
sys.path.append(root + '/pyqt5/icons')

from extensionController import *
import MeshWrapper
from connector import *
from orientedBoundingBox import *
from extraFunctions import *
import icons

from PyQt5.QtWidgets import (
	QApplication, QWidget, QAction, qApp, QMainWindow, QTextEdit,
	QTabWidget, QStackedWidget,QCommandLinkButton, QPushButton
	)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication, QSize
from PyQt5 import uic, QtCore

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

# SUBSTEP BUTTON INITIAL COORDINATES
BUTTON_X = 20
BUTTON_Y = 50

BUTTONSTYLEHIGHLIGHT = 'background-color: gray; border: 1px solid black'

SCAN_NAME = 'bunnyr'

class Socketmixer(QMainWindow):

	def __init__(self):
		QMainWindow.__init__(self)

		uic.loadUi('socketmixer.ui', self)

		# ============ BUTTONS =============

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
			self.s6_a, self.s6_b, self.s6_c, self.s6_d, self.s6_e, self.s6_f,
			self.s6_g
		]

		self.steps = {
			0 : [self.s1page, self.step1_buttons, 0],
			1 : [self.s2page, self.step2_buttons, 0],
			2 : [self.s3page, self.step3_buttons, 0],
			3 : [self.s4page, self.step4_buttons, 0],
			4 : [self.s5page, self.step5_buttons, 0],
			5 : [self.s6page, self.step6_buttons, 0]
		}
		
		for i in range(1, 7):
			removeStepModel(i)

		# distance = 0
		# for i in range(self.steps[0][3]):
		# 	this_button = self.addButton(
		# 		BUTTON_X, BUTTON_Y + distance, string.ascii_uppercase[i])
		# 	self.step1_buttons.append(this_button)
		# 	distance += 20

		# for i in range(len(self.step1_buttons)):
		# 	self.step1_buttons[i].clicked.connect(
		# 		lambda: self.setStep(i + 1, 0, self.step1_buttons[i]))

		# # STEP 1 BUTTONS
		self.s1_a.clicked.connect(lambda: self.setStep(1, 0, self.s1_a))
		self.s1_b.clicked.connect(lambda: self.setStep(2, 0, self.s1_b))
		self.s1_c.clicked.connect(lambda: self.setStep(3, 0, self.s1_c))
		self.s1_d.clicked.connect(lambda: self.setStep(4, 0, self.s1_d))
		self.s1_e.clicked.connect(lambda: self.setStep(5, 0, self.s1_e))
		self.s1_f.clicked.connect(lambda: self.setStep(6, 0, self.s1_f))
		self.s1_g.clicked.connect(lambda: self.setStep(7, 0, self.s1_g))
		self.s1_h.clicked.connect(lambda: self.setStep(8, 0, self.s1_h))
		self.s1_i.clicked.connect(lambda: self.setStep(9, 0, self.s1_i))
		self.s1_j.clicked.connect(lambda: self.setStep(10, 0, self.s1_j))

		# STEP 2 BUTTONS
		self.s2_a.clicked.connect(lambda: self.setStep(1, 1, self.s2_a))
		self.s2_b.clicked.connect(lambda: self.setStep(2, 1, self.s2_b))
		self.s2_c.clicked.connect(lambda: self.setStep(3, 1, self.s2_c))
		self.s2_d.clicked.connect(lambda: self.setStep(4, 1, self.s2_d))
		self.s2_e.clicked.connect(lambda: self.setStep(5, 1, self.s2_e))
		self.s2_f.clicked.connect(lambda: self.setStep(6, 1, self.s2_f))

		# STEP 3 BUTTONS
		self.s3_a.clicked.connect(lambda: self.setStep(1, 2, self.s3_a))
		self.s3_b.clicked.connect(lambda: self.setStep(2, 2, self.s3_b))
		self.s3_c.clicked.connect(lambda: self.setStep(3, 2, self.s3_c))
		self.s3_d.clicked.connect(lambda: self.setStep(4, 2, self.s3_d))
		self.s3_e.clicked.connect(lambda: self.setStep(5, 2, self.s3_e))
		self.s3_f.clicked.connect(lambda: self.setStep(6, 2, self.s3_f))

		# STEP 4 BUTTONS
		self.s4_a.clicked.connect(lambda: self.setStep(1, 3, self.s4_a))
		self.s4_b.clicked.connect(lambda: self.setStep(2, 3, self.s4_b))
		self.s4_c.clicked.connect(lambda: self.setStep(3, 3, self.s4_c))
		self.s4_d.clicked.connect(lambda: self.setStep(4, 3, self.s4_d))
		self.s4_e.clicked.connect(lambda: self.setStep(5, 3, self.s4_e))
		self.s4_f.clicked.connect(lambda: self.setStep(6, 3, self.s4_f))
		self.s4_g.clicked.connect(lambda: self.setStep(7, 3, self.s4_g))

		# STEP 5 BUTTONS
		self.s5_a.clicked.connect(lambda: self.setStep(1, 4, self.s5_a))
		self.s5_b.clicked.connect(lambda: self.setStep(2, 4, self.s5_b))
		self.s5_c.clicked.connect(lambda: self.setStep(3, 4, self.s5_c))
		self.s5_d.clicked.connect(lambda: self.setStep(4, 4, self.s5_d))
		self.s5_e.clicked.connect(lambda: self.setStep(5, 4, self.s5_e))

		# STEP 6 BUTTONS
		self.s6_a.clicked.connect(lambda: self.setStep(1, 5, self.s6_a))
		self.s6_b.clicked.connect(lambda: self.setStep(2, 5, self.s6_b))
		self.s6_c.clicked.connect(lambda: self.setStep(3, 5, self.s6_c))
		self.s6_d.clicked.connect(lambda: self.setStep(4, 5, self.s6_d))
		self.s6_e.clicked.connect(lambda: self.setStep(5, 5, self.s6_e))
		self.s6_f.clicked.connect(lambda: self.setStep(6, 5, self.s6_f))
		self.s6_g.clicked.connect(lambda: self.setStep(7, 5, self.s6_g))

		self.s1_p1_button_importFile.clicked.connect(self.importFile)
		self.s1_p2_button_planeCut.clicked.connect(self.planeCut)
		self.s1_p2_button_planeCut_accept.clicked.connect(self.accept)
		self.s1_p2_button_planeCut_accept.clicked.connect(
			lambda: self.setStep(3, 0, self.s1_c))
		self.s1_p2_button_planeCut_cancel.clicked.connect(self.cancel)
		self.s1_p3_button_selectResidual.clicked.connect(
			lambda: self.selectTool(30.2))
		self.s1_p3_button_selectResidual_accept.clicked.connect(self.expandToConnected)
		self.s1_p3_button_selectResidual_accept.clicked.connect(
			lambda: self.setStep(4, 0, self.s1_d))
		self.s1_p3_button_selectResidual_cancel.clicked.connect(
			lambda: self.selectTool(30.2))
		self.s1_p4_button_invert.clicked.connect(self.invertTool)
		self.s1_p4_button_discard.clicked.connect(self.discard)
		self.s1_p4_button_discard_accept.clicked.connect(self.accept)
		self.s1_p4_button_discard_accept.clicked.connect(
			lambda: self.setStep(5, 0, self.s1_e))
		self.s1_p5_button_inspector.clicked.connect(self.inspector)
		self.s1_p5_button_inspector.clicked.connect(
			lambda: self.setStep(6, 0, self.s1_f))
		self.s1_p6_button_remesh.clicked.connect(
			lambda: self.remesh(self.s1_p6_value_remesh.value(), 
								self.s1_p6_value_smooth.value()))
		self.s1_p6_button_remesh_accept.clicked.connect(self.accept)
		self.s1_p6_button_remesh_accept.clicked.connect(
			lambda: self.setStep(7, 0, self.s1_g))
		self.s1_p6_button_remesh_cancel.clicked.connect(self.cancel)
		self.s1_p7_button_autoAlign.clicked.connect(self.autoAlign)
		self.s1_p7_button_autoAlign_accept.clicked.connect(self.accept)
		self.s1_p7_button_autoAlign_accept.clicked.connect(
			lambda: self.setStep(8, 0, self.s1_h))
		self.s1_p7_button_autoAlign_cancel.clicked.connect(self.cancel)
		self.s1_p8_button_recenter.clicked.connect(self.recenter)
		self.s1_p9_button_manualAlign.clicked.connect(self.manualAlign)
		self.s1_p9_button_manualAlign_accept.clicked.connect(self.accept)
		self.s1_p9_button_manualAlign_accept.clicked.connect(
			lambda: self.setStep(10, 0, self.s1_j))
		self.s1_p9_button_manualAlign_cancel.clicked.connect(self.cancel)
		self.s1_p10_button_duplicate.clicked.connect(self.duplicate)
		self.s1_p10_button_save.clicked.connect(
			lambda: self.exportStepModel(1))

		self.s2_p1_button_brushSize.clicked.connect(
			lambda: self.selectTool(self.s2_p1_value_brushSize.value()))
		self.s2_p2_button_smoothBoundary.clicked.connect(self.smoothBoundary)
		self.s2_p2_button_smoothBoundary_accept.clicked.connect(self.accept)
		self.s2_p3_button_generateOffset.clicked.connect(
			lambda: self.offset(
						self.s2_p3_value_distance.value(), 
						self.s2_p3_value_softTransition.value(), 
						self.s2_p3_value_isConnected.isChecked()))
		self.s2_p3_button_generateOffset_accept.clicked.connect(self.accept)
		self.s2_p4_button_smooth.clicked.connect(
			lambda: self.smooth(self.s2_p4_value_smooth.value()))
		self.s2_p4_button_smooth_accept.clicked.connect(self.accept)
		self.s2_p5_button_yes.clicked.connect(
			lambda: self.setStep(1, self.s2_a, 1))
		self.s2_p5_button_no.clicked.connect(
			lambda: self.setStep(6, self.s2_f, 1))
		self.s2_p6_button_clearFaceGroups.clicked.connect(self.clearFaceGroups)
		self.s2_p6_button_save.clicked.connect(
			lambda: self.exportStepModel(2))

		self.s3_p1_button_brushSize.clicked.connect(
			lambda: self.selectTool(self.s3_p1_value_brushSize.value(), True))
		self.s3_p2_button_smoothTrimLine.clicked.connect(self.smoothBoundary)
		self.s3_p3_button_createFaceGroup.clicked.connect(self.createFaceGroup)
		self.s3_p4_button_selectFaceGroup.clicked.connect(self.selectTool)
		self.s3_p5_button_expand.clicked.connect(self.expand)
		self.s3_p5_button_contract.clicked.connect(self.contract)
		self.s3_p6_button_remeshTrimLine.clicked.connect(self.remeshSpecial)
		self.s3_p6_button_remeshTrimLine_accept.clicked.connect(self.accept)
		self.s3_p6_button_save.clicked.connect(
			lambda: self.exportStepModel(3))

		self.s4_p1_button_selectFacegroup.clicked.connect(self.selectTool)
		self.s4_p3_button_generateOffset.clicked.connect(
			lambda: self.offset(self.s4_p2_value_offsetSocket.value()))
		self.s4_p3_button_generateOffset_accept.clicked.connect(self.accept)
		self.s4_p4_button_separateOffset.clicked.connect(self.separate)
		self.s4_p5_button_brushSize.clicked.connect(
			lambda: self.selectTool(self.s4_p5_value_brushSize.value()))
		self.s4_p5_button_contract.clicked.connect(self.contract)
		self.s4_p5_button_expand.clicked.connect(self.expand)
		self.s4_p5_button_smoothBoundary.clicked.connect(self.smoothBoundary)
		self.s4_p5_button_createHoles.clicked.connect(self.discard)
		self.s4_p6_button_createRelief.clicked.connect(self.sculptingTools)
		self.s4_p6_button_createRelief_accept.clicked.connect(self.accept)
		self.s4_p7_button_selectAll.clicked.connect(self.selectAll)
		self.s4_p7_button_generateOffset.clicked.connect(
			lambda: self.offset(self.s4_p7_value_offsetDistance.value()))
		self.s4_p7_button_generateOffset_accept.clicked.connect(self.accept)
		self.s4_p7_button_save.clicked.connect(
			lambda: self.exportStepModel(4))

		self.s5_p1_button_brushSize.clicked.connect(
			lambda: self.selectTool(self.s5_p1_value_brushSize.value()))
		self.s5_p1_button_contract.clicked.connect(self.contract)
		self.s5_p1_button_expand.clicked.connect(self.expand)
		self.s5_p2_button_smooth.clicked.connect(
			lambda: self.smooth(self.s5_p2_value_smooth.value()))
		self.s5_p2_button_smooth_accept.clicked.connect(self.accept)
		self.s5_p3_button_sculptingTools.clicked.connect(self.sculptingTools)
		self.s5_p4_button_clearFaceGroups.clicked.connect(self.clearFaceGroups)
		self.s5_p5_button_remesh.clicked.connect(self.remeshSpecial)
		self.s5_p5_button_remesh_accept.clicked.connect(self.accept)
		self.s5_p5_button_save.clicked.connect(
			lambda: self.exportStepModel(5))

		self.s6_p1_button_selectCoupler.clicked.connect(
			lambda: self.importConnector(str(self.s6_p1_value_selectCoupler.currentText())))
		self.s6_p2_button_manualAlign.clicked.connect(self.manualAlign)
		self.s6_p2_button_manualAlign_accept.clicked.connect(self.accept)
		self.s6_p3_button_selectTool.clicked.connect(self.selectTool)
		self.s6_p4_button_alignMountingPoint.clicked.connect(self.cutSocketForConnection)
		self.s6_p5_button_joinMountingPoint.clicked.connect(self.joinConnectionToSocket)
		self.s6_p6_button_brushSize.clicked.connect(
			lambda: self.selectTool(self.s6_p6_value_brushSize.value()))
		self.s6_p6_button_expand.clicked.connect(self.expand)
		self.s6_p6_button_contract.clicked.connect(self.contract)
		self.s6_p6_button_smoothJoin.clicked.connect(self.smoothBoundary)
		self.s6_p7_a_button_importHoleMaker.clicked.connect(self.importHoleMaker)
		self.s6_p7_b_button_alignBottomView.clicked.connect(self.alignZCam)
		self.s6_p7_c_button_positionHoleMaker.clicked.connect(self.alignTransform)
		self.s6_p7_c_button_positionHoleMaker_accept.clicked.connect(self.accept)
		self.s6_p7_d_button_createHole.clicked.connect(self.boolean)
		self.s6_p7_d_button_createHole_accept.clicked.connect(self.accept)
		self.s6_p7_button_save.clicked.connect(
			lambda: self.exportStepModel(6))

		# Load first page
		self.setSteps(0, self.s1_button)

	# ============== API CALLS ==================
	def accept(self):
		accept()
		saveLatest()

	def cancel(self):
		cancel()

	def exportStepModel(self, step_number):
		exportStepModel(step_number)

	def importFile(self):
		MeshWrapper.importFile()

	def planeCut(self):
		planeCut()

	def expandToConnected(self):
		expandToConnected()

	def invertTool(self):
		invertTool()

	def discard(self):
		discard()

	def inspector(self):
		inspector()
		repairAll()

	def remesh(self, remeshvalue, smoothvalue):
		selectAll()
		remesh(1, remeshvalue)
		remesh(2, smoothvalue)

	def remeshSpecial(self):
		selectAll()
		remeshSpecial()

	def selectAll(self):
		selectAll()

	def autoAlign(self):
		exportTempModel()
		reOrientModel()

	def recenter(self):
		alignZCam(1)

	def manualAlign(self):
		alignTransform()

	def duplicate(self):
		exportTempModel()
		duplicateAndRenameAndHide(SCAN_NAME, 'rectifiedLimb')

	def selectTool(self, size=1.3, symmetry=False):
		selectToolSymmetry(size, symmetry)

	def smoothBoundary(self):
		smoothBoundary()

	def selectAll(self):
		selectAll()

	def offset(self, distance, connected=False, soft_value=0):
		offsetDistance(distance, connected)
		softTransition(soft_value)

	def smooth(self, smooth_value):
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

	def separate(self):
		separate()
		renameObjectByName('rectifiedLimb (part)','socket')

	def importConnector(self, socketname):
		print(socketname)
		importConnectorAndPosition('socket.obj')

	def cutSocketForConnection(self):
		cutSocketForConnection()

	def joinConnectionToSocket(self):
		joinConnectionToSocket()

	def importHoleMaker(self):
		importHoleMaker('holemakerv2.obj')

	def alignZCam(self):
		alignZCam(5)

	def alignTransform(self):
		alignTransform()

	def boolean(self):
		boolean('socket', 'holemaker')

	def sculptingTools(self):
		sculptingTools()

	# =============== PAGE CHANGES ==================

	def unHighlight(self, clickedButton, d):

		for button in d:
			if not (button == clickedButton) :
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
		self.unHighlight(button, self.step1_buttons)
		self.unHighlight(button, self.step2_buttons)
		self.unHighlight(button, self.step3_buttons)
		self.unHighlight(button, self.step4_buttons)
		self.unHighlight(button, self.step5_buttons)
		self.unHighlight(button, self.step6_buttons)

	def setStep(self, index, page, button):
		self.stackedWidget.setCurrentIndex(page)
		self.steps[page][0].setCurrentIndex(index)
		if button:
			button.setStyleSheet(BUTTONSTYLEHIGHLIGHT)
			self.unHighlight(button, self.steps[page][1])
		if self.steps[page][2] == 0:
			self.steps[page][2] = 1
		else:
			fileName = 'Step ' + str(page + 1) + '.obj'
			importFigure(fileName, 'AutoSave')

	def addButton(self, x, y, text):
		button = QPushButton('Button', self.stackedWidget)
		button.setText(text)
		button.setGeometry(x, y, 26, 22)

		return button


if __name__ == "__main__":
	app = QApplication(sys.argv)
	main = Socketmixer()
	main.show()
	sys.exit(app.exec_())		

