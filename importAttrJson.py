import pymel.core as pm
import json

objNameSpace = pm.ls(sl=1)[0].namespace()


openFilePath = 'd:/fuck.pose'

with open(openFilePath) as jsonFile:
    attrData = json.load(jsonFile)

for x in attrData:
    setObj = pm.PyNode(objNameSpace + ':' + x)
    for y in attrData[x]:
        setObjAttr = setObj.attr(y[0])
        setObjAttr.set(y[1])
