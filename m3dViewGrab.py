
import pymel.api as api
import shiboken
from PySide import QtGui, QtCore

def m3dViewGrab(outPath, cropWidth = 800, cropHeight = 800, outWidth = 128, outheight = 128):

    view = api.M3dView.active3dView()
    
    widget_ptr = view.widget()
    widget = shiboken.wrapInstance(long(widget_ptr), QtGui.QWidget)
    
    viewWidth = view.portWidth()
    viewHeight = view.portHeight()
    
    xPoint = (viewWidth / 2) - (cropWidth / 2)
    yPoint = (viewHeight / 2) - (cropHeight / 2)
    
    pixmap = QtGui.QPixmap.grabWindow(widget.winId(), xPoint, yPoint, cropWidth, cropHeight)
    
    resizePixmap = pixmap.scaled(outWidth, outheight, QtCore.Qt.KeepAspectRatio)
    
    resizePixmap.save(outPath)
    #pixmap.save(outPath)

