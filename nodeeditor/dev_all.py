
from nodeeditor.utils import *

import nodeeditor.dev as Default


import nodeeditor.dev_Geom2D as Geom2D

import nodeeditor.dev_BSpline as BSpline

import nodeeditor.dev_Coin as Coin

import nodeeditor.dev_Combination as Combination
import nodeeditor.dev_Construction as Construction
import nodeeditor.dev_Conversion as Conversion
import nodeeditor.dev_Curves  as Curves

import nodeeditor.dev_Details  as Details
import nodeeditor.dev_Document as Document

if devmode:
    import nodeeditor.dev_Development as Development


#import nodeeditor.dev_  as 

import nodeeditor.dev_Generator as Generator

import nodeeditor.dev_Information  as Information

import nodeeditor.dev_Lambda as Lambda
import nodeeditor.dev_Logic  as Logic

import nodeeditor.dev_Points as Points
import nodeeditor.dev_Primitive as Primitive
import nodeeditor.dev_Projection as Projection

import nodeeditor.dev_Sensor  as Sensor
import nodeeditor.dev_Signal  as Signal
import nodeeditor.dev_Surface  as Surface

import nodeeditor.dev_Voronoi as Voronoi

from nodeeditor.say import *



import nodeeditor
if devmode:
    reload(nodeeditor.dev)
    reload(nodeeditor.dev_Development)
    pass


#reload(nodeeditor.dev_Logic)
#reload(nodeeditor.dev_Points)

#reload(nodeeditor.dev_BSpline)


#reload(nodeeditor.dev_Primitive)

#reload(nodeeditor.dev_Coin)
#reload(nodeeditor.dev_Conversion)
#reload(nodeeditor.dev_Information)
#reload(nodeeditor.dev_Lambda)

#reload(nodeeditor.dev_Projection)
#reload(nodeeditor.dev_Primitives)

def run_FreeCAD_Collect_Data(self, mode=None):

    if mode=="reset":
        self.points=[]
    
    else:

        maxSize=self.getData("maxSize")    
        point = self.getData("data")

        self.points += [point]
        if maxSize >0 and len(self.points)>maxSize:
                self.points = self.points[len(self.points)-maxSize:]   

    self.setData("collection",self.points)

    if not self.inRefresh.hasConnections():
        self.outExec.call()

