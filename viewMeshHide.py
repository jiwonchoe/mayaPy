import pymel.core as pm
import pymel.api as api

def viewObjectList(cut=False):

    #layerOnOff(False)

    activeView = api.M3dView.active3dView()
    objSelectionList = api.MSelectionList()
    api.MGlobal.selectFromScreen(0, 0, activeView.portWidth(), activeView.portHeight(), api.MGlobal.kReplaceList)
    api.MGlobal.getActiveSelectionList(objSelectionList)
    api.MGlobal.clearSelectionList()
    
    hideList = []

    for x in range(objSelectionList.length()):
        dummy = api.MObject()
        objSelectionList.getDependNode(x, dummy)
        if cut:
            hideList.append(api.MFnTransform(dummy).name().split(':')[0])
        else:
            hideList.append(api.MFnTransform(dummy).name())
    
    #layerOnOff(True)
    
    return hideList


def viewOutHide():
    
    transNodeList = []
    
    startTime = pm.playbackOptions(q=1, min=1)
    endTime = pm.playbackOptions(q=1, max=1)
    
    for x in range(int(startTime), int(endTime + 1)):
        pm.currentTime(x)
        transNodeList += viewObjectList(False)
    
    transNodeListS = set(transNodeList)

    allTransNodeList = set()
    
    for x in pm.ls(type='mesh'):
        allTransNodeList.add(x.getParent().name())

    hideList = allTransNodeList - transNodeListS
    
    for x in hideList:
        try:
            pm.setAttr(x + '.v', 0)
        except:
            pass

    pm.currentTime(startTime)

viewOutHide()
