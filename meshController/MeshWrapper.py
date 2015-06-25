import os,sys

from mmapi import  *
from mmRemote import *
import mm


import Tkinter, tkFileDialog

def meshWrapper(func):
    def inner(*args, **kwargs): #1
        try:
                
            remote = mmRemote()
            remote.connect()
            cmd = func(*args, **kwargs)
            if cmd is None:
                return True 
            remote.runCommand(cmd);
            return True
        except :
            #to do log this
            return False

        finally:
            remote.shutdown();
            
    return inner


class MeshWrapper(object):  
    @staticmethod
    def SingleInstanceApiCommander(operation, modifier, modifierValue):
        try:
            remote = mmRemote()
            remote.connect()
            cmd = mmapi.StoredCommands()
            #some commands don't follow the scheme

            if operation is "open":
                cmd.AppendSceneCommand_AppendMeshFile(modifier);
            elif operation is "invert" or operation is "expandToConnected" :
                cmd.AppendSelectUtilityCommand(operation);
            elif operation is "selectAll":
                 cmd.AppendSelectCommand_All()
            elif operation is "complete":
                cmd.AppendCompleteToolCommand("accept")
            elif operation is "cancel":
                cmd.AppendCompleteToolCommand("cancel")
            
            elif operation is "selectNewPart":
                objects =  mm.list_objects(remote)
                for object in objects:
                    name = mm.get_object_name(remote,object)
                    if "(part)" in name:
                        selectList = []
                        selectList.append(object)
                        mm.select_objects(remote, selectList)
                        return True
                return False
            elif operation is "repairAll":
                cmd.AppendToolUtilityCommand("repairAll")
         
            else:
                cmd.AppendBeginToolCommand(operation)
        
            if modifierValue is not None:
                cmd.AppendToolParameterCommand(modifier,modifierValue)

        
            remote.runCommand(cmd);
            remote.shutdown();
            return True
        except ex:
            #to do log this
            return False
        finally:
            remote.shutdown();
    def __init__(self):
        self.cmd  = mmapi.StoredCommands()

    @staticmethod
    def importFile():

        root = Tkinter.Tk()
        root.withdraw()
        fileName= os.path.normpath(tkFileDialog.askopenfilename(filetypes=[("Obj Files","*.obj")])).encode('ascii','ignore')
        if fileName is not '':
            return MeshWrapper.importFigure(fileName) 
            
        return True
    
    @meshWrapper
    def trial(self):
          cmd  = mmapi.StoredCommands()
          cmd.AppendSelectCommand_All()
          return cmd
    


    @staticmethod
    def selectNewPart():
        return MeshWrapper.SingleInstanceApiCommander("selectNewPart",None,None) 


   
    @staticmethod
    def seperate():
        return MeshWrapper.SingleInstanceApiCommander("separate",None,None) 
    @staticmethod
    def expandToConnected():
        return MeshWrapper.SingleInstanceApiCommander("expandToConnected",None,None) 

    @staticmethod
    def planecut():
        return MeshWrapper.SingleInstanceApiCommander("planeCut",None,None) 

    @staticmethod
    def makeSlice():
        return MeshWrapper.SingleInstanceApiCommander("planeCut",'cutType',1)

    @staticmethod
    def createFaceGroup():
        return MeshWrapper.SingleInstanceApiCommander("createFaceGroup",None,None) 
    @staticmethod
    def align():
        return MeshWrapper.SingleInstanceApiCommander("align",None,None) 
    @staticmethod
    def inspector():
         return MeshWrapper.SingleInstanceApiCommander("inspector",None,None) 
           
    @staticmethod
    def repairAll():
         return MeshWrapper.SingleInstanceApiCommander("repairAll",None,None)  
  

    @staticmethod 
    def cancel():
        return MeshWrapper.SingleInstanceApiCommander("cancel",None,None) 
    @staticmethod 
    def complete():
        return MeshWrapper.SingleInstanceApiCommander("complete",None,None) 
    @staticmethod
    def importFigure(fileLocation):
        return MeshWrapper.SingleInstanceApiCommander("open",fileLocation,None)
    
    @staticmethod
    def smoothBoundary(): 
      return MeshWrapper.SingleInstanceApiCommander("smoothBoundary",None,None)
    @staticmethod
    def selectAll(): 
      return MeshWrapper.SingleInstanceApiCommander("selectAll",None,None)

    @staticmethod
    def wireframe():
        print 'here'

    @staticmethod
    def remesh(value):
       return MeshWrapper.SingleInstanceApiCommander("remesh","smooth",value)

    @staticmethod
    def deformsmooth(value):
       return MeshWrapper.SingleInstanceApiCommander("smooth","scale",value)
     
    @staticmethod
    def roughtselectionforsocket():
        print 'here'
    
    @staticmethod
    def invertSelection():
        return MeshWrapper.SingleInstanceApiCommander("invert",None,None)

    @staticmethod
    def editoffset(value):
        return MeshWrapper.SingleInstanceApiCommander("offset","offsetWorld",value)


    @staticmethod
    def editDiscard():
        return MeshWrapper.SingleInstanceApiCommander("discard",None,None)


    @staticmethod
    def selectleghide():
        print 'here'





 
