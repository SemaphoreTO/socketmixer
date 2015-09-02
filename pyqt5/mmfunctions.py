import os, sys

from selection import *
from tool import *
from scene import *
from mmapi import *
from mmRemote import *
from orientedBoundingBox import *


def accept():
	try:
		remote = mmRemote()
		remote.connect()
		accept_tool(remote)
		saveFile(remote)
		remote.shutdown()
	except:
		remote.shutdown()

def cancel():
	try:
		remote = mmRemote()
		remote.connect()
		cancel_tool(remote)
		remote.shutdown()
	except:
		remote.shutdown()

def selectAll():
	try:
		remote = mmRemote()
		remote.connect()
		select_all(remote)
		remote.shutdown()
	except:
		remote.shutdown()

def inspector():
	try:
		remote = mmRemote()
		remote.connect()
		cancel_tool(remote)
		begin_tool(remote, 'inspector')
		tool_utility_command(remote, 'repairAll')
		accept_tool(remote)
		remote.shutdown()
	except:
		remote.shutdown()

def planeCut():
	try:
		remote = mmRemote()
		remote.connect()
		begin_tool(remote, 'planeCut')
		remote.shutdown()
	except:
		remote.shutdown()

def discard():
	try:
		remote = mmRemote()
		remote.connect()
		begin_tool(remote, 'discard')
		remote.shutdown()
	except:
		remote.shutdown()

def sculptingTools():
	try:
		remote = mmRemote()
		remote.connect()
		begin_tool(remote, 'volumeBrush')
		remote.shutdown()
	except:
		remote.shutdown()

def smoothBoundary():
	try:
		remote = mmRemote()
		remote.connect()
		begin_tool(remote, 'smoothBoundary')
		remote.shutdown()
	except:
		remote.shutdown()

def clearAllFaceGroup():
	try:
		remote = mmRemote()
		remote.connect()
		begin_tool(remote, 'clearFaceGroup')
		remote.shutdown()
	except:
		remote.shutdown()

def createFaceGroup():
	try:
		remote = mmRemote()
		remote.connect()
		begin_tool(remote, 'createFaceGroup')
		remote.shutdown()
	except:
		remote.shutdown()

def deformSmooth(value):
	try:
		remote = mmRemote()
		remote.connect()
		begin_tool(remote, 'smooth')
		set_toolparam(remote, 'smooth', value)
		remote.shutdown()
	except:
		remote.shutdown()

def remesh(param, paramvalue):	

	try:
		remote = mmRemote()
		remote.connect()
		begin_tool(remote, 'remesh')
		if param == 1:
			param = 'density'
		elif param == 2:
			param == 'smooth'
		elif param == 3:
			param = 'normalThreshold'
		set_toolparam(remote, param, paramvalue)
		remote.shutdown()
	except:
		remote.shutdown()

def remeshSpecial():
	try:
		remote = mmRemote()
		remote.connect()
		begin_tool(remote, 'remesh')
		set_toolparam(remote, 'density', 0.5)
		set_toolparam(remote, 'smooth', 1.0)
		set_toolparam(remote, 'preserveGroups', True)
		accept_tool(remote)
		remote.shutdown()
	except:
		remote.shutdown()

def separate():
	try:
		remote = mmRemote()
		remote.connect()
		begin_tool(remote, 'separate')
		remote.shutdown()
	except:
		remote.shutdown()

def selectTool(size=1.3, symmetry=False):
	try:
		remote = mmRemote()
		remote.connect()
		begin_tool(remote, 'select')
		set_toolparam(remote, 'radiusWorld', size)
		set_toolparam(remote, 'symmetry', symmetry)
		remote.shutdown()
	except:
		remote.shutdown()

def invertTool():
	try:
		remote = mmRemote()
		remote.connect()
		selection_utility_command(remote, 'invert')
		remote.shutdown()
	except:
		remote.shutdown()

def expandToConnected():
	try:
		remote = mmRemote()
		remote.connect()
		selection_utility_command(remote, 'expandToConected')
		remote.shutdown()
	except:
		remote.shutdown()	

def offsetDistance(distance, checked=False):

	try:
		remote = mmRemote()
		remote.connect()
		selection_utility_command('optimizeBoundary')
		begin_tool('offset')
		set_toolparam('offsetWorld', distance)
		if checked:
			set_toolparam('connected', True)
		remote.shutdown()
	except:
		remote.shutdown()

def softTransition(value):

	try: 
		remote = mmRemote()
		remote.connect()
		selection_utility_command('optimizeBoundary')
		begin_tool('offset')
		set_toolparam('softenWorld', value)
		remote.shutdown()
	except:
		remote.shutdown()

def expandByOneRing():

	try:
		remote = mmRemote()
		remote.connect()
		selection_utility_command('expandByOneRing')
		remote.shutdown()
	except:
		remote.shutdown()

def contractByOneRing():
	try:
		remote = mmRemote()
		remote.connect()
		selection_utility_command('contractByOneRing')
		remote.shutdown()
	except:
		remote.shutdown()


def saveFile(remote, name=None):
	
	if not name:
		name = 'Auto_Save.mix'
	cwd = os.getcwd()
	tmp_dir = 'tmp'
	if not os.path.exists(tmp_dir):
		os.makedirs(tmp_dir)
	path = os.path.join(cwd, tmp_dir, name)
	save_mix(remote, path)


def exportStepModel(step_number):

	try:
		remote = mmRemote()
		remote.connect()
		name = 'Step ' + str(step_number) + '.obj'
		saveFile(remote, name)
		remote.shutdown()
	except:
		remote.shutdown()

def exportTempModel():

	try:
		remote = mmRemote()
		remote.connect()
		name = 'tmp.obj'
		saveFile(remote, name)
		remote.shutdown()
	except:
		remote.shutdown()

def alignTransform():

	try:
		remote = mmRemote()
		remote.connect()
		begin_tool('transform')
		set_toolparam(remote, 'pivotFrameMode', 0)
		remote.shutdown()
	except:
		remote.shutdown()




