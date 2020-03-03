'''
Base classes and methods for neo4j cypher
'''

from PyFlow.Packages.PyFlowCypher.Nodes import *

sayl()



class CypherNodeBase(NodeBase):
    '''common methods for neo4j integration'''
    
    dok = 0
    
    def __init__(self, name="myNode",**kvargs):
        
        super(CypherNodeBase, self).__init__(name)
        self._debug = True
        self._debug = nodeeditor.config.debug
        self._preview=False
    

    def compute(self, *args, **kwargs):
        if self._debug:
            say("--- Start",self.name)
            self._started=time.time()
            say(self.__class__.category())
        
        import nodeeditor.cypher_dev_all
        reload(nodeeditor.cypher_dev_all)
        a="nodeeditor.cypher_dev_all.{}.run_{}(self)".format(self.__class__.category(),self.__class__.__name__)
        a=eval(a)

        if self._debug: 
            say("--- Done Post",self.name,round(time.time()-self._started2,2))

        if self._preview:
            say("create preview")
            self.preview()

        self.outExec.call()
        self.setColor()
        if self._debug: 
            say("--- Done Post",self.name,round(time.time()-self._started2,2))

            

    def preview(self):
        yid="ID_"+str(self.uid)
        yid=yid.replace('-','_')
        name=yid
    
    

    
    def refresh(self, *args, **kwargs):
        self.compute(*args, **kwargs)
        
        
    def show(self,*args, **kwargs):
        sayl()
        #say("self:",self)
        say("Content of {}:".format(self.getName()))
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

    
    

 
    def getPinDataYsorted(self,pinName):
        pin=self.getPinByName(pinName)
        ySortedPins = sorted(pin.affected_by, key=lambda pin: pin.owningNode().y)
        dat=[ps.getData() for ps in ySortedPins]
        return dat

 
 
            
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

    def setImage(self,imagename="neo4j"):
        import os
        image= os.path.dirname(__file__)+"/../UI/icons/"+imagename+".svg"
        wr=self.getWrapper()
        wr.image=image
        wr.svgIcon.setElementId("layer1")


'''
class FreeCadNodeBase2(FreeCadNodeBase):
    
    dok = 0
    
    def __init__(self, name="FreeCADNode",**kvargs):
        
        super(FreeCadNodeBase2, self).__init__(name)
    
    @timer
    def compute(self, *args, **kwargs):
        if self._debug:
            say("--- Start",self.name)
            self._started=time.time()
            say(self.__class__.category())
            #eval("import dev_{}".format(self.__class__.category())
        
        import nodeeditor.dev_all
        reload(nodeeditor.dev_all)
        a="nodeeditor.dev_all.{}.run_{}(self)".format(self.__class__.category(),self.__class__.__name__)
        try:
            a=eval(a)
        except:
            sayW("tried to run " + a)
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

'''





def nodelist():
    return [
    ]
