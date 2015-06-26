import pymel.core as pm

class renameNumberTool():

    def __init__(self):
        
        self.winName = 'RenameNumberTool'

    def initUI(self):
        
        if pm.window().exists(self.winName):
            pm.deleteUI(self.winName)
        
        window = pm.window(self.winName,wh=[400,100],s=0)
        ColumnLayout = pm.columnLayout(p=window)
        self.TextField = pm.textField(p=ColumnLayout,w=400,h=20)
        self.button = pm.button(p=ColumnLayout,w=400,h=30,l='ReName',c=pm.Callback(self.run))        

        window.show()

    def run(self):

        getText = self.TextField.getText()
        nums = getText.count('#')

        if nums != 0:
            getList = pm.ls(sl=1)
            if getList == []:
                print 'select???'
            else:
                if getText[0] != '#':
                    for y,x in enumerate(getList):
                        eval("x.rename(getText.split('#')[0] + '%0" + str(nums) + "d' % " + str(y+1) + " + getText.split('#')[-1])")
                        print x.name()
                else:                    
                    print 'first???'
        else:
            print '###???'
