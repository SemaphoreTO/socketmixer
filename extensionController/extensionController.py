import imp,os
from os import listdir


class extensionController ():
    @staticmethod
    def getAllModuleNames(folder):
        results = []
        sub = [each for each in os.listdir(folder) if each.endswith('.py')]
        for file in sub:
            abc = folder+'/'+file 
            results.append(abc)
        return results
    @staticmethod
    def getModule(pycFile):
        module = imp.load_source(os.path.splitext(pycFile)[0], pycFile)
        return module
    @staticmethod
    def getExtensions(directory):
        if not os.path.isdir(directory):
            return
        modules = []
        results = extensionController.getAllModuleNames(directory)
        for file in results:
            modules.append(extensionController.getModule(file))

        return modules

    
