import pymel.core as pm


def ChnInOut(inoutType='in'):

    if len(pm.ls(sl=1)) == 0:
        print 'pz select Obj'
        return 0
    
    obj = pm.ls(sl=1)[0]
    
    channels = pm.channelBox('mainChannelBox', q = 1, sma = 1)
    
    
    objChannels = map(obj.attr, channels)
    
    inputList = []
    outputList = []
    
    for x in objChannels:
        if x.isConnected():
            inputList.append(x.inputs())
        else:
            inputList.append(None)
        if not len(x.outputs()) <= 0:
            outputList.append(x.outputs)
        else:
            outputList.append(None)
    
    print inputList
    print outputList
    
    if inoutType == 'in':
        pm.select(inputList, r=1)
        return inputList
    else:
        return outputList


ChnInOut()
