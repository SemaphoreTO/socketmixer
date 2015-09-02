import sys, numpy as np
from numpy import linalg
import os
import string

root = os.path.normpath(os.getcwd() + os.sep + os.pardir) 
sys.path.append(root)
sys.path.append(root + '/meshController')
sys.path.append(root + '/meshController/mm')
sys.path.append(root + '/meshController/pythonApi')
sys.path.append(root + '/extensions')
sys.path.append(root + '/socket')

from extraFunctions import *
import icons
from mmfunctions import *

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
SUBSTEP_BUTTON_X = 20
SUBSTEP_BUTTON_Y = 50

# PAGE BUTTON INITIAL COORDINATES
STEP_BUTTON_X = 160
STEP_BUTTON_Y = 40

BUTTONSTYLEHIGHLIGHT = 'background-color: #5CADFF; border: 1px solid #5CADFF'

class Socketmixer(QMainWindow):

	def __init__(self):
		QMainWindow.__init__(self)

		uic.loadUi('socketmixer.ui', self)

		exit_action = QAction(QIcon('exit.png'), '&Exit', self)
		exit_action.setShortcut('Ctrl+Q')
		exit_action.setStatusTip('Exit application')
		exit_action.triggered.connect(qApp.quit)

		self.menuBar.setNativeMenuBar(False)

		# ============ BUTTONS =============

		self.step_buttons = [
			self.s1_button, self.s2_button, self.s3_button, 
			self.s4_button, self.s5_button, self.s6_button]
		self.step1_buttons = []
		self.step2_buttons = []
		self.step3_buttons = []
		self.step4_buttons = []
		self.step5_buttons = []
		self.step6_buttons = []
		
		for i in range(1, 7):
			removeStepModel(i)

		# STEP BUTTONS
		self.s1_button.clicked.connect(lambda: self.set_step(0, 0, self.s1_button))
		self.s2_button.clicked.connect(lambda: self.set_step(0, 1, self.s2_button))
		self.s3_button.clicked.connect(lambda: self.set_step(0, 2, self.s3_button))
		self.s4_button.clicked.connect(lambda: self.set_step(0, 3, self.s4_button))
		self.s5_button.clicked.connect(lambda: self.set_step(0, 4, self.s5_button))
		self.s6_button.clicked.connect(lambda: self.set_step(0, 5, self.s6_button))


		# STEP 1B PLANECUT BUTTONS
		s1_mm_actions = {
			self.s1_p0_button_begin: [lambda: self.set_step(1, 0, self.step1_buttons[1])],
			self.s1_p1_button_importFile: [self.importFile],
			self.s1_p2_button_planeCut: [planeCut],
			self.s1_p2_button_planeCut_accept: [accept, lambda: self.set_step(3, 0, self.step1_buttons[3])],
			self.s1_p2_button_planeCut_cancel: [cancel],
			self.s1_p3_button_selectResidual: [lambda: selectToolSymmetry(30.2)],
			self.s1_p3_button_selectResidual_accept: [expandToConnected, lambda: self.set_step(4, 0, self.step1_buttons[4])],
			self.s1_p3_button_selectResidual_cancel: [lambda: selectToolSymmetry(30.2)],
			self.s1_p4_button_invert: [invertTool],
			self.s1_p4_button_discard: [discard],
			self.s1_p4_button_discard_accept: [accept, lambda: self.set_step(5, 0, self.step1_buttons[5])],
			self.s1_p5_button_inspector: [inspector],
			self.s1_p5_button_accept: [lambda: self.set_step(6, 0, self.step1_buttons[6])],
			self.s1_p6_button_remesh: [selectAll, lambda: remesh(1, self.s1_p6_value_remesh.value()), lambda: remesh(2, self.s1_p6_value_smooth.value())],
			self.s1_p6_button_remesh_accept: [accept, lambda: self.set_step(7, 0, self.step1_buttons[7]), cancel],
			self.s1_p6_button_remesh_cancel: [cancel],
			self.s1_p7_button_autoAlign: [exportTempModel, self.reOrientModel],
			self.s1_p7_button_autoAlign_accept: [accept, lambda: self.set_step(8, 0, self.step1_buttons[8])],
			self.s1_p7_button_autoAlign_cancel: [cancel],
			self.s1_p8_button_recenter: [lambda: alignZCam(1), lambda: self.set_step(9, 0, self.step1_buttons[9])],
			self.s1_p9_button_manualAlign: [alignTransform],
			self.s1_p9_button_manualAlign_accept: [accept, lambda: self.set_step(10, 0, self.step1_buttons[10])],
			self.s1_p9_button_manualAlign_cancel: [cancel],
			self.s1_p10_button_duplicate: [exportTempModel, lambda: self.duplicateAndRenameAndHide('rectifiedLimb')],
			self.s1_p10_button_accept: [lambda: exportStepModel(1), lambda: self.set_step(0, 1, self.s2_button)]
		}


		s2_mm_actions = {
			self.s2_p0_button_begin: [lambda: self.set_step(1, 1, self.step2_buttons[1])],
			self.s2_p1_button_brushSize: [	lambda: selectTool(self.s2_p1_value_brushSize.value())],
			self.s2_p1_button_accept: [lambda: self.set_step(2, 1, self.step2_buttons[2])],
			self.s2_p1_button_cancel: [cancel, lambda: selectTool(self.s2_p1_value_brushSize.value())],
			self.s2_p2_button_smoothBoundary: [smoothBoundary],
			self.s2_p2_button_smoothBoundary_accept: [accept, lambda: self.set_step(3, 1, self.step2_buttons[3])],
			self.s2_p2_button_cancel: [cancel, lambda: selectTool(self.s2_p1_value_brushSize.value())],
			self.s2_p3_button_generateOffset: [	lambda: offsetDistance(
															self.s2_p3_value_distance.value(),
															self.s2_p3_value_isConnected.isChecked()),
												lambda: softTransition(self.s2_p3_value_softTransition.value())],
			self.s2_p3_button_generateOffset_accept: [accept, lambda: self.set_step(4, 1, self.step2_buttons[4])],
			self.s2_p3_button_cancel: [cancel, lambda: selectTool(self.s2_p1_value_brushSize.value())],
			self.s2_p4_button_smooth: [lambda: deformSmooth(self.s2_p4_value_smooth.value())],
			self.s2_p4_button_smooth_accept: [accept, lambda: self.set_step(5, 1, self.step2_buttons[5])],
			self.s2_p5_button_yes: [lambda: self.set_step(2, 1, self.step2_buttons[1])],
			self.s2_p5_button_no: [lambda: self.set_step(6, 1, self.step2_buttons[6])],
			self.s2_p6_button_clearFaceGroups: [selectAll, clearAllFaceGroup],
			self.s2_p6_button_clearFaceGroups_accept: [	lambda: self.set_step(0, 2, self.s3_button),
														lambda: exportStepModel(2)]
		}

		s3_mm_actions = {
			self.s3_p0_button_begin: [lambda: self.set_step(1, 2, self.step3_buttons[1])],
			self.s3_p1_button_brushSize: [lambda: selectTool(self.s3_p1_value_brushSize.value(), True)],
			self.s3_p1_button_accept: [lambda: self.set_step(2, 2, self.step3_buttons[2])],
			self.s3_p1_button_cancel: [cancel, lambda: selectTool(self.s3_p1_value_brushSize.value(), True)],
			self.s3_p2_button_smoothTrimLine: [smoothBoundary],
			self.s3_p2_button_cancel: [cancel, lambda: selectToolSymmetry(self.s3_p1_value_brushSize.value(), True)],
			self.s3_p2_button_accept: [accept, lambda: self.set_step(3, 2, self.step3_buttons[3])],
			self.s3_p3_button_createFaceGroup: [createFaceGroup, selectTool],
			self.s3_p3_button_cancel: [selectAll, clearAllFaceGroup, selectTool],
			self.s3_p3_button_accept: [lambda: self.set_step(4, 2, self.step3_buttons[4])],
			self.s3_p4_button_selectFaceGroup: [selectTool],
			self.s3_p4_button_accept: [lambda: self.set_step(5, 2, self.step3_buttons[5])],
			self.s3_p4_button_cancel: [cancel, selectTool],
			self.s3_p5_button_expand: [expandByOneRing],
			self.s3_p5_button_contract: [contractByOneRing],
			self.s3_p5_button_accept: [lambda: self.set_step(6, 2, self.step3_buttons[6])],
			self.s3_p6_button_remeshTrimLine: [selectAll, remeshSpecial],
			self.s3_p6_button_remeshTrimLine_accept: [accept, 
										lambda: exportStepModel(3),
										lambda: self.set_step(0, 3, self.s4_button)],
			self.s3_p6_button_remeshTrimLine: [cancel]

		}

		s4_mm_actions = {
			self.s4_p0_button_begin: [lambda: self.set_step(1, 3, self.step4_buttons[1])],
			self.s4_p1_button_selectFacegroup: [selectTool],
			self.s4_p1_button_accept: [accept, lambda: self.set_step(2, 3, self.step4_buttons[2])],
			self.s4_p1_button_cancel: [cancel, selectTool],
			self.s4_p2_button_accept: [lambda: self.set_step(3, 3, self.step4_buttons[3])],
			self.s4_p3_button_generateOffset: [lambda: offsetDistance(self.s4_p2_value_offsetSocket.value())],
			self.s4_p3_button_generateOffset_accept: [accept, lambda: self.set_step(4, 3, self.step4_buttons[4])],
			self.s4_p3_button_cancel: [cancel],
			self.s4_p4_button_separateOffset: [separate, lambda: self.renameObjectByName('rectifiedLimb (part)', 'socket')],
			self.s4_p4_button_accept: [accept, lambda: self.set_step(5, 3, self.step4_buttons[5])],
			self.s4_p5_button_brushSize: [lambda: selectTool(self.s4_p5_value_brushSize.value())],
			self.s4_p5_button_contract: [contractByOneRing],
			self.s4_p5_button_expand: [expandByOneRing],
			self.s4_p5_button_smoothBoundary: [smoothBoundary],
			self.s4_p5_button_createHoles: [discard],
			self.s4_p5_button_accept: [accept, lambda: self.set_step(6, 3, self.step4_buttons[6])],
			self.s4_p6_button_createRelief: [sculptingTools],
			self.s4_p6_button_createRelief_accept: [accept, lambda: self.set_step(7, 3, self.step4_buttons[7])],
			self.s4_p7_button_selectAll: [selectAll],
			self.s4_p7_button_generateOffset: [lambda: offsetDistance(self.s4_p7_value_offsetDistance.value())],
			self.s4_p7_button_accept: [accept, lambda: exportStepModel(4), lambda: self.set_step(0, 4, self.s5_button)]
		}

		s5_mm_actions = {
			self.s5_p0_button_begin: [lambda: self.set_step(1, 4, self.step5_buttons[1])],
			self.s5_p1_button_brushSize: [lambda: selectToolSymmetry(self.s5_p1_value_brushSize.value())],
			self.s5_p1_button_contract: [contractByOneRing],
			self.s5_p1_button_expand: [expandByOneRing],
			self.s5_p1_button_accept: [accept, lambda: self.set_step(2, 4, self.step5_buttons[2])],
			self.s5_p1_button_cancel: [cancel, lambda: selectToolSymmetry(self.s5_p1_value_brushSize.value())],
			self.s5_p2_button_smooth: [lambda: deformSmooth(self.s5_p2_value_smooth.value())],
			self.s5_p2_button_smooth_accept: [accept, lambda: self.set_step(3, 4, self.step5_buttons[3])],
			self.s5_p2_button_cancel: [cancel, lambda: selectToolSymmetry(self.s5_p1_value_brushSize.value())],
			self.s5_p3_button_sculptingTools: [sculptingTools],
			self.s5_p3_button_accept: [lambda: self.set_step(4, 4, self.step5_buttons[4])],
			self.s5_p4_button_clearFaceGroups: [selectAll, clearAllFaceGroup],
			self.s5_p4_button_accept: [lambda: self.set_step(5, 4, self.step5_buttons[5])],
			self.s5_p5_button_remesh: [selectAll, remeshSpecial],
			self.s5_p5_button_cancel: [cancel],
			self.s5_p5_button_remesh_accept: [accept, 
					lambda: exportStepModel(5),
					lambda: self.set_step(0, 5, self.s6_button)]
		}

		s6_mm_actions = {
			self.s6_p0_button_begin: [lambda: self.set_step(1, 5, self.step6_buttons[1])],
			self.s6_p1_button_selectCoupler: [lambda: self.importConnector(str(self.s6_p1_value_selectCoupler.currentText()))],
			self.s6_p1_button_accept: [lambda: self.set_step(2, 5, self.step6_buttons[2])],
			self.s6_p2_button_manualAlign: [alignTransform],
			self.s6_p2_button_accept: [accept, lambda: self.set_step(3, 5, self.step1_buttons[3])],
			self.s6_p2_button_cancel: [cancel],
			self.s6_p3_button_selectTool: [selectTool],
			self.s6_p3_button_accept: [lambda: self.set_step(4, 5, self.step1_buttons[4])],
			self.s6_p4_button_alignMountingPoint: [self.cutSocketForConnection],
			self.s6_p4_button_accept: [accept, lambda: self.set_step(5, 5, self.step1_buttons[5])],
			self.s6_p5_button_joinMountingPoint: [self.joinConnectionToSocket],
			self.s6_p5_button_accept: [accept, lambda: self.set_step(6, 5, self.step1_buttons[6])],
			self.s6_p6_button_brushSize: [lambda: selectTool(self.s6_p6_value_brushSize.value())],
			self.s6_p6_button_contract: [contractByOneRing],
			self.s6_p6_button_expand: [expandByOneRing],
			self.s6_p6_button_smoothJoin: [smoothBoundary],
			self.s6_p6_button_accept: [accept, lambda: self.set_step(7, 5, self.step1_buttons[7])],
			self.s6_p7_a_button_importHoleMaker: [self.importHoleMaker],
			self.s6_p7_b_button_alignBottomView: [lambda: self.alignZCam(5)],
			self.s6_p7_c_button_positionHoleMaker: [alignTransform],
			self.s6_p7_c_button_positionHoleMaker_accept: [accept],
			self.s6_p7_d_button_createHole: [lambda: self.boolean('socket', 'holemaker')],
			self.s6_p7_d_button_createHole_accept: [accept, lambda: exportStepModel(6)]

		}

		''' { page number (int): [	page of stackedWidget, 
									ptr to list of step buttons, 
									indicator of completed step (0 incomplete, 1 complete)
								 	dict: {button: [list of functions]}
								 ]
			}
		'''
		self.steps = {
			0 : [self.s1page, self.step1_buttons, 0, s1_mm_actions, 10, self.s1],
			1 : [self.s2page, self.step2_buttons, 0, s2_mm_actions, 6, self.s2],
			2 : [self.s3page, self.step3_buttons, 0, s3_mm_actions, 6, self.s3],
			3 : [self.s4page, self.step4_buttons, 0, s4_mm_actions, 7, self.s4],
			4 : [self.s5page, self.step5_buttons, 0, s5_mm_actions, 5, self.s5],
			5 : [self.s6page, self.step6_buttons, 0, s6_mm_actions, 7, self.s6]
		}

		self.build_step_buttons()

		self.connect_button_to_actions()

		# Load first page
		self.set_step(0, 0, self.s1_button)


	def connect_button_to_actions(self):

		for actions in self.steps.values():
			for button, functions in actions[3].items():
				self.set_action(button, functions)

	def importFile(self):
		importFile()

	def reOrientModel(self):
		reOrientModel()

	def duplicateAndRenameAndHide(self, rectified):
		duplicateAndRenameAndHide(rectified)

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

	def boolean(self, p1, p2):
		boolean(p1, p2)

	# =============== PAGE CHANGES ==================

	def unhighlight(self, clickedButton, d):

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

	def set_step(self, index, page, button):
		self.stackedWidget.setCurrentIndex(page)
		self.steps[page][0].setCurrentIndex(index)
		if button:
			button.setStyleSheet(BUTTONSTYLEHIGHLIGHT)
			if button in self.step_buttons:
				self.unhighlight(button, self.step_buttons)
			else:
				self.unhighlight(button, self.steps[page][1])
		if self.steps[page][2] == 0:
			self.steps[page][2] = 1
		else:
			fileName = 'Step ' + str(page + 1) + '.obj'
			importFigure(fileName, 'AutoSave')

	def build_step_buttons(self):

		for j in range(len(self.steps)):

			distance = 0
			for i in range(self.steps[j][4]):
				this_button = self.add_button(
					SUBSTEP_BUTTON_X, 
					SUBSTEP_BUTTON_Y + distance, string.ascii_uppercase[i], i, j)
				self.steps[j][1].append(this_button)
				distance += 20

	def add_button(self, x, y, text, i, page):
		button = QPushButton('Button', self.steps[page][5])
		button.setText(text)
		button.setGeometry(x, y, 26, 22)
		button.clicked.connect(lambda: self.set_step(i+1, page, button))

		return button

	def set_action(self, button, functions):
		''' (QPushButton, [list of functions]) -> None
			Set button to connect to list of functions upon click.
		'''
		for function in functions:
			button.clicked.connect(function)



if __name__ == "__main__":
	app = QApplication(sys.argv)
	main = Socketmixer()
	main.show()
	sys.exit(app.exec_())		

