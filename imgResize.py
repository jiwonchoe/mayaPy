import pymel.api as pa
import os, glob
from PyQt4 import QtGui, QtCore
import sip


def getPyQtMayaWindow():  
    accessMainWindow = pa.MQtUtil.mainWindow()
    return sip.wrapinstance(long(accessMainWindow), QtCore.QObject)

class imgResize(QtGui.QWidget):
    def __init__(self,parent=getPyQtMayaWindow()):
        super(imgResize, self).__init__(parent)

        mainLayout = QtGui.QVBoxLayout()
        lineLayout = QtGui.QHBoxLayout()
        outLineLayout = QtGui.QHBoxLayout()
        sizeLayout = QtGui.QHBoxLayout()

        self.pathLine = QtGui.QLineEdit()
        self.outPathLine = QtGui.QLineEdit()

        self.runButton = QtGui.QPushButton('Resize')
        self.runButton.clicked.connect(self.reSizeFile)
        
        openLabel = QtGui.QLabel('Open Path')

        pathDialBT = QtGui.QPushButton('Open')
        pathDialBT.clicked.connect(self.openPath)

        outLabel = QtGui.QLabel('Out Path')
        outPathDialBT = QtGui.QPushButton('Open')
        outPathDialBT.clicked.connect(self.outPath)

        sizeLabel = QtGui.QLabel('Size')
        self.xLine = QtGui.QLineEdit('512')
        self.yLine = QtGui.QLineEdit('512')

        fileTypeLabel = QtGui.QLabel('Type')
        self.fileType = QtGui.QLineEdit('png')

        outFileTypeLabel = QtGui.QLabel('outType')
        self.outFileType = QtGui.QLineEdit('png')

        self.progress = QtGui.QProgressBar()
        
        lineLayout.addWidget(openLabel)
        lineLayout.addWidget(self.pathLine)
        lineLayout.addWidget(pathDialBT)
        
        outLineLayout.addWidget(outLabel)
        outLineLayout.addWidget(self.outPathLine)
        outLineLayout.addWidget(outPathDialBT)

        sizeLayout.addWidget(sizeLabel)
        sizeLayout.addWidget(self.xLine)
        sizeLayout.addWidget(self.yLine)
        sizeLayout.addWidget(fileTypeLabel)
        sizeLayout.addWidget(self.fileType)
        sizeLayout.addWidget(outFileTypeLabel)
        sizeLayout.addWidget(self.outFileType)
        

        mainLayout.addLayout(lineLayout)
        mainLayout.addLayout(outLineLayout)
        mainLayout.addLayout(sizeLayout)
        mainLayout.addWidget(self.runButton)
        mainLayout.addWidget(self.progress)
        
        # style
        styleFile = open('w:/BBM/Assets/Rig/Set/Rigging/set/darkorange.stylesheet', 'r')
        self.setStyleData = styleFile.read()
        styleFile.close()
        self.setStyleSheet(self.setStyleData)

        self.setLayout(mainLayout)
        self.setWindowTitle('Resize')
        self.setWindowFlags(QtCore.Qt.Window)

        self.show()

    def openPath(self):
        self.openFolder = str(QtGui.QFileDialog.getExistingDirectory(self, 'Open Folder', 'c:/'))
        self.pathLine.setText(self.openFolder)

    def outPath(self):
        self.outFolder = str(QtGui.QFileDialog.getExistingDirectory(self, 'Open Folder', 'c:/'))
        self.outPathLine.setText(self.outFolder)

    def reSizeFile(self):
        fileIn = str(self.pathLine.text()).replace('\\','/') + '/*.' + str(self.fileType.text())
        fileList = glob.glob(fileIn)

        sizeX = int(self.xLine.text())
        sizeY = int(self.yLine.text())
        
        self.progress.setRange(1, len(fileList))
        
        i = 1
        
        for x in fileList:
            self.progress.setValue(i)
            i += 1
            img = pa.MImage()
            img.readFromFile(x.replace('\\','/'))
            img.resize(sizeX, sizeY, True)
            folder = str(self.outPathLine.text()).replace('\\','/') + '/'
            fileName = os.path.basename(x).split('.')[0] + '.'  + str(self.outFileType.text())
            img.writeToFile(folder + fileName, str(self.outFileType.text()))

test_ = imgResize()
