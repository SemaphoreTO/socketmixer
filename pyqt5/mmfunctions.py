import os, sys, shutil, math, numpy as np

from selection import *
from tool import *
from scene import *
from mmapi import *
from mmRemote import *
from orientedBoundingBox import *

def accept():
	remote = mmRemote()
	try:
		remote.connect()
		accept_tool(remote)
		# save_mix(remote, path)
		remote.shutdown()
	except:
		remote.shutdown()

def planeCut():

	remote = mmRemote()
	try:
		remote.connect()
		begin_tool(remote, 'planeCut')
		remote.shutdown()
	except:
		remote.shutdown()

def cancel():

	remote = mmRemote()
	try:
		remote.connect()
		cancel_tool(remote)
		remote.shutdown()
	except:
		remote.shutdown()

def selectAll():

	remote = mmRemote()
	try:
		remote.connect()
		select_all(remote)
		remote.shutdown()
	except:
		remote.shutdown()

def inspector():
	remote = mmRemote()
	try:
		remote.connect()
		cancel_tool(remote)
		begin_tool(remote, 'inspector')
		tool_utility_command(remote, 'repairAll')
		accept_tool(remote)
		remote.shutdown()
	except:
		remote.shutdown()

def discard():

	remote = mmRemote()
	try:
		remote.connect()
		begin_tool(remote, 'discard')
		remote.shutdown()
	except:
		remote.shutdown()

def sculptingTools():
	remote = mmRemote()
	try:
		remote.connect()
		begin_tool(remote, 'volumeBrush')
		remote.shutdown()
	except:
		remote.shutdown()

def smoothBoundary():
	remote = mmRemote()
	try:
		remote.connect()
		begin_tool(remote, 'smoothBoundary')
		remote.shutdown()
	except:
		remote.shutdown()

def separate():
	remote = mmRemote()
	try:
		remote.connect()
		begin_tool(remote, 'separate')
		remote.shutdown()
	except:
		remote.shutdown()

def invertTool():
	remote = mmRemote()
	try:
		remote.connect()
		selection_utility_command(remote, 'invert')
		remote.shutdown()
	except:
		remote.shutdown()

def clearAllFaceGroup():
	remote = mmRemote()
	try:
		remote.connect()
		begin_tool(remote, 'clearFaceGroup')
		remote.shutdown()
	except:
		remote.shutdown()

def createFaceGroup():
	remote = mmRemote()
	try:
		remote.connect()
		begin_tool(remote, 'createFaceGroup')
		remote.shutdown()
	except:
		remote.shutdown()

def expandToConnected():
	
	remote = mmRemote()
	try:
		remote.connect()
		selection_utility_command(remote, 'expandToConnected')
		remote.shutdown()
	except:
		remote.shutdown()	

def expandByOneRing():
	remote = mmRemote()
	try:
		remote.connect()
		selection_utility_command(remote, 'expandByOneRing')
		remote.shutdown()
	except:
		remote.shutdown()

def contractByOneRing():
	remote = mmRemote()
	try:
		remote.connect()
		selection_utility_command(remote, 'contractByOneRing')
		remote.shutdown()
	except:
		remote.shutdown()

def offsetDistance(distance, connected=False):

	remote = mmRemote()
	try:
		remote.connect()
		selection_utility_command(remote, 'optimizeBoundary')
		begin_tool(remote, 'offset')
		set_toolparam(remote, 'offsetWorld', distance)
		if checked:
			set_toolparam(remote, 'connected', connected)
		remote.shutdown()
	except:
		remote.shutdown()

def softTransition(soft_value):

	remote = mmRemote()
	try:
		remote.connect()
		selection_utility_command(remote, 'optimizeBoundary')
		begin_tool(remote, 'offset')
		set_toolparam(remote, 'softenWorld', soft_value)
		remote.shutdown()
	except:
		remote.shutdown()

def deformSmooth(smooth_value):

	remote = mmRemote()
	try:
		remote.connect()
		begin_tool(remote, 'smooth')
		set_toolparam(remote, 'smooth', smooth_value)
		remote.shutdown()
	except:
		remote.shutdown()

def selectTool(size=1.3, symmetry=False):
	remote = mmRemote()
	try:
		remote.connect()
		begin_tool(remote, 'select')
		set_toolparam(remote, 'radiusWorld', size)
		set_toolparam(remote, 'symmetry', symmetry)
		remote.shutdown()
	except:
		remote.shutdown()

def remesh(param, value):

	remote = mmRemote()
	try:
		remote.connect()
		begin_tool(remote, 'remesh')
		if param == 1:
			param = 'density'
		elif param == 2:
			param = 'smooth'
		elif param == 3:
			param = 'normalThreshold'
		set_toolparam(remote, param, value)
		remote.shutdown()
	except:
		remote.shutdown()

def remeshSpecial():
	remote = mmRemote()
	try:
		remote.connect()
		begin_tool(remote, 'remesh')
		set_toolparam(remote, 'density', 0.5)
		set_toolparam(remote, 'smooth', 1.0)
		set_toolparam(remote, 'preserveGroups', True)
		accept_tool(remote)
	except:
		remote.shutdown()

def boolean(obj1, obj2):
	remote = mmRemote()
	try:
		remote.connect()
		[found1, id1] = find_object_by_name(remote, obj1)
		[found2, id2] = find_object_by_name(remote, obj2)
		if found1 and found2:
			select_objects(remote, [id1, id2])
			begin_tool(remote, 'difference')
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
			print(orig)
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
		begin_tool(remote, 'duplicate')
		duplicateName = partToDuplicate + '.obj (copy)'
		[state, id] = find_object_by_name(remote, duplicateName)
		set_object_name(remote, id, new + '.obj')
		[state, id] = find_object_by_name(remote, partToDuplicate + '.obj')
		set_hidden(remote, id)
		remote.shutdown()
	except:
		remote.shutdown()

def alignTransform():

	remote = mmRemote()
	try:
		remote.connect()
		begin_tool(remote, 'transform')
		set_toolparam(remote, 'pivotFrameMode', 0)
		remote.shutdown()
	except:
		remote.shutdown()

def alignZCam(view):

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
		eye.z = -10.0
	elif view == 3:
		eye.x = 10.0
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

	up = vec3f()

	if view == 4 or view == 5:
		target.y = 0.0
		up.x = 1.0
		up.y = 0.0
		up.z = 0.0
	else:
		target.y = height
		up.x = 0.0
		up.y = 1.0
		up.z = 0.0
	target.z = 0

	camera_control_set_specific_view(remote, eye, target, up)
	remote.shutdown()

def reOrientModel(path):
    tmpDirectory = os.path.join(path, 'tmp')
    fileName = str(os.path.join(tmpDirectory, 'tmp.obj'))

    xAvg, yAvg, zAvg, xRot, zRot, rotationVector = calculateEigenVectors(fileName, 0)

    ## make another 270 degree rotation about y axis
    angle = math.pi/2
    #yRotation = np.matrix([[math.cos(angle), 0,-math.sin(angle)], [0, 1.0,0],[math.sin(angle), 0,math.cos(angle)]])
    xRotation =np.matrix([[1, 0, 0], [0, m.cos(angle), -m.sin(angle)],[0, m.sin(angle), m.cos(angle)]])
    zRotation =np.matrix([[math.cos(angle), -math.sin(angle), 0], [math.sin(angle), math.cos(angle), 0], [0, 0, 1]]) 

    if xRot:
        rotationVector = np.dot(xRotation, rotationVector)
    elif zRot:
        rotationVector = np.dot(zRotation, rotationVector)
   
    
    rotation =[]
    a = rotationVector.item((0, 0))
    b = rotationVector.item((0, 1))
    c = rotationVector.item((0, 2)) 
    d = rotationVector.item((1, 0))
    e = rotationVector.item((1, 1))
    f = rotationVector.item((1, 2))  
    g = rotationVector.item((2, 0))
    h = rotationVector.item((2, 1))
    i = rotationVector.item((2, 2)) 
    
    remote = mmRemote()
    try:
	    remote.connect()

	    result = to_scene_xyz(remote, xAvg, yAvg, zAvg)
	    xAvg = result[0]
	    yAvg = result[1]
	    zAvg = result[2]
	    #translate from scene to world coordinates
	    result2 = to_scene_xyz(remote, 0, 0, 0)
	    xAvg = xAvg - result2[0]
	    yAvg = yAvg - result2[1]
	    zAvg = zAvg - result2[2]

	    begin_tool(remote, 'transform')
	    set_toolparam(remote, 'rotation', (a, b, c, d, e, f, g, h, i))
	    set_toolparam(remote, 'translation', (-xAvg, -yAvg, -zAvg))
	    remote.shutdown()

    except:
	    remote.shutdown()
    finally:
    	os.remove (fileName)

def exportStepModel(path, step_number):

	try:
		remote = mmRemote()
		remote.connect()
		name = 'Step ' + str(step_number) + '.mix'
		directory = os.path.join(path, 'Steps')
		if not os.path.exists(directory):
			os.makedirs(directory)
		fileName = str(os.path.join(directory, name))
		save_mix(remote, fileName)
		remote.shutdown()
	except:
		remote.shutdown()

def exportTempModel(path):

	try:
		remote = mmRemote()
		remote.connect()
		name = 'tmp.obj'
		directory = os.path.join(path, 'tmp')
		if not os.path.exists(directory):
			os.makedirs(directory)
		fileName = str(os.path.join(directory, name))
		save_current(remote, fileName)
		remote.shutdown()
	except:
		remote.shutdown()

def importFile(fileName):

	try:
		remote = mmRemote()
		remote.connect()
		found = False
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

def getDirectory(name):

	if not os.path.exists(name):
		return ''
	else:
		cwd = os.getcwd()
		path = os.path.join(cwd, name)
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

def saveFile(path, name=None):
		
	try:
		remote = mmRemote()
		remote.connect()
		if not name:
			name = 'Auto_Save.mix'
		fileName = str(os.path.join(path, name))
		save_mix(remote, fileName)
		remote.shutdown()
	except:
		remote.shutdown()