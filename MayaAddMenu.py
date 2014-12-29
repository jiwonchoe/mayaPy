import pymel.core as pm
import pymel.api as api
import os, sys
from PySide import QtGui

import shiboken 



class MayaAddMenu():
    
    def __init__(self):
        
        self.setPath = 'W:/GBK/Set/rig/menu'
    
    def run(self):
        self.fileList()
        self.addMainMenu()
        self.addFolderMenu()
        self.sysAppend(self.dirNameList)


    def getDirList(self, setPath):
        
        dirList = os.walk(setPath).next()[1]
        
        return dirList

    def fileList(self):
        
        self.dirNameList = self.getDirList(self.setPath)
        
        self.dirFile = {}
        
        for x in self.dirNameList:
            self.dirFile[x] =  self.filter(os.walk(self.setPath + '/' + x).next()[2])
        
    def filter(self, objList):
        
        remap = []
        
        for obj in objList:
            if obj.split('.')[-1] == 'py':
                remap.append(obj.split('.')[0])
        
        return remap

    def sysAppend(self, dirList):
        
        for x in dirList:
            sys.path.append(self.setPath + '/' + x)

    def addMainMenu(self):

        if pm.menu('addMenu',q=1,ex=1):
            pm.deleteUI('addMenu')
        
        self.mainMenu = QtGui.QMenu('StudioDot')
        self.mainMenu.setWindowTitle('sdot')
        self.mainMenu.setObjectName('addMenu')
        mayaWinPtr = api.MQtUtil.mainWindow()
        mainWin = shiboken.wrapInstance(long(mayaWinPtr), QtGui.QWidget)

        self.mayaMenuBar = mainWin.findChild(QtGui.QMenuBar, '')
        self.mayaMenuBar.addMenu(self.mainMenu)
    
    def importLib(self, mod):
        im = __import__(mod)
        get = getattr(im, mod)
        get()


    def addFolderMenu(self):
        
        self.itemList = []
        self.command = []
        for y, x in enumerate(self.dirFile.keys()):
            self.itemList.append(QtGui.QMenu(x))
            self.mainMenu.addMenu(self.itemList[y])

            for k in self.dirFile[x]:

                self.itemList[y].addAction(k, pm.Callback(self.importLib,k))



test = MayaAddMenu()
test.run()
