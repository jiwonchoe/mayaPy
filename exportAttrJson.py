import pymel.core as pm
import json

'''
selectNode = pm.ls(sl=1)
outputPath = 'd:/fuck.pose'
attrData = {}
'''

def exportAttrJson(selectNode, outputPath, attrData):
    
    for y in selectNode:
        addVar = []
        attrList = y.listAttr(k=1)
        for x in attrList:
            addVar.append([x.name().split('.')[-1], x.get()])
        attrData[y.name().split(':')[-1]] = addVar
    
    with open(outputPath, 'w') as outFile:
        json.dump(attrData, outFile, indent=4, separators=(',', ': '))
