# implemenation of the compute methods for category 

import numpy as np
import random
import time
import os.path
from os import path
import matplotlib.pyplot as plt
import scipy.interpolate

from nodeeditor.say import *
import nodeeditor.store as store
import nodeeditor.pfwrap as pfwrap


print ("reloaded: "+ __file__)



from nodeeditor.cointools import *



def run_FreeCAD_ImageT(self):

    from scipy import ndimage
    fn=self.getData('image')
    import matplotlib.image as mpimg    

    img=mpimg.imread(fn)
    (sa,sb,sc)=img.shape
    red=0.005*(self.getData("red")+100)
    green=0.005*(self.getData("green")+100)
    blue=0.005*(self.getData("blue")+100)
    #blue=0
    say("rgb",red,green,blue)
    
    
    # andere filtre
    #img = ndimage.sobel(img)
    #img = ndimage.laplace(img)
    
    im2=img[:,:,0]*red+img[:,:,1]*green+img[:,:,2]*blue
    im2=np.round(im2)
    
    if self.getData('invert'):
        im2 = 1- im2
    
    #im2 = ndimage.sobel(im2)

   
    ss=int((self.getData('maskSize')+100)/20)
    say("ss",ss)
    if ss != 0:
        mode=self.getData('mode')
        say("mode",mode)
        if mode=='closing':
            im2=ndimage.grey_closing(im2, size=(ss,ss))
        elif mode=='opening':
            im2=ndimage.grey_opening(im2, size=(ss,ss))    
        elif mode=='erosion':
            im2=ndimage.grey_erosion(im2, size=(ss,ss))
        elif mode=='dilitation':
            im2=ndimage.grey_dilation(im2, footprint=np.ones((ss,ss)))
        else:
            say("NO MODE")
       


    




    nonzes=np.where(im2 == 0)
    pts = [FreeCAD.Vector(sb+-x,sa-y) for y,x in np.array(nonzes).swapaxes(0,1)]
    
    h=10
    pts = [FreeCAD.Vector(sb+-x,sa-y,(red*img[y,x,0]+green*img[y,x,1]+blue*img[y,x,2])*h) for y,x in np.array(nonzes).swapaxes(0,1)]
    colors=[img[y,x] for y,x in np.array(nonzes).swapaxes(0,1)]
    say("len pts",len(pts))
    self.setData("Points_out",pts)
    


