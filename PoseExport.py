import pymel.core as pm
import pymel.api as api
from PySide import QtGui, QtCore
import shiboken
import m3dViewGrab as m3v
import exportAttrJson

reload(exportAttrJson)

def getPySideMayaWindow():  
    
    accessMainWindow = api.MQtUtil.mainWindow()  
    
    return shiboken.wrapInstance(long(accessMainWindow), QtGui.QWidget)

class PoseExport(QtGui.QWidget):

    def __init__(self, parent=getPySideMayaWindow()):
        
        super(PoseExport, self).__init__(parent)

        self.outPath = 'd:/test.pose'
        
        mainLayout = QtGui.QVBoxLayout()
        pathLayout = QtGui.QHBoxLayout()
        pushLayout =  QtGui.QHBoxLayout()
        
        outPathLabel = QtGui.QLabel('output :')
        self.outPathLine = QtGui.QLineEdit(self.outPath)
        outPush = QtGui.QPushButton('F')
        outPush.clicked.connect(self.outPathOpen)
        
        getPush = QtGui.QPushButton('Get Get Get Value !!!')
        getPush.clicked.connect(self.makeJson)
        
        imgPush = QtGui.QPushButton('Get Get Get Image !!!')
        imgPush.clicked.connect(self.makeImage)
       
        pathLayout.addWidget(outPathLabel)
        pathLayout.addWidget(self.outPathLine)
        pathLayout.addWidget(outPush)

        pushLayout.addWidget(imgPush)
        pushLayout.addWidget(getPush)
        pushLayout.setSpacing(0)
        
        mainLayout.addLayout(pathLayout)
        mainLayout.addLayout(pushLayout)
        
        self.setLayout(mainLayout)
        self.setWindowFlags(QtCore.Qt.Window)
        
        self.setWindowTitle('GetGetGet Value')
        self.setObjectName('getValueAndImage')
        
        self.show()

    def outPathOpen(self):
        openFolder = QtGui.QFileDialog.getExistingDirectory(self, 'Open Folder', 'd:/')
        self.outPathLine.setText(openFolder)

    def makeImage(self):
        outPath = self.outPathLine.text().replace('pose', 'png')
        m3v.m3dViewGrab(outPath, 800, 800, 400, 400)
    
    def makeJson(self):
        outPath = self.outPathLine.text()
        selectNode = pm.ls(sl=1)
        exportAttrJson.exportAttrJson(selectNode, outPath, {})

test = PoseExport()
