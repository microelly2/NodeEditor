# Base classes and methods for freecad nodes

from PyFlow.Packages.PyFlowFreeCAD.Nodes import *

sayl()


# method only for get runtime
def timer(func):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        log=False
        log=nodeeditor.config.log
        try :
                is_method   = inspect.getargspec(func)[0][0] == 'self'
        except :
                is_method   = False
        if is_method :
                name    = '{}.{}.{}'.format(func.__module__, args[0].__class__.__name__, func.__name__)
        else :
                name    = '{}.{}'.format(fn.__module__, func.__name__)
        if log: sayW("call '{}'".format(name))
        start_time = time.time()
        value = func(*args, **kwargs)
        end_time = time.time()
        run_time = end_time - start_time    # 3
        if log: sayW("Finished method '{0}' in {1:.4f} secs".format(func.__name__,run_time))
        return value
    return wrapper_timer


class FreeCadNodeBase(NodeBase):
    '''common methods for FreeCAD integration'''
    
    dok = 0
    
    def __init__(self, name="FreeCADNode",**kvargs):
        
        super(FreeCadNodeBase, self).__init__(name)
        self._debug = False
        self._debug = nodeeditor.config.debug
        self._preview=False
    
    @timer
    def compute(self, *args, **kwargs):
        if self._debug:
            say("!-- Start",self.name)
            self._started=time.time()
        import nodeeditor.dev
        reload (nodeeditor.dev)
        a=eval("nodeeditor.dev.run_{}(self)".format(self.__class__.__name__))
        if self._debug: 
            say("--- Done",self.name,round(time.time()-self._started,2))
        if self._preview:
            say("create preview")
            self.preview()
            

    def preview(self):
        yid="ID_"+str(self.uid)
        yid=yid.replace('-','_')
        name=yid
        label="PV_"+self.getWrapper().getHeaderText()
        a=FreeCAD.ActiveDocument.getObject(name)

        if not self._preview and a != None:
            FreeCAD.ActiveDocument.removeObject(name)
        else:
            
            try:
                shape=self.getPinObject("Shape_out")
                pts=None
            except:
                shape=None

            if shape is None:
                try:
                    pts=self.getData("Points_out")
                except:
                    pts=None
            if pts is not None:
                import Points
                if a == None:
                    a = FreeCAD.ActiveDocument.addObject('Points::Feature', name)
                pm=a.Placement
                a.Points=Points.Points(pts)
                a.Placement=pm
                a.Label=label
            elif shape is not None:
                if a== None:
                    a=FreeCAD.ActiveDocument.addObject("Part::Feature",name)
                pm=a.Placement
                a.Shape=shape
                a.Placement=pm
                a.Label=label


    def makebackref(self):
        '''make reference insinde FreeCAD document to the node'''
        import nodeeditor.PyFlowGraph
        from nodeeditor.PyFlowGraph import PyFlowRef
        reload (nodeeditor.PyFlowGraph)
        try:
            label="REF_"+self.getWrapper().getHeaderText()
        except:
            return

        yid="REFID_"+str(self.uid)
        yid=yid.replace('-','_')
        name=yid
        a=FreeCAD.ActiveDocument.getObject(name)
        if a == None:
            a=PyFlowRef(name)
            a.refname=self.name
            a.Label=label

        return a
 
    
    
    def bake(self, *args, **kwargs):
        import nodeeditor.dev
        reload (nodeeditor.dev)
        try: s=self.getPinObject('Shape_out')
        except:
            say("nothing to bake")
            return
        
        # a=eval("nodeeditor.dev.run_{}(self,bake=True)".format(self.__class__.__name__))
        
        f = w.addObject('Part::Feature','baked')
        f.Shape=self.getPinObject('Shape_out')

    
    def refresh(self, *args, **kwargs):
        self.compute(*args, **kwargs)
        
        
    def initpins(self,name):

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.Show = self.createInputPin('Show', 'ExecPin', None, self.show)
        
        self.trace = self.createInputPin('trace', 'BoolPin')
        self.randomize = self.createInputPin("randomize", 'BoolPin')
        
        self.part = self.createOutputPin('Part', 'FCobjPin')
        self.shapeout = self.createOutputPin('Shape', 'ShapePin','True')
        
        self.objname = self.createInputPin("objectname", 'StringPin')
        self.objname.setData(name)
        
        self.shapeOnly = self.createInputPin("shapeOnly", 'BoolPin', True)
        self.shapeOnly.recomputeNode=True
    
    
    @timer
#    @genPart
    def show(self,*args, **kwargs):
        sayl()
        #say("self:",self)
        say("Content of {}:".format(self.getName()))
        #say("list all pins !! siehe FreeCAD.ref")
        FreeCAD.tt=self
        ll=len(self.getName())
        #say("self.getOrderedPins()")
        #say( self.getOrderedPins())
        
        k=self.orderedInputs.values()
        say("INPINS")
        for t in k:
            say(t)
            say(t.getFullName(),t.getData())
        sayl()
        k=self.orderedOutputs.values()
        say("OUTPINS")
        for t in k:
            say(t)
            say(t.getFullName(),t.getData())
        sayl()
        
        FreeCAD.ref=self
        return
        
        for t in self.getOrderedPins():
            say("{} = {} ({})".format(t.getName()[ll+1:],t.getData(),t.__class__.__name__))
            if len(t.affected_by):
                for tt in t.affected_by:
                    if not tt.getName().startswith(self.getName()):
                        say("<---- {} = {} ({})".format(tt.getName(),tt.getData(),tt.__class__.__name__))
            
            if len(t.affects):
                for tt in t.affects:
                    if not tt.getName().startswith(self.getName()):
                        say("----> {} = {} ({})".format(tt.getName(),tt.getData(),tt.__class__.__name__))
            
            
            n=t.__class__.__name__
            # spezialausgaben fuer objekte
            if n == 'ArrayPin':
                say(t.getArray())
            if n == 'FCobjPin':
                obj=t.getObject()
                if obj  !=  None :
                    try:
                        say("object: {} ({})".format(obj.Label,obj.Name))
                    except:
                        say(obj)
        
        FreeCAD.ref=self
        
        
        
        
    def getDatalist(self,pinnames):
        namelist=pinnames.split()
        ll=[self.getPinByName(a).getData() for a in namelist]
        return ll
        
    def applyPins(self,ff,zz):
        zz2=self.getDatalist(zz)
        return ff(*zz2)
        
    def setDatalist(self,pinnames,values):
        namelist=pinnames.split()
        sayl("--set pinlist for {}".format(self.getName()))
        for a,v in zip(namelist,values):
            say(a,v)
            #self.getPinByName(a).setData(v)
            self.getPinByName(a).setData(v)
 
    def getObject(self):
        '''get the FreeCAD object'''
        
        
        yid="ID_"+str(self.uid)
        yid=yid.replace('-','_')
        
        cc=FreeCAD.ActiveDocument.getObject(yid)
        
        try:
            if self.shapeOnly.getData():
                if cc:
                    say("delete object")
                    FreeCAD.ActiveDocument.removeObject(cc.Name)
                return None
        except: pass
        
        if cc == None:
            cc=FreeCAD.ActiveDocument.addObject("Part::Feature",yid)
            cc.ViewObject.Transparency=80
            cc.ViewObject.LineColor=(1.,0.,0.)
            cc.ViewObject.PointColor=(1.,1.,0.)
            cc.ViewObject.PointSize=10
            r=random.random()
            cc.ViewObject.ShapeColor=(0.,0.2+0.8*r,1.0-0.8*r)
        return cc
        
    def postCompute(self,fcobj=None):
        
        if self.part.hasConnections():
            say("send a Part")
            if fcobj == None:
                self.part.setData(None)
            else:
                self.part.setData(fcobj.Name)
        self.outExec.call()
        try:
            if self.trace.getData():
                self.show()
        except:
            pass
        
    #method to write/read the objectpins
    def getPinObject(self,pinName):
        return store.store().get(self.getData(pinName))
        
        
    def getPinObjectsA(self,pinName):
        eids=self.getData(pinName)
        if eids == None:
            sayW("no data on pin",pinName)
            return []
        return [store.store().get(eid) for eid in eids]
        
    def setPinObjects(self,pinName,objects):
        pin=self.getPinByName(pinName)
        ekeys=[]
        for i,e in enumerate(objects):
            k=str(pin.uid)+"__"+str(i)
            store.store().add(k,e)
            ekeys += [k]
        self.setData(pinName,ekeys)
        
    def setPinObject(self,pinName,obj):
        pin=self.getPinByName(pinName)
        k=str(pin.uid)
        store.store().add(k,obj)
        pin.setData(k)


    def getPinObjects(self,pinname='Shapes_in',sort=False):
        outArray=[]
        pin=self.getPinByName(pinname)
        if sort:
            pins = sorted(pin.affected_by, key=lambda pin: pin.owningNode().y)
        else:
            pins = pin.affected_by

        for i in pins:
            outArray.append(i.owningNode().getPinObject(i.name))

        print (outArray)
        return outArray

    def getPinPlacement(self,pinName):
        pmk=self.getData(pinName)
        return FreeCAD.Placement(FreeCAD.Matrix(*pmk))
    
    def setPinPlacement(self,pinName,placement):
        yy=placement.toMatrix().A 
        self.setData(pinName,list(yy))

    def getPinPlacements(self,pinName):
        pmks=self.getData(pinName)
        return [FreeCAD.Placement(FreeCAD.Matrix(*pmk)) for pmk in pmks]
    
    def setPinPlacements(self,pinName,placements):
        yy=[list(placement.toMatrix().A) for placement in placements]
        self.setData(pinName,yy)

    def setPinRotations(self,pinName,rotations):
        self.setData(pinName,[list(r.toEuler()) for r in rotations])
    
    def getPinRotations(self,pinName):
        rin=self.getData(pinName)
        rots=[FreeCAD.Rotation(*r) for r in rin]
        return rots

 
            
    def reset(self,*args, **kwargs):
        pass
        
    def refresh(self,*args, **kwargs):
        pass
        
    def funA(self,*args, **kwargs):
        sayl("function funA called")
        pass
        
    def funB(self,*args, **kwargs):
        sayl("function funB called")
        pass
        
    def funC(self,*args, **kwargs):
        sayl("function funC called")
        pass
 
    def setNodename(self,name):
        self.getWrapper().setHeaderHtml(name)
       
    def setColor(self, r= None,g= None, b= None, a=1.):
        if r == None:
            r = random.random()
        if g == None:
            g = random.random()
        if b == None:
            b = random.random()
            
        wr=self.getWrapper()
        if wr is not None:
            wr.headColor=QtGui.QColor.fromRgbF(r,g,b,a)
            wr.update()

    def setImage(self,imagename="freecad"):
        import os
        image= os.path.dirname(__file__)+"/../UI/icons/"+imagename+".svg"
        wr=self.getWrapper()
        wr.image=image
        wr.svgIcon.setElementId("layer1")


class FreeCadNodeBase2(FreeCadNodeBase):
    '''common methods for FreeCAD integration'''
    
    dok = 0
    
    def __init__(self, name="FreeCADNode",**kvargs):
        
        super(FreeCadNodeBase2, self).__init__(name)
    
    @timer
    def compute(self, *args, **kwargs):
        if self._debug:
            say("--- Start",self.name)
            self._started=time.time()
        import nodeeditor.dev
        reload (nodeeditor.dev)
        a=eval("nodeeditor.dev.run_{}(self)".format(self.__class__.__name__))
        if self._debug: 
            say("--- Done",self.name,round(time.time()-self._started,2))

        self._started2=time.time()
        self.outExec.call()
        self.setColor()
        if self._debug: 
            say("--- Done Post",self.name,round(time.time()-self._started2,2))


        if self._preview:
            say("create preview")
            self.preview()



# example shape
def createShape(a):
    
    pa=FreeCAD.Vector(0,0,0)
    pb=FreeCAD.Vector(a*50,0,0)
    pc=FreeCAD.Vector(0,50,0)
    shape=Part.makePolygon([pa,pb,pc,pa])
    return shape


def updatePart(name,shape):

    FreeCAD.Console.PrintError("update Shape for "+name+"\n")
    a=FreeCAD.ActiveDocument.getObject(name)
    if a== None:
        a=FreeCAD.ActiveDocument.addObject("Part::Feature",name)
    a.Shape=shape



def onBeforeChange_example(self,newData,*args, **kwargs):
    FreeCAD.Console.PrintError("before:"+str(self)+"\n")
    FreeCAD.Console.PrintError("data before:"+str(self.getData())+"-- > will change to:"+str(newData) +"\n")
    # do something like backup or checks before change here

def onChanged_example(self,*args, **kwargs):
    FreeCAD.Console.PrintError("Changed data to:"+str(self.getData()) +"\n")
    self.owningNode().reshape()




def nodelist():
    return [
#                FreeCAD_Bar,
#                FreeCAD_YYY,
    ]
