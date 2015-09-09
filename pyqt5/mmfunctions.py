import os, sys, shutil

from selection import *
from tool import *
from scene import *
from mmapi import *
from mmRemote import *
from orientedBoundingBox import *


def accept(path):
	try:
		remote = mmRemote()
		remote.connect()
		accept_tool(remote)
		saveFile(path)
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
		selection_utility_command(remote, 'expandToConnected')
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

def importFile(fileName):

	try:
		remote = mmRemote()
		remote.connect()
		found = False
		# cwd = os.getcwd()
		# path = os.path.join(cwd, fileName)
		path = str(fileName[0])
		if os.path.exists(path):
			if path[-4:] == '.mix':
				open_mix(remote, path)
			elif path[-4:] == '.obj':
				append_objects_from_file(remote, path)
			else:
				# create new project
				pass
			found = True
		else:
			print('File not found')
		remote.shutdown()
	except:
		remote.shutdown()


def saveFile(path, name=None):
		
	try:
		remote = mmRemote()
		remote.connect()
		if not name:
			name = 'Auto_Save.mix'
		fileName = os.path.join(path, name)
		save_mix(remote, fileName)
		remote.shutdown()
	except:
		remote.shutdown()

def makeDirectory(name=None, overwrite=False):

	if not name:
		name = 'Project'
	cwd = os.getcwd()
	if not os.path.exists(name):
		os.makedirs(name)
	else:
		if overwrite == True:
			shutil.rmtree(name)
			os.makedirs(name)
		else:
			return ''
	path = os.path.join(cwd, name)
	# Clear scene in meshmixer
	clearScene()

	return path

def clearScene():
	try:
		remote = mmRemote()
		remote.connect()

		allobjects = list_objects(remote)
		delete_objects(remote, allobjects)
		remote.shutdown()
	except:
		remote.shutdown()

def exportStepModel(path, step_number):

	try:
		remote = mmRemote()
		remote.connect()
		name = 'Step ' + str(step_number) + '.obj'
		path = os.path.join(path, 'Steps')
		saveFile(path, name)
		remote.shutdown()
	except:
		remote.shutdown()

def exportTempModel(path):

	try:
		remote = mmRemote()
		remote.connect()
		name = 'tmp.obj'
		path = os.path.join(path, 'tmp')
		saveFile(path, name)
		remote.shutdown()
	except:
		remote.shutdown()

def renameObjectByName(orig, new):
	try:
		remote = mmRemote()
		remote.connect()
		if orig == '*':
			objects = list_objects(remote)
			for object in objects:
				set_object_name(remote, object, new)
		else:
			[state, id] = find_object_by_name(remote, orig)
			set_object_name(remote, id, new)
		remote.shutdown()
	except:
		remote.shutdown()

def duplicateRenameHide(new):
	try:
		remote = mmRemote()
		remote.connect()
		objects = list_selected_objects(remote)
		partToDuplicate = get_object_name(remote, objects[0])[:-4]
		begin_tool('duplicate')
		duplicateName = partToDuplicate + '.obj (copy)'
		[state, id] = find_object_by_name(remote, duplicateName)
		set_object_name(remote, id, newName + '.obj')
		[state, id] = find_object_by_name(remote, partToDuplicate + '.obj')
		set_hidden(id)
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

def boolean(obj1, obj2):
	try:
		remote = mmRemote()
		remote.connect()
		[found1, id1] = mm.find_object_by_name(remote, obj1)
		[found2, id2] = mm.find_object_by_name(remote, obj2)
		if found1 and found2:
			mm.select_objects(remote, [id1, id2])
			begin_tool('difference')
		remote.shutdown()
	except:
		remote.shutdown()

def alignZCam(view):

	try:
		remote = mmRemote()
		remote.connect()
		divisor = 1.0
		height = 0.7
		eye = vec3f()
		if view == 0:
			eye.x = -10.0
			eye.y = height
			eye.z = 0
		elif view == 1:
			eye.x = 0.0
			eye.y = height
			eye.z = 10.0
		elif view == 2:
			eye.x = 0
			eye.y = height
			eye.z = 0
		elif view == 4:
			eye.x = 0.0
			eye.y = 10.0
			eye.z = 0
		elif view == 5:
			eye.x = 0.0
			eye.y = -10.0
			eye.z = 0
		else:
			eye.x = 0.0
			eye.y = 10.0
			eye.z = 0.0
		target = vec3f()
		target.x = 0.0
		if view == 4 or view == 5:
			target.y = 0.0
			up = vec3f()
			up.x = 1.0
			up.y = 0.0
			up.z = 0.0
		else:
			target.y = height
			up = vec3f()
			up.x = 0.0
			up.y = 1.0
			up.z = 0.0
		target.z = 0
	 
	 	camera_control_set_specific_view(remote, eye,target,up)
	 	remote.shutdown()
	except:
		remote.shutdown()


