from MeshWrapper import *
from mmapi import  *
from mm import *
import connector
import socket_util
from socket_names import *
import json
from orientedBoundingBox import *
import numpy as np
import math
import os
import numpy.linalg as linalg

########################### File Management CALLS ##############################

@meshWrapper
def exportTempModel():
    cmd  = mmapi.StoredCommands()
    cwd =os.getcwd()
    tmpDirectory = os.path.join(cwd,'tmp')
    if not os.path.exists(tmpDirectory):
        os.makedirs(tmpDirectory)
    fileName = os.path.join(tmpDirectory,'tmp.obj')
    cmd.AppendSceneCommand_ExportMeshFile_CurrentSelection(fileName)
    return cmd
    
    


## use extensionFunction()
def importFile(fileLocation = None,folder=None):
    if fileLocation != None and folder != None:
        currentPath = os.path.join(os.getcwd(), folder,fileLocation)
        if os.path.isfile(currentPath):
            return MeshWrapper.importFigure(currentPath)
        else:
            return false
    else:
        return MeshWrapper.importFile()
def planeCut():
    return MeshWrapper.planecut()

@meshWrapper
def importFigure(fileName):
    cmd  = mmapi.StoredCommands()
    found = False
    if os.path.isdir('history'):
        historyFolder = os.path.join(os.getcwd(),'history')
        for root, dirs, files in os.walk(historyFolder):
            for file in files:
                if file == fileName:
                    fileFullPath = os.path.join(root, file)
                    cmd.AppendSceneCommand_OpenMixFile(fileFullPath);
                    found = True
    if found == True:
        return cmd
    else:
        return None  

def saveStep(stepArray):
    step = 'wizTmp'
    for s in stepArray:
        step = step+ '_'+str(s)
    step = step + '.mix'
    saveLatest(step)

   
def loadStep(stepArray):
    step = 'wizTmp'
    for step in stepArray:
        step = step+ '_'+str(step)
    step = step + '.mix'
    loadLatest(step)

@meshWrapper
def loadLatest(name):
    cmd  = mmapi.StoredCommands()
    currentDir = os.getcwd()
    saveFile = currentDir+name
    if os.path.isfile(saveFile):
        cmd.AppendSceneCommand_OpenMixFile(saveFile)
    return cmd

@meshWrapper
def saveLatest():
    name ='save.mix'
    cmd  = mmapi.StoredCommands()
    currentDir = os.getcwd()
    historyDirectory = 'history'
    if not os.path.exists(historyDirectory):
        os.makedirs(historyDirectory)
    saveFile = os.path.join(currentDir,'history',name)
    cmd.AppendSceneCommand_ExportMixFile(saveFile)
    return cmd

########################### BASIC API CALLS ####################################


@meshWrapper
def remesh(param,paramValue):
    cmd  = mmapi.StoredCommands()
    cmd.AppendBeginToolCommand('remesh')
    if param == 1:
        param = 'density'
    elif param ==2:
        param= 'smooth'
    elif param ==3:
        param = 'normalThreshold'
    else:
        return None
    cmd.AppendToolParameterCommand(param,paramValue) 
    return cmd


@meshWrapper
def smooth(smoothValue):
    cmd  = mmapi.StoredCommands()
    cmd.AppendBeginToolCommand('smooth')
    cmd.AppendToolParameterCommand('smooth',smoothValue) 
    return cmd

@meshWrapper
def createFaceGroup():
    cmd  = mmapi.StoredCommands()
    cmd.AppendBeginToolCommand('createFaceGroup') 
    return cmd


@meshWrapper
def alignTransform():
    cmd  = mmapi.StoredCommands()
    cmd.AppendBeginToolCommand('transform')
    return cmd

@meshWrapper
def selectTool(size=1.3):
    cmd  = mmapi.StoredCommands()
    cmd.AppendBeginToolCommand('select')
    cmd.AppendToolParameterCommand("radiusWorld",size) 
    #cmd  = mmapi.StoredCommands()
    #cmd.AppendSelectCommand_All()
    #cmd.AppendSelectUtilityCommand("invert") 
    return cmd

@meshWrapper
def repairAll():
    cmd  = mmapi.StoredCommands()
    cmd.AppendToolUtilityCommand("repairAll")
    cmd.AppendCompleteToolCommand('accept')
    return cmd

@meshWrapper
def inspector():
    cmd  = mmapi.StoredCommands()
    cmd.AppendCompleteToolCommand("cancel") 
    cmd.AppendBeginToolCommand('inspector') 
    return cmd

@meshWrapper
def selectAll():
    cmd  = mmapi.StoredCommands()
    cmd.AppendSelectCommand_All()
    return cmd

@meshWrapper
def discard():
    cmd  = mmapi.StoredCommands()
    cmd.AppendBeginToolCommand('discard') 
    return cmd

@meshWrapper
def invertTool():
    cmd  = mmapi.StoredCommands()
    cmd.AppendSelectUtilityCommand("invert") 
    return cmd

@meshWrapper
def expandToConnected():
    cmd  = mmapi.StoredCommands()
    cmd.AppendSelectUtilityCommand("expandToConnected") 
    return cmd



@meshWrapper
def cancel():
    cmd  = mmapi.StoredCommands()
    cmd.AppendCompleteToolCommand("cancel") 
    return cmd

@meshWrapper
def fitPrimitive():
    cmd  = mmapi.StoredCommands()
    cmd.AppendBeginToolCommand('fitPrimitive') 
    return cmd

@meshWrapper
def deformSmooth(smoothValue):
     cmd  = mmapi.StoredCommands()
     cmd.AppendBeginToolCommand('smooth') 
     cmd.AppendToolParameterCommand('smooth',smoothValue)
     return cmd


@meshWrapper
def smoothBoundary():
    cmd  = mmapi.StoredCommands()
    cmd.AppendBeginToolCommand('smoothBoundary')
    cmd.AppendCompleteToolCommand('accept') 
    return cmd

@meshWrapper
def accept():
    cmd  = mmapi.StoredCommands()
    cmd.AppendCompleteToolCommand('accept')
    return cmd

#i am to tired to give a shit
@meshWrapper
def acceptSelect():
    cmd  = mmapi.StoredCommands()
    cmd.AppendCompleteToolCommand('accept')
    cmd.AppendSelectCommand_All()
    cmd.AppendSelectUtilityCommand("invert") 
    return cmd

@meshWrapper
def separate():
    cmd  = mmapi.StoredCommands()
    cmd.AppendBeginToolCommand('separate')
    return cmd


@meshWrapper
def offsetDistance(distance,checked=False):
    cmd  = mmapi.StoredCommands()
    cmd.AppendBeginToolCommand('offset')
    cmd.AppendToolParameterCommand('offsetWorld',distance)
    if checked:
        cmd.AppendToolParameterCommand('connected',True)
    return cmd

@meshWrapper
def connected(state):
    cmd  = mmapi.StoredCommands()
    cmd.AppendBeginToolCommand('offset')
    cmd.AppendToolParameterCommand('Connected',state)
    return cmd

@meshWrapper
def softTransition(value):
    cmd  = mmapi.StoredCommands()
    cmd.AppendBeginToolCommand('offset')
    cmd.AppendToolParameterCommand('softenWorld',value)
    return cmd


@meshWrapper
def flattenSmooth():
    cmd  = mmapi.StoredCommands()
    cmd.AppendBeginToolCommand('volumeBrush')
    cmd.AppendToolUtilityCommand('setPrimary','flatten')
    return cmd

@meshWrapper
def bubbleSmooth():
    cmd  = mmapi.StoredCommands()
    cmd.AppendBeginToolCommand('volumeBrush')
    cmd.AppendToolUtilityCommand('setPrimary','bubbleSmooth')
    return cmd




########################### SCENE API CALLS ####################################

def centerModel():
    cwd =os.getcwd()
    tmpDirectory = os.path.join(cwd,'tmp')
    fileName = os.path.join(tmpDirectory,'tmp.obj')
    xAvg,yAvg,zAvg,xRot,zRot,rotationVector = calculateEigenVectors(fileName,0)
    remote = mmRemote()
    remote.connect()
    cmd  = mmapi.StoredCommands( )
    result =  mm.to_scene_xyz(remote,xAvg,yAvg,zAvg)
    xAvg = result[0]
    yAvg = result[1]
    zAvg = result[2]
    cmd.AppendBeginToolCommand('transform')
    cmd.AppendToolParameterCommand('translation',-xAvg,0,-zAvg)
    cmd.AppendCompleteToolCommand('accept')
    remote.runCommand(cmd)
    remote.shutdown()
    os.remove (fileName)
    return True


@meshWrapper
def align():
    cmd  = mmapi.StoredCommands()
    cmd.AppendCompleteToolCommand("cancel") 
    cmd.AppendBeginToolCommand('align')
    
    return cmd



@meshWrapper
def alignZCam(view):
    cmd  = mmapi.StoredCommands()
    divisor = 1.0
    height = 0.7
    eye = vec3f()
    if view == 0:
        eye.x = -10.0/divisor
        eye.y= height
        eye.z = 0
    elif view ==1:
        eye.x = 0.0
        eye.y=  height
        eye.z = 10.0/divisor
    elif view ==2:
        eye.x =0
        eye.y= height
        eye.z =  -10.0/divisor
    elif view ==3:
        eye.x = 10.0
        eye.y= height
        eye.z = 0
    elif view ==4:
        eye.x = 0.0
        eye.y= 1.0
        eye.z = 0
    else:
        eye.x = 0.0
        eye.y=  10.0
        eye.z = 0.0


    target = vec3f()
    target.x = 0.0

    if view == 4:
        target.y= 0.0
    else:
        target.y= height
    target.z = 0

    if view == 4:
        up = vec3f()
        up.x = 1.0
        up.y= 0.0
        up.z = 0.0
    else:
        up = vec3f()
        up.x = 0.0
        up.y= 1.0
        up.z = 0.0
   
 
    cmd.CameraControl_SetSpecificView(eye,target,up)
    return cmd


########################### MESHMIXER OBJECT API CALLS #########################




###HACK## want to sleep, fix later
selectedObjects = None 
def getSelectedObject():
    remote = mmRemote()
    remote.connect()
    selectedObjects = mm.list_selected_objects(remote)
    remote.shutdown()
    jsonreturn =  json.dumps(selectedObjects)
    return jsonreturn

def selectObjects(data):
    if data != None:
        remote = mmRemote()
        remote.connect()
        mm.select_objects(remote,data)
        remote.shutdown()
        return True
    else:
        return False


def reOrientModel():
    cwd =os.getcwd()
    tmpDirectory = os.path.join(cwd,'tmp')
    fileName = os.path.join(tmpDirectory,'tmp.obj')
    xAvg,yAvg,zAvg,xRot,zRot,rotationVector = calculateEigenVectors(fileName,0)

    ## make another 270 degree rotation about y axis
    angle = math.pi/2
    #yRotation = np.matrix([[math.cos(angle), 0,-math.sin(angle)], [0, 1.0,0],[math.sin(angle), 0,math.cos(angle)]])
    xRotation =np.matrix([[1.0, 0,0], [0, m.cos(angle),-m.sin(angle)],[0, m.sin(angle),m.cos(angle)]])
    zRotation =np.matrix([[math.cos(angle), -math.sin(angle),0], [math.sin(angle), math.cos(angle),0],[0, 0,1]]) 

    if xRot:
        rotationVector = np.dot(xRotation,rotationVector)
    elif zRot:
        rotationVector = np.dot(zRotation,rotationVector)
   
    
    rotation =[]
    a=rotationVector.item((0,0))
    b=rotationVector.item((0,1))
    c=rotationVector.item((0,2)) 
    d= rotationVector.item((1,0))
    e =rotationVector.item((1,1))
    f=rotationVector.item((1,2))  
    g=rotationVector.item((2,0))
    h=rotationVector.item((2,1))
    i=rotationVector.item((2,2)) 
    
    remote = mmRemote()
    remote.connect()
    cmd  = mmapi.StoredCommands( )
    result =  mm.to_scene_xyz(remote,xAvg,yAvg,zAvg)
    xAvg = result[0]
    yAvg = result[1]
    zAvg = result[2]
    
    cmd.AppendBeginToolCommand('transform')
    cmd.AppendToolParameterCommand('rotation',a,b,c,d,e,f,g,h,i)

    cmd.AppendToolParameterCommand('translation',-xAvg,-yAvg,-zAvg)
    cmd.AppendCompleteToolCommand('accept')
    remote.runCommand(cmd)
    remote.shutdown()

    os.remove (fileName)
    # delete tmp model

    return True

def deleteObjectByName(name):
    remote = mmRemote()
    remote.connect()
    [state,id]= mm.find_object_by_name(remote,name)
    objects = []
    objects.append(id)
    mm.delete_objects(remote,objects)
    remote.shutdown()


def hideObjectByName(name):
    remote = mmRemote()
    remote.connect()
    try:
        [state,id]= mm.find_object_by_name(remote,name)
        cmd  = mmapi.StoredCommands()
        cmd.AppendSceneCommand_SetHidden(id)
        remote.runCommand(cmd)
        remote.shutdown()
    except:
        remote.shutdown()

def showObjectByName(name):
    remote = mmRemote()
    remote.connect()
    [state,id]= mm.find_object_by_name(remote,name)
    cmd  = mmapi.StoredCommands()
    cmd.AppendSceneCommand_SetVisible(id)
    remote.runCommand(cmd)
    remote.shutdown()


def getAllObjects():
    remote = mmRemote()
    remote.connect()
    try:
        objects= mm.list_objects(remote)
        objectnames= []
        for object in objects:
            name = mm.get_object_name(remote, object)
            objectnames.append(name)
        remote.shutdown()
        # convert to json
        jsonreturn =  json.dumps(objectnames)
        return jsonreturn
    except:
        remote.shutdown()
        return False

def selectObjectByName(objectName):
    remote = mmRemote()
    remote.connect()
    mm.select_object_by_name(remote,objectName)

    remote.shutdown()

def renameObjectByName(origName, newName):
    remote = mmRemote()
    remote.connect()
    try:
        cmd  = mmapi.StoredCommands()
        if  origName == '*' : # this mean everthing
            objects= mm.list_objects(remote)
            for object in objects:
                cmd.AppendSceneCommand_SetObjectName(object,newName)
            remote.runCommand(cmd)
        else:
            [state,id]= mm.find_object_by_name(remote,origName)
        
            cmd.AppendSceneCommand_SetObjectName(id,newName)
            remote.runCommand(cmd)
        remote.shutdown()
        return True
    except:
        remote.shutdown() 
        return False

def duplicate(partToDuplicate):
    remote = mmRemote()
    remote.connect()
    try:
         mm.select_object_by_name(remote,partToDuplicate)
         cmd  = mmapi.StoredCommands()
         cmd.AppendBeginToolCommand('duplicate')
         remote.runCommand(cmd)
         remote.shutdown()
     
         return True
    except:
        remote.shutdown() 
        return False

              

@meshWrapper
def colorView():
    cmd  = mmapi.StoredCommands()
    cmd.ViewControl_SetTriangleColorMode(1)
    
    return cmd


########################### SOCKET BUILDER CODE #########################


# [RMS] start the selection tool
def beginSelection():
    remote = mmRemote()
    remote.connect()
    mm.select_object_by_name(remote, SocketName() )
    mm.begin_tool(remote, "select")
    mm.set_toolparam(remote, "radiusWorld", 25.0)
    remote.shutdown()
    return True


# [RMS] the following three steps implement the three stages of attaching the Connector 
#   to the Socket (first import and position Connector, then plane-cut outer shell of Socket, then Join & Smooth)
#   You could call all three in a row, to fully automate it. With the three separate steps, the user has
#   the option to reposition the connector and cutting plane
def importConnectorAndPosition():
    connector.import_connector(False)
    return True

def cutSocketForConnection():
    connector.connector_plane_cut(False)
    return True

def joinConnectionToSocket():
    connector.connector_join()
    return True

