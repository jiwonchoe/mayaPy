###########################################################################################################################################################
# Written by jiwon choi
# help : jiwonkun@gmail.com
###########################################################################################################################################################

import pymel.api as api
import pymel.core as pm

import shiboken
from PySide import QtGui, QtCore

###########################################################################################################################################################


def getMayaWindow():  

    accessMainWindow = api.MQtUtil.mainWindow()

    return shiboken.wrapInstance(long(accessMainWindow), QtGui.QMainWindow)


###########################################################################################################################################################


class FoDoRi(QtGui.QWidget):
    
    def __init__ (self, parent=getMayaWindow()):
        
        self.closeCheck()

        super(FoDoRi, self).__init__(parent)
        
        ### deco

        titleP = QtGui.QPalette()
        titleP.setColor(QtGui.QPalette.Foreground, QtGui.QColor(0, 255, 0))
        titleP.setColor(QtGui.QPalette.Background, QtGui.QColor(10, 10, 10))

        titleFT = QtGui.QFont()
        titleFT.setBold(1)
        titleFT.setPointSize(20)
        
        lineFT = QtGui.QFont()
        lineFT.setBold(1)
        lineFT.setPointSize(16)
        
        listFT = QtGui.QFont()
        listFT.setPointSize(10)
        
        listP = QtGui.QPalette()
        listP.setColor(QtGui.QPalette.Highlight, QtGui.QColor(100, 200, 100))
        
        buttonFT = QtGui.QFont()
        buttonFT.setBold(1)
        buttonFT.setPointSize(10)
        
        makerP = QtGui.QPalette()
        makerP.setColor(QtGui.QPalette.Foreground, QtGui.QColor(0, 255, 0))
        makerP.setColor(QtGui.QPalette.Background, QtGui.QColor(10, 10, 10))
        
        makerFT = QtGui.QFont()
        makerFT.setBold(1)
        makerFT.setPointSize(7)
        
        labelFT = QtGui.QFont()
        labelFT.setBold(1)
        
        labelP = QtGui.QPalette()
        labelP.setColor(QtGui.QPalette.Foreground, QtGui.QColor(40, 40, 40))
        
        ### widget

        titleLB = QtGui.QLabel('FoDoRiTooL')
        titleLB.setAlignment(QtCore.Qt.AlignCenter)
        titleLB.setPalette(titleP)
        titleLB.setFont(titleFT)
        titleLB.setFrameStyle(QtGui.QFrame.StyledPanel | QtGui.QFrame.Plain)
        titleLB.setAutoFillBackground(1)

        makerLB = QtGui.QLabel('Written by jiwon choi | jiwonkun@gmail.com')
        makerLB.setPalette(makerP)
        makerLB.setFont(makerFT)
        makerLB.setAlignment(QtCore.Qt.AlignCenter)
        makerLB.setAutoFillBackground(1)        

        nodeLB = QtGui.QLabel('Search Node : ')
        nodeLB.setFont(labelFT)
        nodeLB.setPalette(labelP)
        
        self.completer = QtGui.QCompleter()
        self.setModelNode()
        
        self.nodeLineEdit = QtGui.QLineEdit()
        self.nodeLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.nodeLineEdit.setFont(lineFT)
        
        self.nodeLineEdit.setCompleter(self.completer)
        self.nodeLineEdit.returnPressed.connect(self.selectNode)
        
        #
        
        selectNodeButton = QtGui.QPushButton('select node')
        selectNodeButton.clicked.connect(self.selectNode)
        selectNodeButton.hide()
        
        line01 = QtGui.QFrame()
        line01.setFrameShape(QtGui.QFrame.HLine)
        line01.setFrameShadow(QtGui.QFrame.Plain)
        line01.setLineWidth(3)
        
        getListButton = QtGui.QPushButton('ListUp')
        getListButton.clicked.connect(self.listAttr)
        getListButton.setFont(buttonFT)
        
        #
        
        attrListLB = QtGui.QLabel('Attr List : ')
        attrListLB.setFont(labelFT)
        attrListLB.setPalette(labelP)

        self.weightListWidget = QtGui.QListWidget()
        self.weightListWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.weightListWidget.setFont(listFT)
        self.weightListWidget.setPalette(listP)
        self.weightListWidget.itemSelectionChanged.connect(self.getAttrNode)

        filterAttrLB = QtGui.QLabel('Filter attr : ')
        filterAttrLB.setFont(labelFT)
        filterAttrLB.setPalette(labelP)
        
        self.attrFilterLine = QtGui.QLineEdit('')
        self.attrFilterLine.setAlignment(QtCore.Qt.AlignCenter)
        self.attrFilterLine.returnPressed.connect(self.attrFilter)
        self.attrFilterLine.setFont(lineFT)
        
        valueLB = QtGui.QLabel('Value : ')
        valueLB.setFont(labelFT)
        valueLB.setPalette(labelP)
        
        self.setValueLine = QtGui.QLineEdit()
        self.setValueLine.setText('0.0')
        self.setValueLine.setValidator(QtGui.QDoubleValidator(self.setValueLine))
        self.setValueLine.setAlignment(QtCore.Qt.AlignCenter)
        self.setValueLine.returnPressed.connect(self.run)
        self.setValueLine.setFont(lineFT)
        
        setAttrB = QtGui.QPushButton('SetAttr')
        setAttrB.setFont(buttonFT)
        setAttrB.clicked.connect(self.run)
        
        overrideCrB = QtGui.QPushButton('Override Create')
        overrideCrB.setFont(buttonFT)
        overrideCrB.clicked.connect(lambda : self.overrideAttrRun(True))
        
        overrideRmB = QtGui.QPushButton('Override Remove')
        overrideRmB.setFont(buttonFT)
        overrideRmB.clicked.connect(lambda : self.overrideAttrRun(False))

        closeB = QtGui.QPushButton('Close')
        closeB.setFont(buttonFT)
        closeB.clicked.connect(self.close)

        sizeG = QtGui.QSizeGrip(self)
        
        ### layer
        
        inButtonLayout = QtGui.QHBoxLayout()
        inButtonLayout.setSpacing(1)
        
        inButtonLayout.addWidget(overrideCrB)
        inButtonLayout.addWidget(overrideRmB)
        
        buttonLayout = QtGui.QVBoxLayout()
        buttonLayout.setSpacing(1)

        buttonLayout.addWidget(setAttrB)
        buttonLayout.addLayout(inButtonLayout)
        buttonLayout.addWidget(closeB)        
        
        mainLayout = QtGui.QVBoxLayout()
        
        mainLayout.addWidget(titleLB)
        mainLayout.addWidget(nodeLB)
        mainLayout.addWidget(self.nodeLineEdit)
        mainLayout.addWidget(selectNodeButton)
        mainLayout.addWidget(line01)
        mainLayout.addWidget(getListButton)
        mainLayout.addWidget(attrListLB)
        mainLayout.addWidget(self.weightListWidget)
        mainLayout.addWidget(filterAttrLB)
        mainLayout.addWidget(self.attrFilterLine)
        mainLayout.addWidget(valueLB)
        mainLayout.addWidget(self.setValueLine)
        mainLayout.addLayout(buttonLayout)
        mainLayout.addWidget(makerLB)
        mainLayout.addWidget(sizeG, 0, QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)

        ### self

        self.setLayout(mainLayout)        
        self.setWindowTitle('Fordori')
        self.setObjectName('ForDoRiUI')
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window)

    
    def getAttrNode(self):
        
        try:
            valueOrg = self.obj.attr(self.weightListWidget.currentItem().text()).get()
        except:
            valueOrg = 0
        
        if type(valueOrg) == bool:
            valueOrg = int(valueOrg)
        
        value = unicode(valueOrg)
        
        self.setValueLine.setText(value)


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

        self.listAttr()

    
    def listAttr(self):

        self.objectList = pm.ls(sl=1)
        
        if not len(self.objectList):
            return 0

        self.obj = self.objectList[-1]
                
        self.objAttrList = pm.listAttr(self.obj, s=1)
        
        self.weightListWidget.clear()
        self.weightListWidget.addItems(self.objAttrList)
        
        self.nodeLineEdit.setText(self.obj.nodeType())


    def attrFilter(self):
        
        newList = []
        
        for x in self.objAttrList:
            if x.find(self.attrFilterLine.text()) != -1:
                newList.append(x)
        
        if len(newList):
            self.weightListWidget.clear()
            self.weightListWidget.addItems(newList)
            

    def run(self):
        
        items = self.weightListWidget.selectedItems()
        
        attrList = []
        
        pm.undoInfo(ock=1)        
        
        for x in items:
            attrList.append(x.text())
        
        value = float(self.setValueLine.text())
        
        for x in self.objectList:
            for y in attrList:
                try:
                    x.attr(y).set(value)
                except:
                    print x
        
        pm.undoInfo(cck=1)

    
    def overrideAttrRun(self, mode):

        items = self.weightListWidget.selectedItems()
        
        if pm.editRenderLayerGlobals(q=1, crl=1) == 'defaultRenderLayer':
            return 0

        attrList = []
        
        pm.undoInfo(ock=1)        
        
        for x in items:
            attrList.append(x.text())
        
        for x in self.objectList:
            for y in attrList:
                try:
                    if mode:
                        pm.editRenderLayerAdjustment(x.attr(y))
                    else:
                        overrideList = pm.editRenderLayerAdjustment(q=1)
                        if x.attr(y).name() in overrideList:
                            pm.editRenderLayerAdjustment(x.attr(y), remove=1)
                except:
                    print x                
        
        pm.undoInfo(cck=1)


    def mousePressEvent(self, event):
        
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()


    def mouseMoveEvent(self, event):
        
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()


    def closeCheck(self):

        for x in QtGui.QApplication.topLevelWidgets():
            try:
                if x.__class__.__name__ == self.__class__.__name__:
                    x.close()
            except:
                pass


FoDoRiRun = FoDoRi()
FoDoRiRun.show()
