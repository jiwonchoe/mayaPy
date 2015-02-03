# -*- coding: cp949 -*-

import pymel.api as api
import shiboken
from PySide import QtGui, QtCore

def getMayaWindow():  
    accessMainWindow = api.MQtUtil.mainWindow()  
    return shiboken.wrapInstance(long(accessMainWindow), QtGui.QMainWindow)  

class ActViewObjSetAttr(QtGui.QWidget):
    
    def __init__(self, parent=getMayaWindow()):
        
        super(ActViewObjSetAttr, self).__init__(parent)
        
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.setSpacing(0)
        
        font = QtGui.QFont(u'궁서')
        font.setPointSize(16)
        font.setBold(1)
        
        label = QtGui.QLabel(u'\nDAG 노드는 작동하지 않습니다.\n')
        label.setFont(font)
        label.setAlignment(QtCore.Qt.AlignCenter)
        
        self.apiTypeLine = QtGui.QLineEdit('kPluginDependNode')
        self.apiTypeLine.setAlignment(QtCore.Qt.AlignCenter)
        
        self.plugTypeLine = QtGui.QLineEdit('showWholeMesh')
        self.plugTypeLine.setAlignment(QtCore.Qt.AlignCenter)
        
        
        self.valueLine = QtGui.QLineEdit('1')
        self.valueLine.setAlignment(QtCore.Qt.AlignCenter)
        
        getButton = QtGui.QPushButton('Get apiType')
        getButton.clicked.connect(self.setApiType)
        setButton = QtGui.QPushButton('Set Attr')
        setButton.clicked.connect(self.setValue)
        
        mainLayout.addWidget(label)
        mainLayout.addWidget(self.apiTypeLine)
        mainLayout.addWidget(self.plugTypeLine)
        mainLayout.addWidget(self.valueLine)
        mainLayout.addWidget(getButton)
        mainLayout.addWidget(setButton)
        
        self.setLayout(mainLayout)
        self.setObjectName('ActViewSetObjectAttr')
        self.setWindowTitle(u'뷰포트로 제어하는 DG 속성')
        self.setWindowFlags(QtCore.Qt.Window)
        self.show()
        
    
    def fromScreen(self):
        
        api.MGlobal.clearSelectionList()
        activeView = api.M3dView.active3dView()
        api.MGlobal.selectFromScreen(0, 0, activeView.portWidth(), activeView.portHeight(), api.MGlobal.kReplaceList)
        
        self.getObj()
        
        api.MGlobal.clearSelectionList()

    def getObj(self):

        self.objects = api.MSelectionList()
        api.MGlobal.getActiveSelectionList(self.objects)


    def setApiType(self):
        
        self.getObj()
        
        getObject = api.MObject()
        
        self.objects.getDependNode(0, getObject)
        
        self.apiTypeLine.setText(getObject.apiTypeStr())

    def findList(self, dagpath, apiType='kPluginDependNode', plugType='showWholeMesh', value = 1):
        
        dagpath.child(0).apiTypeStr()
        shapeNode = api.MFnDependencyNode(dagpath.child(0))
        shapeNode.name()
        getObj = shapeNode.object()
        
        depG = api.MItDependencyGraph(getObj, api.MItDependencyGraph.kUpstream, api.MItDependencyGraph.kPlugLevel)
        
        while not depG.isDone():
            currentItem = depG.currentItem()
            dependNodeFunc = api.MFnDependencyNode(currentItem)
            if currentItem.apiTypeStr() == apiType:
                dependNodeFunc.findPlug(plugType).setInt(value)
            depG.next()
    
    def setValue(self):
        
        self.fromScreen()
        
        apiType = self.apiTypeLine.text()
        plugType = self.plugTypeLine.text()
        value = int(self.valueLine.text())
        
        
        for x in range(self.objects.length()):
            dagpath = api.MDagPath()
            self.objects.getDagPath(x, dagpath)
            self.findList(dagpath, apiType, plugType, value)
