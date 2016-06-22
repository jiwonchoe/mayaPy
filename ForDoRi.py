# Written by jiwon choi

import pymel.api as api
import pymel.core as pm
import shiboken
from PySide import QtGui, QtCore


def getPySideMayaWindow():  

    accessMainWindow = api.MQtUtil.mainWindow()

    return shiboken.wrapInstance(long(accessMainWindow), QtGui.QMainWindow)


class ForDoRi(QtGui.QWidget):
    
    def __init__ (self, parent=getPySideMayaWindow()):
        
        self.closeCheck()
        
        super(ForDoRi, self).__init__(parent)

        mainLayout = QtGui.QVBoxLayout()
        
        self.nodeLineEdit = QtGui.QLineEdit()
        self.completer = QtGui.QCompleter()
        
        self.nodeLineEdit.setCompleter(self.completer)
        self.nodeLineEdit.returnPressed.connect(self.selectNode)
        self.setModelNode()
        
        selectNodeButton = QtGui.QPushButton('select node')
        selectNodeButton.clicked.connect(self.selectNode)
        
        line01 = QtGui.QFrame()
        line01.setFrameShape(QtGui.QFrame.HLine)
        line01.setFrameShadow(QtGui.QFrame.Plain)
        line01.setLineWidth(3)
        
        
        self.weightListWidget = QtGui.QListWidget()
        self.weightListWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        
        getListButton = QtGui.QPushButton('listAttr')
        getListButton.clicked.connect(self.listAttr)
        
        self.setValueLine = QtGui.QLineEdit()
        self.setValueLine.setText('0.0')
        self.setValueLine.setAlignment(QtCore.Qt.AlignCenter)
        self.setValueLine.returnPressed.connect(self.run)
        
        runButton = QtGui.QPushButton('set')
        runButton.clicked.connect(self.run)
        
        mainLayout.addWidget(self.nodeLineEdit)
        mainLayout.addWidget(selectNodeButton)
        mainLayout.addWidget(line01)
        mainLayout.addWidget(getListButton)
        mainLayout.addWidget(self.weightListWidget)
        mainLayout.addWidget(self.setValueLine)
        mainLayout.addWidget(runButton)

        self.setLayout(mainLayout)

        
        self.setWindowTitle('ForDoRi 2016')
        self.setObjectName('ForDoRiUI')
        self.setWindowFlags(QtCore.Qt.Window)
        self.show()

    def setModelNode(self):
        
        slm = QtGui.QStringListModel()
        
        slm.setStringList(pm.allNodeTypes())
        
        self.completer.setModel(slm)

    def selectNode(self):
        
        nodeName = self.nodeLineEdit.text()
        
        if nodeName == '':
            return '1'
        
        if nodeName.find('/') == -1:
            nodeList = pm.ls(type=nodeName)
        else:
            nodeNameS, nodeNameO = nodeName.split('/')
            nodeList = pm.ls(nodeNameO, type=nodeNameS)
        
        if not len(nodeList):
            return '2'
        
        pm.select(nodeList, r=1)

    
    def listAttr(self):
        
        self.objectList = pm.ls(sl=1)
        
        obj = self.objectList[-1]
                
        objAttrList = pm.listAttr(obj, s=1)
        
        self.weightListWidget.clear()
        self.weightListWidget.addItems(objAttrList) 

    def run(self):
        
        items = self.weightListWidget.selectedItems()
        
        attrList = []
        
        pm.undoInfo(ock=1)        
        
        for x in items:
            attrList.append(x.text())
        
        value = float(self.setValueLine.text())
        
        for x in self.objectList:
            for y in attrList:
                x.attr(y).set(value)
        
        pm.undoInfo(cck=1)
        


    def closeEvent(self, evt):

        super(ForDoRi, self).closeEvent(evt)
        self.deleteLater()

    def closeCheck(self):

        for x in QtGui.QApplication.topLevelWidgets():
            try:
                if x.objectName() == 'ForDoRiUI':
                    x.deleteLater()
            except:
                pass
    

test = ForDoRi()
test.show()
