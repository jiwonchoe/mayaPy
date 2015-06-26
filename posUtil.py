import pymel.core as pm

def typeCheck(obj):
    
    if obj.__class__ == pm.MeshVertex:
        typeC = 'mesh'
    elif obj.__class__ == pm.LatticePoint:
        typeC = 'lattice'
    elif obj.__class__ == pm.NurbsCurveCV:
        typeC = 'curve'
    else:
        typeC = 'transform'

    return typeC

def latticePt(pointList):

    pointValueList = []

    for x in pointList:
        obj = x.node()
        index = x.currentItemIndex()
        localPoint = obj.point(index[0], index[1], index[2])
        objPoint = obj.wm.get().translate
        setPoint = pm.datatypes.Point(localPoint.x * obj.getParent().sx.get(), localPoint.y * obj.getParent().sy.get(), localPoint.z * obj.getParent().sz.get())
        pointValueList.append(objPoint + setPoint)

    return pointValueList

def meshCurveVt(pointList):
    
    pointValueList = []

    for x in pointList:
        pointValueList.append(x.getPosition('world'))

    return pointValueList

def makeNodeSet(pointValueList, transNodeType):
    
    for x in pointValueList:
        if transNodeType == 'locator':
            pm.spaceLocator().t.set(x)
        else:
            pm.createNode(transNodeType).t.set(x)

def tansformAttach(objList):
    
    pointValueList = []
    
    for x in objList:
        pointValueList.append(x.wm.get().translate)
    
    return pointValueList



def run():

    objList = pm.ls(sl=1, fl=1)
    
    node = 'locator'

    if objList[0].__class__ == pm.MeshVertex:
        pointValueList = meshCurveVt(objList)
    elif objList[0].__class__ == pm.LatticePoint:
        pointValueList = latticePt(objList)
    elif objList[0].__class__ == pm.NurbsCurveCV:
        pointValueList = meshCurveVt(objList)
    else:
        pointValueList = tansformAttach(objList)

    makeNodeSet(pointValueList, node)


def center():
    
    objList = pm.ls(sl=1, fl=1)
    
    node = 'locator'

    if objList[0].__class__ == pm.MeshVertex:
        pointValueList = meshCurveVt(objList)
    elif objList[0].__class__ == pm.LatticePoint:
        pointValueList = latticePt(objList)
    elif objList[0].__class__ == pm.NurbsCurveCV:
        pointValueList = meshCurveVt(objList)
    else:
        pointValueList = tansformAttach(objList)
    
    sumPoint = pm.datatypes.Point(0, 0, 0)

    for x in pointValueList:
        sumPoint = sumPoint + x
    
    value = sumPoint / len(pointValueList)

    makeNodeSet([value], node)
