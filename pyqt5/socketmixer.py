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
#import MeshWrapper
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

BUTTONSTYLEHIGHLIGHT = 'background-color: #5CADFF; border: 1px solid #5CADFF'

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
		
		for i in range(1, 7):
			removeStepModel(i)

		# distance = 0
		# for i in range(self.steps[1][3]):
		# 	this_button = self.addButton(
		# 		BUTTON_X, 
		# 		BUTTON_Y + distance, string.ascii_uppercase[i])
		# 	this_button.clicked.connect(lambda: self.setStep(i + 1, 1, this_button))
		# 	self.step2_buttons.append(this_button)
		# 	distance += 20

		# STEP BUTTONS
		self.s1_button.clicked.connect(lambda: self.setSteps(0, self.s1_button))
		self.s2_button.clicked.connect(lambda: self.setSteps(1, self.s2_button))
		self.s3_button.clicked.connect(lambda: self.setSteps(2, self.s3_button))
		self.s4_button.clicked.connect(lambda: self.setSteps(3, self.s4_button))
		self.s5_button.clicked.connect(lambda: self.setSteps(4, self.s5_button))
		self.s6_button.clicked.connect(lambda: self.setSteps(5, self.s6_button))

		# STEP 1 BUTTONS
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

		# # STEP 2 BUTTONS
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


		# STEP 1B PLANECUT BUTTONS
		s1_mm_actions = {
			self.s1_p0_button_begin: [lambda: self.setStep(1, 0, self.s1_a)],
			self.s1_p1_button_importFile: [self.importFile],
			self.s1_p2_button_planeCut: [self.planeCut],
			self.s1_p2_button_planeCut_accept: [self.accept, lambda: self.setStep(3, 0, self.s1_c)],
			self.s1_p2_button_planeCut_cancel: [self.cancel],
			self.s1_p3_button_selectResidual: [lambda: selectToolSymmetry(30.2)],
			self.s1_p3_button_selectResidual_accept: [self.expandToConnected, lambda: self.setStep(4, 0, self.s1_d)],
			self.s1_p3_button_selectResidual_cancel: [lambda: selectToolSymmetry(30.2)],
			self.s1_p4_button_invert: [self.invertTool],
			self.s1_p4_button_discard: [self.discard],
			self.s1_p4_button_discard_accept: [self.accept, lambda: self.setStep(5, 0, self.s1_e)],
			self.s1_p5_button_inspector: [self.inspector, self.repairAll],
			self.s1_p5_button_accept: [lambda: self.setStep(6, 0, self.s1_f)],
			self.s1_p6_button_remesh: [self.selectAll, lambda: self.remesh(1, self.s1_p6_value_remesh.value()), lambda: self.remesh(2, self.s1_p6_value_smooth.value())],
			self.s1_p6_button_remesh_accept: [self.accept, lambda: self.setStep(7, 0, self.s1_g), self.cancel],
			self.s1_p6_button_remesh_cancel: [self.cancel],
			self.s1_p7_button_autoAlign: [self.exportTempModel, self.reOrientModel],
			self.s1_p7_button_autoAlign_accept: [self.accept, lambda: self.setStep(8, 0, self.s1_h)],
			self.s1_p7_button_autoAlign_cancel: [self.cancel],
			self.s1_p8_button_recenter: [lambda: alignZCam(1), lambda: self.setStep(9, 0, self.s1_i)],
			self.s1_p9_button_manualAlign: [self.alignTransform],
			self.s1_p9_button_manualAlign_accept: [self.accept, lambda: self.setStep(10, 0, self.s1_j)],
			self.s1_p9_button_manualAlign_cancel: [self.cancel],
			self.s1_p10_button_duplicate: [self.exportTempModel, lambda: self.duplicateAndRenameAndHide(SCAN_NAME, 'rectifiedLimb')],
			self.s1_p10_button_accept: [lambda: exportStepModel(1), lambda: self.setStep(0, 1, self.s2_button)]
		}

		# for button, functions in s1_mm_actions.items():
		# 	self.setAction(button, functions)

		s2_mm_actions = {
			self.s2_p0_button_begin: [lambda: self.setStep(1, 1, self.s2_a)],
			self.s2_p1_button_brushSize: [	lambda: self.selectToolSymmetry(self.s2_p1_value_brushSize.value())],
			self.s2_p1_button_accept: [lambda: self.setStep(2, 1, self.s2_b)],
			self.s2_p1_button_cancel: [cancel, lambda: self.selectToolSymmetry(self.s2_p1_value_brushSize.value())],
			self.s2_p2_button_smoothBoundary: [self.smoothBoundary],
			self.s2_p2_button_smoothBoundary_accept: [self.accept, lambda: self.setStep(3, 1, self.s2_c)],
			self.s2_p2_button_cancel: [cancel, lambda: self.selectToolSymmetry(self.s2_p1_value_brushSize.value())],
			self.s2_p3_button_generateOffset: [	lambda: self.offsetDistance(
															self.s2_p3_value_distance.value(),
															self.s2_p3_value_isConnected.isChecked()),
												lambda: self.softTransition(self.s2_p3_value_softTransition.value())],
			self.s2_p3_button_generateOffset_accept: [self.accept, lambda: self.setStep(4, 1, self.s2_d)],
			self.s2_p3_button_cancel: [self.cancel, lambda: self.selectToolSymmetry(self.s2_p1_value_brushSize.value())],
			self.s2_p4_button_smooth: [lambda: self.deformSmooth(self.s2_p4_value_smooth.value())],
			self.s2_p4_button_smooth_accept: [self.accept, lambda: self.setStep(5, 1, self.s2_e)],
			self.s2_p5_button_yes: [lambda: self.setStep(2, 1, self.s2_a)],
			self.s2_p5_button_no: [lambda: self.setStep(6, 1, self.s2_f)],
			self.s2_p6_button_clearFaceGroups: [self.selectAll, self.clearAllFaceGroup],
			self.s2_p6_button_clearFaceGroups_accept: [	lambda: self.setStep(0, 2, self.s3_button),
														lambda: self.exportStepModel(2)]
		}

		# for button, functions in s2_mm_actions.items():
		# 	self.setAction(button, functions)

		s3_mm_actions = {
			self.s3_p0_button_begin: [lambda: self.setStep(1, 2, self.s3_a)],
			self.s3_p1_button_brushSize: [lambda: self.selectToolSymmetry(self.s3_p1_value_brushSize.value(), True)],
			self.s3_p1_button_accept: [lambda: self.setStep(2, 2, self.s3_b)],
			self.s3_p1_button_cancel: [self.cancel, lambda: self.selectToolSymmetry(self.s3_p1_value_brushSize.value(), True)],
			self.s3_p2_button_smoothTrimLine: [self.smoothBoundary],
			self.s3_p2_button_cancel: [cancel, lambda: selectToolSymmetry(self.s3_p1_value_brushSize.value(), True)],
			self.s3_p2_button_accept: [self.accept, lambda: self.setStep(3, 2, self.s3_c)],
			self.s3_p3_button_createFaceGroup: [self.createFaceGroup, self.selectToolSymmetry],
			self.s3_p3_button_cancel: [self.selectAll, self.clearAllFaceGroup, self.selectToolSymmetry],
			self.s3_p3_button_accept: [lambda: self.setStep(4, 2, self.s3_d)],
			self.s3_p4_button_selectFaceGroup: [self.selectToolSymmetry],
			self.s3_p4_button_accept: [lambda: self.setStep(5, 2, self.s3_e)],
			self.s3_p4_button_cancel: [self.cancel, self.selectToolSymmetry],
			self.s3_p5_button_expand: [self.expandByOneRing],
			self.s3_p5_button_contract: [self.contractByOneRing],
			self.s3_p5_button_accept: [lambda: self.setStep(6, 2, self.s3_f)],
			self.s3_p6_button_remeshTrimLine: [self.selectAll, self.remeshSpecial],
			self.s3_p6_button_remeshTrimLine_accept: [self.accept, 
										lambda: self.exportStepModel(3),
										lambda: self.setStep(0, 3, self.s4_button)],
			self.s3_p6_button_remeshTrimLine: [self.cancel]

		}

		# for button, functions in s3_mm_actions.items():
		# 	self.setAction(button, functions)

		s4_mm_actions = {
			self.s4_p0_button_begin: [lambda: self.setStep(1, 3, self.s4_a)],
			self.s4_p1_button_selectFacegroup: [self.selectToolSymmetry],
			self.s4_p1_button_accept: [self.accept, lambda: self.setStep(2, 3, self.s4_b)],
			self.s4_p1_button_cancel: [self.cancel, self.selectToolSymmetry],
			self.s4_p2_button_accept: [lambda: self.setStep(3, 3, self.s4_c)],
			self.s4_p3_button_generateOffset: [lambda: self.offsetDistance(self.s4_p2_value_offsetSocket.value())],
			self.s4_p3_button_generateOffset_accept: [self.accept, lambda: self.setStep(4, 3, self.s4_d)],
			self.s4_p3_button_cancel: [self.cancel],
			self.s4_p4_button_separateOffset: [self.separate, lambda: self.renameObjectByName('rectifiedLimb (part)', 'socket')],
			self.s4_p4_button_accept: [self.accept, lambda: self.setStep(5, 3, self.s4_e)],
			self.s4_p5_button_brushSize: [lambda: self.selectToolSymmetry(self.s4_p5_value_brushSize.value())],
			self.s4_p5_button_contract: [self.contractByOneRing],
			self.s4_p5_button_expand: [self.expandByOneRing],
			self.s4_p5_button_smoothBoundary: [self.smoothBoundary],
			self.s4_p5_button_createHoles: [self.discard],
			self.s4_p5_button_accept: [self.accept, lambda: self.setStep(6, 3, self.s4_f)],
			self.s4_p6_button_createRelief: [self.sculptingTools],
			self.s4_p6_button_createRelief_accept: [self.accept, lambda: self.setStep(7, 3, self.s4_g)],
			self.s4_p7_button_selectAll: [self.selectAll],
			self.s4_p7_button_generateOffset: [lambda: self.offsetDistance(self.s4_p7_value_offsetDistance.value())],
			self.s4_p7_button_accept: [self.accept, lambda: self.exportStepModel(4), lambda: self.setStep(0, 4, self.s5_button)]
		}

		# for button, functions in s4_mm_actions.items():
		# 	self.setAction(button, functions)

		s5_mm_actions = {
			self.s5_p0_button_begin: [lambda: self.setStep(1, 4, self.s5_a)],
			self.s5_p1_button_brushSize: [lambda: selectToolSymmetry(self.s5_p1_value_brushSize.value())],
			self.s5_p1_button_contract: [self.contractByOneRing],
			self.s5_p1_button_expand: [self.expandByOneRing],
			self.s5_p1_button_accept: [self.accept, lambda: self.setStep(2, 4, self.s5_b)],
			self.s5_p1_button_cancel: [self.cancel, lambda: selectToolSymmetry(self.s5_p1_value_brushSize.value())],
			self.s5_p2_button_smooth: [lambda: deformSmooth(self.s5_p2_value_smooth.value())],
			self.s5_p2_button_smooth_accept: [self.accept, lambda: self.setStep(3, 4, self.s5_c)],
			self.s5_p2_button_cancel: [self.cancel, lambda: selectToolSymmetry(self.s5_p1_value_brushSize.value())],
			self.s5_p3_button_sculptingTools: [self.sculptingTools],
			self.s5_p3_button_accept: [lambda: self.setStep(4, 4, self.s5_d)],
			self.s5_p4_button_clearFaceGroups: [self.selectAll, self.clearAllFaceGroup],
			self.s5_p4_button_accept: [lambda: self.setStep(5, 4, self.s5_e)],
			self.s5_p5_button_remesh: [self.selectAll, self.remeshSpecial],
			self.s5_p5_button_cancel: [self.cancel],
			self.s5_p5_button_remesh_accept: [self.accept, 
					lambda: self.exportStepModel(5),
					lambda: self.setStep(0, 5, self.s6_button)]
		}

		# for button, functions in s5_mm_actions.items():
		# 	self.setAction(button, functions)

		s6_mm_actions = {
			self.s6_p0_button_begin: [lambda: self.setStep(1, 5, self.s6_a)],
			self.s6_p1_button_selectCoupler: [lambda: self.importConnector(str(self.s6_p1_value_selectCoupler.currentText()))],
			self.s6_p1_button_accept: [lambda: self.setStep(2, 5, self.s6_b)],
			self.s6_p2_button_manualAlign: [self.alignTransform],
			self.s6_p2_button_accept: [self.accept, lambda: self.setStep(3, 5, self.s6_c)],
			self.s6_p2_button_cancel: [self.cancel],
			self.s6_p3_button_selectTool: [self.selectToolSymmetry],
			self.s6_p3_button_accept: [lambda: self.setStep(4, 5, self.s6_d)],
			self.s6_p4_button_alignMountingPoint: [self.cutSocketForConnection],
			self.s6_p4_button_accept: [self.accept, lambda: self.setStep(5, 5, self.s6_e)],
			self.s6_p5_button_joinMountingPoint: [self.joinConnectionToSocket],
			self.s6_p5_button_accept: [self.accept, lambda: self.setStep(6, 5, self.s6_f)],
			self.s6_p6_button_brushSize: [lambda: self.selectToolSymmetry(self.s6_p6_value_brushSize.value())],
			self.s6_p6_button_contract: [self.contractByOneRing],
			self.s6_p6_button_expand: [self.expandByOneRing],
			self.s6_p6_button_smoothJoin: [self.smoothBoundary],
			self.s6_p6_button_accept: [self.accept, lambda: self.setStep(7, 5, self.s6_g)],
			self.s6_p7_a_button_importHoleMaker: [self.importHoleMaker],
			self.s6_p7_b_button_alignBottomView: [lambda: self.alignZCam(5)],
			self.s6_p7_c_button_positionHoleMaker: [self.alignTransform],
			self.s6_p7_c_button_positionHoleMaker_accept: [self.accept],
			self.s6_p7_d_button_createHole: [lambda: self.boolean('socket', 'holemaker')],
			self.s6_p7_d_button_createHole_accept: [self.accept, lambda: self.exportStepModel(6)]

		}

		# for button, functions in s6_mm_actions.items():
		# 	self.setAction(button, functions)

		''' { page number (int): [	page of stackedWidget, 
									ptr to list of step buttons, 
									indicator of completed step (0 incomplete, 1 complete)
								 	dict: {button: [list of functions]}
								 ]
			}
		'''
		self.steps = {
			0 : [self.s1page, self.step1_buttons, 0, s1_mm_actions],
			1 : [self.s2page, self.step2_buttons, 0, s2_mm_actions],
			2 : [self.s3page, self.step3_buttons, 0, s3_mm_actions],
			3 : [self.s4page, self.step4_buttons, 0, s4_mm_actions],
			4 : [self.s5page, self.step5_buttons, 0, s5_mm_actions],
			5 : [self.s6page, self.step6_buttons, 0, s6_mm_actions]
		}

		for actions in self.steps.values():
			for button, functions in actions[3].items():
				self.setAction(button, functions)

		# Load first page
		self.setSteps(0, self.s1_button)

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

	def repairAll(self):
		repairAll()

	def remesh(self, param, value):
		remesh(param, value)		

	def remeshSpecial(self):
		remeshSpecial()

	def selectAll(self):
		selectAll()

	def exportTempModel(self):
		exportTempModel()

	def reOrientModel(self):
		reOrientModel()

	def alignTransform(self):
		alignTransform()

	def duplicateAndRenameAndHide(self, part, rectified):
		duplicateAndRenameAndHide(part, rectified)

	def selectToolSymmetry(self, size=1.3, symmetry=False):
		selectToolSymmetry(size, symmetry)

	def smoothBoundary(self):
		smoothBoundary()

	def offsetDistance(self, distance, connected=False):
		offsetDistance(distance, connected)

	def softTransition(self, soft_value):
		softTransition(soft_value)

	def deformSmooth(self, smooth_value):
		deformSmooth(smooth_value)

	def createFaceGroup(self):
		createFaceGroup()

	def clearAllFaceGroup(self):
		clearAllFaceGroup()

	def expandByOneRing(self):
		expandByOneRing()

	def contractByOneRing(self):
		contractByOneRing()

	def separate(self):
		separate()

	def renameObjectByName(self, p1, p2):
		renameObjectByName(p1, p2)

	def importConnector(self, socketname):
		importConnectorAndPosition('socket.obj')

	def cutSocketForConnection(self):
		cutSocketForConnection()

	def joinConnectionToSocket(self):
		joinConnectionToSocket()

	def importHoleMaker(self):
		importHoleMaker('holemakerv2.obj')

	def alignZCam(self, cam_number):
		alignZCam(cam_number)

	def alignTransform(self):
		alignTransform()

	def boolean(self, p1, p2):
		boolean(p1, p2)

	def sculptingTools(self):
		sculptingTools()

	# =============== PAGE CHANGES ==================

	def unHighlight(self, clickedButton, d):

		i = 0
		gray = False
		while i < len(d): 
			if (d[i] == clickedButton):
				gray = True
			elif not gray: 
				d[i].setStyleSheet('background-color: #CEE6FF; border: 1px solid #CEE6FF')
			elif gray:
				d[i].setStyleSheet('background-color: None')
			i += 1

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


	def setStep(self, index, page, button):
		self.stackedWidget.setCurrentIndex(page)
		self.steps[page][0].setCurrentIndex(index)
		if button:
			button.setStyleSheet(BUTTONSTYLEHIGHLIGHT)
			if button in self.step_buttons:
				self.unHighlight(button, self.step_buttons)
			else:
				self.unHighlight(button, self.steps[page][1])
		if self.steps[page][2] == 0:
			self.steps[page][2] = 1
		else:
			fileName = 'Step ' + str(page + 1) + '.obj'
			importFigure(fileName, 'AutoSave')

	def addButton(self, x, y, text):
		button = QPushButton('Button', self.s2)
		button.setText(text)
		button.setGeometry(x, y, 26, 22)

		return button

	def setAction(self, button, functions):
		''' (QPushButton, [list of functions]) -> None
			Set button to connect to list of functions upon click.
		'''
		for function in functions:
			print(function)
			button.clicked.connect(function)


if __name__ == "__main__":
	app = QApplication(sys.argv)
	main = Socketmixer()
	main.show()
	sys.exit(app.exec_())		

