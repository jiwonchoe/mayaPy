import glob, os, itertools
from PyQt4 import QtGui, QtCore
import maya.OpenMayaUI as OpenMayaUI  
import sip
import pymel.core as pm

def getPyQtMayaWindow():  
    accessMainWindow = OpenMayaUI.MQtUtil.mainWindow()
    return sip.wrapinstance(long(accessMainWindow), QtCore.QObject)  

################
###### FN ######
################

def iconList(path):
    getList = glob.glob(path)

    return getList


def iconNameList(path):
    getList = glob.glob(path)
    returnList = []

    for x in getList:
        returnList.append(x.split('\\')[-1][7:].split('.')[0])

    return returnList


def numberCycle(num, cut):
    numList = itertools.cycle(range(num))

    returnList = []

    for y, x in enumerate(numList):
        returnList.append(x)
        if y == cut:
            break
    return returnList

class toolSet():
    def __init__(self):
        self.selectName = ''
    def selectNameSpace(self):
        self.selectName = pm.selected()[0].namespace()
        return self.selectName
        
    def buttonRun(self, number, ctrName):
        ctr = pm.PyNode(nameSP + ctrName)
        ctr.key.set(number)
        ctr.key.setKey(ott='step')

    def mouthMirror(self, ctrName):
        ctr = pm.PyNode(nameSP + ctrName)
        value = ctr.mirror_map.get()
        if value == 0:
             ctr.mirror_map.set(1)
             ctr.mirror_map.setKey()
        else:
             ctr.mirror_map.set(0)
             ctr.mirror_map.setKey()


################
###### UI ######
################



class iconButton(QtGui.QPushButton):

    def __init__(self, number, path, ctrName):
        super(iconButton, self).__init__()

        icon = QtGui.QIcon()
        icon.addFile(path)
        buttonSize = QtCore.QSize()
        buttonSize.setHeight(40)
        buttonSize.setWidth(40)
        self.setIconSize(buttonSize)
        self.setFixedSize(buttonSize)
        self.setIcon(icon)
        checkFile = os.stat(path)
        if checkFile.st_size == long(2869L):
            self.setHidden(1)
        self.setStyleSheet('background-color: #DBDBDB')
        self.num = number
        self.ctr = ctrName
        
        self.setToolTip(str(number))
        self.clicked.connect(self.run)

    def run(self):
        run = toolSet()
        run.buttonRun(self.num, self.ctr)

class eyeTab(QtGui.QWidget):

    def __init__(self):
        super(eyeTab, self).__init__()

        Layout = QtGui.QHBoxLayout()
        self.upLayout = QtGui.QGridLayout()
        self.downLayout = QtGui.QGridLayout()

        self.upLayout.setSpacing(0)
        self.downLayout.setSpacing(0)
        self.upLayout.setHorizontalSpacing(0)
        self.upLayout.setVerticalSpacing(0)
        Layout.setSpacing(0)
        Layout.addLayout(self.upLayout)
        Layout.addLayout(self.downLayout)
        Layout.addStretch(1)

        self.setLayout(Layout)

        self.path = 'W:/BBM/Assets/Rig/CH/Main/facial/emotion_sequence/eye_emotion/icon/*.png'

        self.addIcon()

    def addIcon(self):
        self.LeyeItem = []
        self.ReyeItem = []
        
        iconFileList = iconList(self.path)
        iconCount = len(iconFileList)

        num = numberCycle(4, iconCount - 1)
        i = 0

        for n, x in enumerate(num):
            self.LeyeItem.append(iconButton(n, iconFileList[n], 'L_eye_facial_ctr'))
            self.ReyeItem.append(iconButton(n, iconFileList[n], 'R_eye_facial_ctr'))
            self.upLayout.addWidget(self.ReyeItem[n], i, x)
            self.downLayout.addWidget(self.LeyeItem[n], i, x)
            if x == 3:
                i += 1

class mouthTab(QtGui.QWidget):

    def __init__(self):
        super(mouthTab, self).__init__()

        self.Layout = QtGui.QVBoxLayout()
        self.upLayout = QtGui.QGridLayout()

        self.upLayout.setSpacing(0)
        self.Layout.setSpacing(0)
        self.Layout.addLayout(self.upLayout)
        
        self.path = 'W:/BBM/Assets/Rig/CH/Main/facial/emotion_sequence/charator_emotion/icon/*.png'

        self.setLayout(self.Layout)

        self.addIcon()

    def addIcon(self):
        self.mouthItems = []
        iconFileList = iconList(self.path)
        iconCount = len(iconFileList)

        num = numberCycle(8, iconCount - 1)
        i = 0

        for n, x in enumerate(num):
            self.mouthItems.append(iconButton(n, iconFileList[n], 'mouth_ctr'))
            self.upLayout.addWidget(self.mouthItems[n], i, x)
            if x == 7:
                i += 1



class facialTool(QtGui.QWidget):

    def __init__(self, parent=getPyQtMayaWindow()):
        super(facialTool, self).__init__(parent)

        vLayout = QtGui.QVBoxLayout()
        hLayout = QtGui.QHBoxLayout()

        self.setButton = QtGui.QPushButton('setCharactor')
        reButton = QtGui.QPushButton('Reload')
        mmButton = QtGui.QPushButton('mouthMirror')
        
        self.setButton.clicked.connect(self.namePick)
        reButton.clicked.connect(self.reloadItem)
        mmButton.clicked.connect(self.mirror)
        hLayout.addWidget(self.setButton)
        hLayout.addWidget(reButton)
        hLayout.addWidget(mmButton)

        tab = QtGui.QTabWidget()
        
        self.eye = eyeTab()
        self.mouth = mouthTab()

        tab.addTab(self.eye, 'Eye')
        tab.addTab(self.mouth, 'Mouth')

        vLayout.addWidget(tab)
        vLayout.addLayout(hLayout)
        self.setLayout(vLayout)
        vLayout.addStretch(0)

        # style
        """
        styleFile = open('w:/BBM/Assets/Rig/Set/Rigging/set/darkorange.stylesheet', 'r')
        self.setStyleData = styleFile.read()
        styleFile.close()
        self.setStyleSheet(self.setStyleData)
        """
        self.setWindowTitle('Facial Tool')
        
        self.setWindowFlags(QtCore.Qt.Window)
        
        self.show()
    
    def namePick(self):
        self.nameCH = toolSet()
        global nameSP
        nameSP = self.nameCH.selectNameSpace()
        self.setButton.setText(nameSP)

    def reloadItem(self):
        
        facialType = pm.PyNode(nameSP + 'CH')
        
        for x in self.mouth.mouthItems:
            x.close()
        
        if nameSP.find('badguy_') != -1:
            self.mouth.path = 'W:/BBM/Assets/Rig/CH/Main/facial/emotion_sequence/badguy_01_emotion/icon/*.png'
        else:
            if facialType.facial_m_type.get() == 1:
                self.mouth.path = 'W:/BBM/Assets/Rig/CH/Main/facial/emotion_sequence/M_charator_emotion/icon/*.png'
            elif facialType.facial_m_type.get() == 2:
                self.mouth.path = 'W:/BBM/Assets/Rig/CH/Main/facial/emotion_sequence/V_charator_emotion/icon/*.png'
            else:
                self.mouth.path = 'W:/BBM/Assets/Rig/CH/Main/facial/emotion_sequence/charator_emotion/icon/*.png'
        self.mouth.addIcon()
        
        for y, z in zip(self.eye.LeyeItem, self.eye.ReyeItem):
            y.close()
            z.close()
        
        if facialType.facial_e_type.get() == 0:
            if nameSP.find('bobo') != -1:
                self.eye.path = 'W:/BBM/Assets/Rig/CH/Main/facial/emotion_sequence/eye_emotion/iconBobo/*.png'
            elif nameSP.find('octo') != -1:
                self.eye.path = 'W:/BBM/Assets/Rig/CH/Main/facial/emotion_sequence/eye_emotion/icon/*.png'
            else:
                self.eye.path = 'W:/BBM/Assets/Rig/CH/Main/facial/emotion_sequence/eye_emotion/iconDef/*.png'
        elif facialType.facial_e_type.get() == 2:
            self.eye.path = 'W:/BBM/Assets/Rig/CH/Main/facial/emotion_sequence/Box_eye_emotion/icon/*.png'
        
        self.eye.addIcon()

    def mirror(self):
        self.nameCH.mouthMirror('mouth_ctr')

