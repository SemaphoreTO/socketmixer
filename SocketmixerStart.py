from bottle import route, run, template,static_file,get,post,request,BaseResponse
import os,sys
from threading import Thread
import time
import webbrowser
import json
import win32ui
import re
import cherrypy
##some imports to make pyinstaller work
import numpy as np
import numpy.linalg as linalg



web = False

if web == False:
    sys.path.append( 'extensionController' )
    sys.path.append( 'meshController' )
    sys.path.append( 'meshController/mm' )
    sys.path.append( os.path.join('meshController','pythonApi') )
    from extensionController import *
    from MeshWrapper import  *
    from connector import *
    from orientedBoundingBox import *

@route('/upload', method='POST')
def do_upload():
    upload = request.files.get('upload')
    wkdir = os.getcwd()
    uploadDir = os.path.join(wkdir,'upload')
    if not os.path.exists(uploadDir):
        os.makedirs(uploadDir)
    
    upload.save(uploadDir,overwrite=True) # appends upload.filename automatically
    return upload.filename

@route('/index')
def hello():
	return  static_file('index.html',root='static')
@route('/boot')
def hello():
	return  static_file('boot.html',root='static')

@route(':path#.+#', name='static')
def static(path):
    
      return static_file(path, root='static')

@post('/api/<function>') # or @route('/login', method='POST')
def importMesh(function):
	return callDynamic(function)

@post('/history/check') # or @route('/login', method='POST')
def checkPast():
    mixFiles = []
    if os.path.isdir(os.path.join(os.getcwd(),'history')):
        for root, dirs, files in os.walk("history"):
            for file in files:
                if file.endswith(".mix"):
                    mixFiles.append(file)
    jsonreturn =  json.dumps(mixFiles)
    print jsonreturn
    return jsonreturn
    

def checkifMeshMixerRunning():
  try:
    win32ui.FindWindow("QWidget", None)
    return True
  except:
    print 'meshmixer isnt open'
    return False
  
def callDynamic(functionCall):
    if not checkifMeshMixerRunning():
      return 'false'
    try:
       index = functionCall.index('(')
       functionName = functionCall[0:index]
       for method in extensions:
           if hasattr(method, functionName):
               call = 'method.'+functionCall
               result = eval(call)
               if result is True:
                   return 'true'
               elif result is False:
                   return 'false'
               else:
                  return result
                          
    except :
        return 'false'

class BrowserOpen(Thread):

    def run(self):
        global myport 
        myport = 1343
        global url
        url = 'http://localhost:' +str(myport)+'/boot'
        webbrowser.open(url,new=1,autoraise=True)
     
def startUp():
    global extensions
    extensions = extensionController.getExtensions('extensions')


browser = BrowserOpen()
browser.start()

if web == False:
    startUp()


print 'Semaphore Socketmixer Controller is now working at' 
print str(url)
print "Please don't close this window"
run(server='cherrypy',host='localhost', quiet=True,port=myport,debug=False)





