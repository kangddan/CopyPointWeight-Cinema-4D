import c4d
from c4d import gui
doc = c4d.documents.GetActiveDocument()
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
        self.mainLayout(self.createBut)
        self.GroupEnd()
        return True

    # ---------------------------------------------------------

    def mainLayout(self, widgets):
        vHBLayout = self.GroupBegin(7777, flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,
                         cols=0, rows=0, title="", groupflags=0, initw=0, inith=0)
        widgets()
        self.GroupEnd()

    def createBut(self):
        self.copyBut = self.AddButton(8888, flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,
                       initw=100 ,inith=30 ,name='Copy')
        self.pasteBut = self.AddButton(9999, flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,
                      initw=100 ,inith=30 ,name='Paste')

    # ---------------------------------------------------------

    def Command(self, _id, message):
        obj = doc.GetActiveObject()
        if not isinstance(obj, c4d.PolygonObject):
            c4d.gui.MessageDialog('Please select a polygon object!')
            return True

        weightTag = obj.GetTag(c4d.Tweights)
        if weightTag is None:
            c4d.gui.MessageDialog('The selected object has no weight tag!')
            return True

        if _id == 8888:
            self.weights = []
            self.getSelectedPointWeight(obj, weightTag, self.weights)
        elif _id == 9999:
            doc.StartUndo()
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
            self.setSelectedPointsWeight(obj, weightTag, self.weights)
            c4d.EventAdd()
            doc.EndUndo()
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
        for p in CopyPointWeightUI.getSelectedPoints(obj):
            for index, j in enumerate(range(weightTag.GetJointCount())):
                #weightTag.SetWeight(j, p, 0.0)
                weightTag.SetWeight(j, p, weightData[index])
        weightTag.WeightDirty() # update Skin

    @staticmethod
    def _getSelectedPoints(obj):
        return [p for p in range(obj.GetPointCount()) if obj.GetPointS().IsSelected(p)]

    @staticmethod
    def getSelectedPoints(obj):
        bs = obj.GetPointS()
        sel = bs.GetAll(obj.GetPointCount())
        return [index for index, selected in enumerate(sel) if selected]

if __name__=='__main__':
    CopyPointWeightUI.UIDisplay()

'''
code by kangddan
Revision History
Revision 1: 2024-04-23 : First publish
'''
