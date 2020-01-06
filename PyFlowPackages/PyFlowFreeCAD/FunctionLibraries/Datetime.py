import FreeCAD


import datetime, time
from nodeeditor.say import *

from PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow.Core.Common import *

class Datetime(FunctionLibraryBase):
    '''doc string for '''
    def __init__(self,packageName):
        super(self.__class__, self).__init__(packageName)

    @staticmethod
    @IMPLEMENT_NODE(
            returns=('FloatPin', 0), 
            nodeType=NodeTypes.Pure, 
            meta={'Category': 'Datetime', 'Keywords': ['Time']}
        )
    def time( 
            hour=('IntPin', 0, {PinSpecifires.VALUE_RANGE: (0,23)}),
            #path=("StringPin", "", {PinSpecifires.INPUT_WIDGET_VARIANT: "PathWidget"}),
            minute=('IntPin', 15, {PinSpecifires.VALUE_RANGE: (0,59)}), 
            #second =('IntPin', 0, {PinSpecifires.VALUE_RANGE: (0,59), PinSpecifires.INPUT_WIDGET_VARIANT : "Simple"}),
            second =('IntPin', 0, {PinSpecifires.VALUE_RANGE: (0,59), }),
            microsecond =('IntPin', 0, {PinSpecifires.VALUE_RANGE: (0,999999)})
        ):
        ''' '''      
        
        #t=datetime.time(hour,minute,second,microsecond)
        #say(t)
        tt=hour*24*50+minute*60+second+ microsecond / 1E6
        return tt


    @staticmethod
    @IMPLEMENT_NODE(
            returns=('StringPin', ''), 
            nodeType=NodeTypes.Pure, 
            meta={'Category': 'Datetime', 'Keywords': ['Time']}
        )
    def strftime(
            timestamp =('FloatPin', 0, {PinSpecifires.INPUT_WIDGET_VARIANT : "NO"}),
            sformat = ('StringPin', "%a, %d %b %Y %H:%M:%S",
                {
                    "editable": False,
                    "ValueList":["%a, %d %b %Y %H:%M:%S","%a, %d %b %Y"," %H:%M:%S"],
                    PinSpecifires.INPUT_WIDGET_VARIANT: "EnumWidget",
                    

                })
        ):
        ''' '''
        if timestamp != 0:
            dt = datetime.datetime.fromtimestamp(timestamp)
        else:
            dt = datetime.datetime.now()

        rc=dt.strftime(sformat)
        say(rc)
        return rc
    

    @staticmethod
    @IMPLEMENT_NODE(
            returns=('FloatPin', 0), 
            nodeType=NodeTypes.Pure, 
            meta={'Category': 'Datetime', 'Keywords': ['Time']}
        )

    def now(
            t =('IntPin', 0, 
                {PinSpecifires.INPUT_WIDGET_VARIANT : "Slider",}),
            t2 =('IntPin', 0, 
                {PinSpecifires.INPUT_WIDGET_VARIANT : "Slider", PinSpecifires.VALUE_RANGE: (0,20),}),

        ):
        ''' '''
    
        say(t)
        say(t2)
        rc=time.time()
        return rc
    
