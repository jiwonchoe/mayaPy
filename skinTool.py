__author__ = 'jiwon Choe'
# -*- coding: cp949 -*-

from PyQt4 import QtGui, QtCore
import sip, os
import pymel.api as pa  
#import pymel.core as pm
#from functools import partial
import weight as we
reload(we)


def getPyQtMayaWindow():  
    accessMainWindow = pa.MQtUtil.mainWindow()
    return sip.wrapinstance(long(accessMainWindow), QtCore.QObject)  


class skinJsonTool(QtGui.QMainWindow):

    def __init__(self, parent=getPyQtMayaWindow()):

        super(skinJsonTool, self).__init__(parent)

        addWidget = bodyWidget()

        self.setCentralWidget(addWidget)
        self.setWindowTitle('json skinCluster Vertex Weight')


class bodyWidget(QtGui.QWidget):

    def __init__(self, parent=None):

        super(bodyWidget, self).__init__(parent)

        #

        self.myFont = QtGui.QFont('Consolas', 9)

        # layout

        mainLayout = QtGui.QVBoxLayout()
        listLayout = QtGui.QHBoxLayout()
        buttonLayout = QtGui.QHBoxLayout()

        makeJsonLayout = QtGui.QVBoxLayout()
        openJsonLayout = QtGui.QHBoxLayout()

        makeJsonInfoLayout = QtGui.QHBoxLayout()
        makeJsonFileLayout = QtGui.QHBoxLayout()

        # groupbox
        
        toolName = QtGui.QLabel(u'이것은 스무스 스킨 제이슨 툴')
        toolName.setFont(QtGui.QFont(u'궁서', 24))
        
        hangulFont = QtGui.QFont(u'궁서', 9)

        
        jointGroupBox = QtGui.QGroupBox(u'조인트 맞춤')
        jointGroupBox.setFont(hangulFont)
        openJsonGroupBox = QtGui.QGroupBox(u'제이슨 파일 가져오기')
        openJsonGroupBox.setFont(hangulFont)
        jsonGroupBox = QtGui.QGroupBox(u'제이슨 파일 만들기')
        jsonGroupBox.setFont(hangulFont)

        # button & label

        jsonSelectButton = QtGui.QPushButton(u'파일 선택')
        jsonSelectButton.setFont(hangulFont)
        jsonSelectButton.clicked.connect(self.openFile)


        self.openFileNameLine = QtGui.QLineEdit('D:/')
        self.openFileNameLine.setFont(self.myFont)
        openJsonButton = QtGui.QPushButton(u'웨이트 입력하기')
        openJsonButton.setFont(hangulFont)
        openJsonButton.clicked.connect(self.loadFile)

        shapeSelectButton = QtGui.QPushButton(u'정보 가져오기')
        shapeSelectButton.clicked.connect(self.getSkinInfo)
        shapeSelectButton.setFont(hangulFont)
        shapeInfo = QtGui.QLabel('SelectShape:')
        shapeInfo.setFont(self.myFont)
        self.shapeName = QtGui.QLabel('')
        self.shapeName.setFont(self.myFont)
        skinInfo = QtGui.QLabel('SkinCluster :')
        skinInfo.setFont(self.myFont)
        self.skinClusterName = QtGui.QLabel('')
        self.skinClusterName.setFont(self.myFont)

        jsonOutFolderButton = QtGui.QPushButton(u'폴더 선택')
        jsonOutFolderButton.setFont(hangulFont)
        jsonOutFolderButton.clicked.connect(self.outPath)

        self.fileNameLine = QtGui.QLineEdit('D:/')
        self.fileNameLine.setFont(self.myFont)

        makeJsonButton = QtGui.QPushButton(u'만들기')
        makeJsonButton.setFont(hangulFont)
        makeJsonButton.clicked.connect(self.makeFile)

        JointListButton = QtGui.QPushButton(u'수정된 조인트 순서 입히기')
        JointListButton.setFont(hangulFont)
        JointListButton.clicked.connect(self.reList)

        # list widget

        self.rightListWidget = listWidget()
        self.rightListWidget.setFont(self.myFont)
        self.leftListWidget = listWidget()
        self.leftListWidget.setFont(self.myFont)
        self.leftListWidget.setDragEnabled(False)
        self.leftListWidget.setAcceptDrops(False)
        # set layer

        openJsonLayout.addWidget(jsonSelectButton)
        openJsonLayout.addWidget(self.openFileNameLine)
        openJsonLayout.addWidget(openJsonButton)
        openJsonGroupBox.setLayout(openJsonLayout)

        makeJsonInfoLayout.addWidget(shapeInfo)
        makeJsonInfoLayout.addWidget(self.shapeName)
        makeJsonInfoLayout.addWidget(skinInfo)
        makeJsonInfoLayout.addWidget(self.skinClusterName)
        makeJsonInfoLayout.addWidget(shapeSelectButton)
        makeJsonFileLayout.addWidget(jsonOutFolderButton)
        makeJsonFileLayout.addWidget(self.fileNameLine)
        makeJsonFileLayout.addWidget(makeJsonButton)

        makeJsonLayout.addLayout(makeJsonInfoLayout)
        makeJsonLayout.addLayout(makeJsonFileLayout)

        jsonGroupBox.setLayout(makeJsonLayout)

        buttonLayout.addWidget(JointListButton)

        buttonLayout.setSpacing(0)

        listLayout.addWidget(self.rightListWidget)
        listLayout.addWidget(self.leftListWidget)

        jointGroupBox.setLayout(listLayout)
        
        mainLayout.addWidget(toolName)
        mainLayout.addWidget(jsonGroupBox)
        mainLayout.addWidget(openJsonGroupBox)
        
        mainLayout.addWidget(jointGroupBox)
        mainLayout.addLayout(buttonLayout)

        self.setLayout(mainLayout)

        self.weight = we.weightOut()

    def getSkinInfo(self):
        
        self.weight.getShape()
        
        self.shapeName.setText(self.weight.shape.name())
        self.skinClusterName.setText(self.weight.skin.name())

        self.rightListUP()
        
    def makeFile(self):
        
        filepath = str(self.fileNameLine.text())
        self.weight.outPath = filepath
        self.weight.dump()

    def loadFile(self):
        
        self.loadWeight.getShape()
        self.loadWeight.load()

    def outPath(self):
        
        self.outFolder = str(QtGui.QFileDialog.getExistingDirectory(self, 'Open Folder', 'c:/'))
        outPath = self.outFolder.replace('\\','/') + '/' + os.path.basename(str(self.fileNameLine.text()))
        if outPath.find('//') != -1:
            outPath = outPath.replace('//','/')
        self.fileNameLine.setText(outPath)

    def openFile(self):
        
        self.openFileJson = QtGui.QFileDialog.getOpenFileName(self, 'Open File', 'c:/', filter='*.msw')
        self.openFileNameLine.setText(self.openFileJson)
        
        weightFile = str(self.openFileNameLine.text())

        self.loadWeight = we.weightIn()
        self.loadWeight.outPath = weightFile

        #
        self.loadWeight.openData()
        self.dataJointList = self.loadWeight.getDataJointList()
        
        self.leftListUP()

    def rightListUP(self):
        
        self.rightListWidget.clear()
        
        item = []
        
        for z, xo in enumerate(self.weight.jointList):
            item.append(QtGui.QListWidgetItem(xo.name()))
            self.rightListWidget.addItem(item[z])
    
    def leftListUP(self):
        
        self.leftListWidget.clear()
        
        item = []

        for k, zo in enumerate(self.dataJointList):
            item.append(QtGui.QListWidgetItem(zo))
            self.leftListWidget.addItem(item[k])
    
    def reList(self):
        
        getItemList = []
        
        for x in range(self.rightListWidget.count()):
            getItemList.append(str(self.rightListWidget.item(x).text()))

        self.loadWeight.getShape()
        self.loadWeight.load(getItemList)





class listWidget(QtGui.QListWidget):

    def __init__(self, parent=None):

        super(listWidget, self).__init__(parent)
        
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.setToolTip(u'드래그 드롭을 하시면 아이템이 이동됩니다')
   

test = skinJsonTool()
test.show()
