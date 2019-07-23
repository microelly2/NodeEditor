import FreeCAD
from FreeCAD import Vector as MVector

#from nodeeditor.wrapper import MVector # as Vector

import numpy as np
from nodeeditor.say import *
import nodeeditor.store as store

class Array(object):
    def __init__(self,dat=[]):
        self.dat=np.array(dat)

from PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow.Core.Common import *

class Vector(FunctionLibraryBase):
    '''doc string for Vector'''
    def __init__(self,packageName):
        super(Vector, self).__init__(packageName)

    @staticmethod
    @IMPLEMENT_NODE(returns=('VectorPin', MVector()), nodeType=NodeTypes.Pure, meta={'Category': 'Vector', 'Keywords': ['Vector']})
    def vecCreate( X=('FloatPin', 0), Y=('FloatPin', 0), Z=('FloatPin', 0)):
        ''' vector by coordinates X, Y, Z.'''
        v = MVector(X,Y,Z)
        return v

#    @staticmethod
#    @IMPLEMENT_NODE(returns=('VectorPin', MVector()), nodeType=NodeTypes.Pure, meta={'Category': 'Vector', 'Keywords': ['Vector']})
#    def vecArray ( X=('ArrayPin', Array())):
#        ''' vector by coordinates X, Y, Z.'''
#        v = MVector()
#        return v

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0), nodeType=NodeTypes.Pure, meta={'Category': 'Vector', 'Keywords': ['Vector']})
    def vecX( Vector=('VectorPin', MVector())):
        ''' vector coordinate x'''
        return Vector.x

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0), nodeType=NodeTypes.Pure, meta={'Category': 'Vector', 'Keywords': ['Vector']})
    def vecY( Vector=('VectorPin', MVector())):
        ''' vector coordinate y'''
        return Vector.y

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0), nodeType=NodeTypes.Pure, meta={'Category': 'Vector', 'Keywords': ['Vector']})
    def vecZ( Vector=('VectorPin', MVector())):
        ''' vector coordinate z'''
        return Vector.z

    @staticmethod
    @IMPLEMENT_NODE(returns=("FloatPin", 0.0), meta={'Category': 'Vector', 'Keywords': ['vector', '|', 'dot', 'product']})
    def vecDotProduct(a=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["FloatVector4Pin", "VectorPin", "QuatPin"]}),
                   b=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["FloatVector4Pin", "VectorPin", "QuatPin"]})):
        '''Dot product'''
        return a.dot(b)

    @staticmethod
    @IMPLEMENT_NODE(returns=('VectorPin', MVector(1,2,3)), nodeType=NodeTypes.Pure, meta={'Category': 'Vector', 'Keywords': ['Vector', '+']})
    def vecAdd(a=('VectorPin', MVector()), b=('VectorPin', MVector())):
        '''adds vector a and b'''
        return a + b

    @staticmethod
    @IMPLEMENT_NODE(returns=('VectorPin', MVector()), nodeType=NodeTypes.Pure, meta={'Category': 'Vector', 'Keywords': ['Vector', '-']})
    def vecSubstract(a=('VectorPin', MVector()), b=('VectorPin', MVector())):
        '''substracts vector a and b'''
        return a - b

    @staticmethod
    @IMPLEMENT_NODE(returns=('VectorPin', MVector()), nodeType=NodeTypes.Pure, meta={'Category': 'Vector', 'Keywords': ['Vector', '-']})
    def between(a=('VectorPin', MVector()), b=('VectorPin', MVector()),m=('IntPin',5)):
        '''between vector a and b'''
        
        return a *0.1*(10-m)+b*m*0.1

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', []), nodeType=NodeTypes.Pure, meta={'Category': 'Vector', 'Keywords': ['Vector', '-']})
    def betweenList(a=('AnyPin', [],{'constraint': '1', 
                "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), 
        b=('AnyPin', [],{'constraint': '1', 
                "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), 
        m=('IntPin',5)):
        '''between list a and b'''
        rc=[av *0.1*(10-m)+bv*m*0.1 for av,bv in zip(a,b)]
        return rc

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', []), nodeType=NodeTypes.Pure, meta={'Category': 'Vector', 'Keywords': ['Vector', '-']})
    def move(a=('AnyPin', [],{'constraint': '1', 
                "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), 
        v=('VectorPin', MVector())):
        ''''''
        rc=[MVector(av)+v for av in a]
        return rc



#-------------numpy lib starts here -------------------------

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', [], {'constraint': '1'}), meta={'Category': 'numpy', 'Keywords': ['list','interval']})
    def linSpace(start=('FloatPin',0.),stop=('FloatPin',10), num=('IntPin', 50)):
        """create a linear Space"""

        x1 = np.linspace(start, stop, num, endpoint=True)
        return list(x1)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', [2.],{'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), meta={'Category': 'numpy', 'Keywords': ['list','random']})
    def randomList(size=('IntPin', 50)):
        """create a random list"""
        
        x1 = np.random.random(size)
        return list(x1)


    @staticmethod
    @IMPLEMENT_NODE(returns=('VectorPin', [],{'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), meta={'Category': 'numpy', 'Keywords': ['list','random']})
    def zip(x=('AnyPin', [0]),y=('AnyPin', [1]),z=('AnyPin', [2])) :
        """combine """
        
        res=np.array([x,y,z]).swapaxes(0,1)
        points=[FreeCAD.Vector(list(a)) for a in res]    
        return points

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', [],{'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), meta={'Category': 'numpy', 'Keywords': ['list','scale','multiply']})
    def scale(data=('AnyPin', [0]),factor=('FloatPin', 1.)) :
        """multiply datalist with factor """
        
        return list(np.array(data)*factor)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', [],{'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), meta={'Category': 'numpy', 'Keywords': ['list','scale','multiply']})
    def linearTrafo(data=('AnyPin', [0]),a=('FloatPin', 1.),b=('FloatPin', 0.)) :
        """a*x + b """
        
        return list(np.array(data)*a +b)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', [],{'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), meta={'Category': 'numpy', 'Keywords': ['list','scale','multiply']})
    def sin(data=('AnyPin', [0]),a=('FloatPin', 1.),b=('FloatPin', 1.),c=('FloatPin', 0.)) :
        """a*sin(b*x+c)"""
        
        return list(a*np.sin(np.array(data)*b +c))

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', [],{'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), meta={'Category': 'numpy', 'Keywords': ['list','scale','multiply']})
    def cos(data=('AnyPin', [0]),a=('FloatPin', 1.),b=('FloatPin', 1.),c=('FloatPin', 0.)) :
        """a*cos(b*x+c)"""
        
        return list(a*np.cos(np.array(data)*b +c))

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', [],{'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), meta={'Category': 'numpy', 'Keywords': ['list','scale','multiply']})
    def tan(data=('AnyPin', [0]),a=('FloatPin', 1.),b=('FloatPin', 1.),c=('FloatPin', 1.)) :
        """a*tan(b*x+c)"""
        
        return list(a*np.tan(np.array(data)*b +c))

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', [],{'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), meta={'Category': 'numpy', 'Keywords': ['list','scale','multiply']})
    def arctan(data=('AnyPin', [0]),a=('FloatPin', 1.),b=('FloatPin', 1.),c=('FloatPin', 1.)) :
        """arctan(x)"""
        
        return list(np.arctan(np.array(data)))

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', [],{'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), meta={'Category': 'numpy', 'Keywords': ['list','scale','multiply']})
    def arctan2(y=('AnyPin', [0]),x=('AnyPin', [0])) :
        """arctan2(y,x)"""
        
        return list(np.arctan2(np.array(y),np.array(x)))

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', [],{'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), meta={'Category': 'numpy', 'Keywords': ['list','scale','multiply']})
    def rad2deg(radians=('AnyPin', [0])) :
        """radians to degree"""
        
        return list(np.rad2deg(np.array(radians)))

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', [],{'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), meta={'Category': 'numpy', 'Keywords': ['list','scale','multiply']})
    def deg2rad(degree=('AnyPin', [0])) :
        """degree to radians"""
        
        return list(np.deg2rad(np.array(degree)))


    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', [],{'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), meta={'Category': 'numpy', 'Keywords': ['list','scale','multiply']})
    def unwrap(radians=('AnyPin', [0])) :
        """Unwrap by changing deltas between values to 2*pi complement.
Unwrap radian phase p by changing absolute jumps greater than discont to their 2*pi complement along the given axis."""
        
        return list(np.unwrap(np.array(radians)))


    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', [],{'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), meta={'Category': 'numpy', 'Keywords': ['list','scale','multiply']})
    def interp_lin(x=('AnyPin', [0,0.5,1.,1.5]),xp=('AnyPin', [0,1,2]),yp=('AnyPin', [0.,2.,0.]),) :
        """One-dimensional linear interpolation.

Returns the one-dimensional piecewise linear interpolant to a function with given discrete data points (xp, fp), evaluated at x."""
        
        return list(np.interp(x,xp,yp))

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', [],{'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), meta={'Category': 'numpy', 'Keywords': ['list','scale','multiply']})
    def add(x=('AnyPin', [0,1]),y=('AnyPin', [0,2])) :
        """"""
        
        return list(np.array(x)+np.array(y))


    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', [],{'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), meta={'Category': 'numpy', 'Keywords': ['list','scale','multiply']})
    def interp_cubic(x=('AnyPin', [0,0.5,1.,1.5]),xp=('AnyPin', [0,1,2]),yp=('AnyPin', [0.,2.,0.]),) :
        """Interpolate a 1-D function.

x and y are arrays of values used to approximate some function f: y = f(x). This class returns a function whose call method uses interpolation to find the value of new points."""
        from scipy import interpolate
        f = interpolate.interp1d(xp, yp,kind='cubic')
        y = f(np.array(x)) 
        
        return list(y)






    @staticmethod
    @IMPLEMENT_NODE(returns=('StringPin', None, ), nodeType=NodeTypes.Callable, meta={'Category': 'List', 'Keywords': []})
    def workspacex(name=('StringPin', None,), temp=('BoolPin', True),):

        say("workspace called")
        return (name)

    @staticmethod
    @IMPLEMENT_NODE(returns=('StringPin', "workspace", ),  meta={'Category': 'List', 'Keywords': []})
    def workspace(name=('StringPin', "workspace"), temp=('BoolPin', True),):

        say("workspace called")
        return (name)

    @staticmethod
    @IMPLEMENT_NODE(returns=('StringPin', None, ), nodeType=NodeTypes.Callable, meta={'Category': 'List', 'Keywords': []})
    def view3D(name=('StringPin', None,),Shape=('ShapePin',None),Workspace=('StringPin', None,),
        mode=('IntPin',0),wireframe=('BoolPin',False),transparency=('IntPin',50), temp=('BoolPin', True),):

        import nodeeditor.dev
        reload (nodeeditor.dev)
        return  nodeeditor.dev.run_view3d(name,Shape,Workspace,mode,wireframe,transparency)

        say("create 3d view for ",name,Shape,Workspace,mode)
        return (name)
