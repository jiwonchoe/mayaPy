import pymel.core as pm
import json, ast


class weightOut():
    
    def __init__(self, out='D:/'):

        self.outPath = out

    def getShape(self):

        self.skin = pm.ls(sl=1)[0].listHistory(type='skinCluster')[0]
        self.shape = self.skin.getGeometry()[0]
        self.jointList = self.skin.getInfluence()
        self.fileName = self.shape.name() + '.msw'
        self.weightDic = {}

    def dump(self):

        if self.shape.type() == 'mesh': 
            
            for y, x in enumerate(self.skin.getWeights(self.shape)):
                
                addList = []
                
                for k, z in enumerate(x):
                    
                    addList.append([self.jointList[k].name(), z])
                
                self.weightDic[y] = addList

        elif self.shape.type() == 'nurbsCurve': 
            
            for y, x in enumerate(self.skin.getWeights(self.shape)):
                
                addList = []
                
                for k, z in enumerate(x):
                    
                    addList.append([self.jointList[k].name(), z])
                
                self.weightDic[y] = addList

        elif self.shape.type() == 'lattice':

            ptList = []
            
            for y in self.shape.pt:
                
                ptList.append( str(y.indices()[0][:]))
            
            for y, x in enumerate(self.skin.getWeights(self.shape)):
                
                addList = []
                
                for k, z in enumerate(x):
                    
                    addList.append([self.jointList[k].name(), z])
            
                self.weightDic[ptList[y]] = addList

        with open(self.outPath + self.fileName, 'w') as outFile:
            
            json.dump(self.weightDic, outFile, indent=4, separators=(',', ': '))


class weightIn():

    def __init__(self, out='D:/'):
        
        self.outPath = out
        self.dataJoint = []
        self.weightDic = {}
        
    def getShape(self):

        self.skin = pm.ls(sl=1)[0].listHistory(type='skinCluster')[0]
        self.shape = self.skin.getGeometry()[0]
        self.jointList = self.skin.getInfluence()

    def openData(self):

        with open(self.outPath) as jsonFile:
            
            self.weightDic = json.load(jsonFile)
        
    def load(self, *reList):
        
        
        if len(reList) != 0:
            
            self.jointList = []
            
            for s in reList[0]:
                
                self.jointList.append(s)

        if self.shape.type() == 'mesh':        
            
            for a in range(len(self.weightDic)):
                
                for t in range(len(self.weightDic['0'])):
                    
                    self.weightDic[x][t][0] = self.jointList[t]

                pm.skinPercent(self.skin, self.shape.vtx[a], tv = self.weightDic[x])


        elif self.shape.type() == 'nurbsCurve':        
            
            for a in range(len(self.weightDic)):
                
                for t in range(len(self.weightDic['0'])-1):
                    
                    self.weightDic[x][t][0] = self.jointList[t]

                pm.skinPercent(self.skin, self.shape.cv[a], tv = self.weightDic[x])


        elif self.shape.type() == 'lattice':
            
            reData = []
            
            for a in self.weightDic:
                
                reData.append(ast.literal_eval(a))

            for y, x in enumerate(self.weightDic):
            
                for t in range(len(self.weightDic[x])):
                        
                        self.weightDic[x][t][0] = self.jointList[t]

                pm.skinPercent(self.skin, self.shape.pt[reData[y][0]][reData[y][1]][reData[y][2]], tv = self.weightDic[x])

    def getDataJointList(self):

        dataList = self.weightDic[self.weightDic.keys()[0]]
        
        returnData = []
        
        for x in dataList:
            
            returnData.append(x[0])

        return returnData
