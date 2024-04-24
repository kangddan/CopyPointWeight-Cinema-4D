import c4d
from c4d import gui

class CopyPointWeightUI(gui.GeDialog):
    
    UI_INSTANCE = None 
    @classmethod
    def UIDisplay(cls):
        if not cls.UI_INSTANCE: 
            cls.UI_INSTANCE = CopyPointWeightUI()

        if not cls.UI_INSTANCE.IsVisible():
            cls.UI_INSTANCE.Open(dlgtype=c4d.DLG_TYPE_ASYNC, pluginid=0, xpos=-2, ypos=-2,
                             defaultw=300, defaulth=100, subid=0) 
        else:
            cls.UI_INSTANCE.Open(dlgtype=c4d.DLG_TYPE_ASYNC)
                             
                                
    
    def __init__(self, *args, **kwargs):
        super(CopyPointWeightUI, self).__init__(*args, **kwargs)
        self.weights = []

    def CreateLayout(self):
        self.SetTitle('Copy Point Weight')
        mainLayout = self.GroupBegin(7777, flags=c4d.BFH_SCALEFIT)
        self.createButtons()
        self.GroupEnd()
        return True

    def createButtons(self):
        self.copyBut = self.AddButton(8888, flags=c4d.BFH_SCALEFIT,
                       initw=100 ,inith=30 ,name='Copy')
        self.pasteBut = self.AddButton(9999, flags=c4d.BFH_SCALEFIT,
                      initw=100 ,inith=30 ,name='Paste')

    def Command(self, index, msg):
        doc = c4d.documents.GetActiveDocument()
        obj = doc.GetActiveObject()
        if obj is None: return True
        weightTag = obj.GetTag(c4d.Tweights)
        if weightTag is None: return True

        if index == 8888: 
            self.weights = []
            self.getSelectedPointWeight(obj, weightTag, self.weights)
        elif index == 9999: 
            self.setSelectedPointsWeight(obj, weightTag, self.weights)
        return True
    
    # ------------------------------------------------------
    @staticmethod
    def getSelectedPointWeight(obj, weightTag, weightData):
        for p in CopyPointWeightUI.getSelectedPoints(obj):
            for j in range(weightTag.GetJointCount()):
                pointWeight = weightTag.GetWeight(j, p)
                weightData.append(pointWeight)
            break 
            
    @staticmethod
    def setSelectedPointsWeight(obj, weightTag, weightData):
        doc.StartUndo()
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
        for p in CopyPointWeightUI.getSelectedPoints(obj):
            for index, j in enumerate(range(weightTag.GetJointCount())):
                weightTag.SetWeight(j, p, 0.0)
                weightTag.SetWeight(j, p, weightData[index])
        weightTag.WeightDirty() # update Skin
        c4d.EventAdd()
        doc.EndUndo()
    
    @staticmethod
    def getSelectedPoints(obj):
        return [p for p in range(obj.GetPointCount()) if obj.GetPointS().IsSelected(p)]
              
if __name__=='__main__':
    CopyPointWeightUI.UIDisplay()

'''    
code by kangddan      
Revision History 
Revision 1: 2024-04-23 : First publish
'''    