'''
nodes under development
nodes for debugging and test data 
some stuff to play and new prototypes in very alpha state
'''

from PyFlow.Packages.PyFlowCypher.Nodes import *
from PyFlow.Packages.PyFlowCypher.Nodes.Cypher_Base import CypherNodeBase


'''
ideen
https://github.com/community-graph/twitter-import/blob/master/twitter-import.py

'''


class Cypher_Driver(CypherNodeBase):
    '''
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        

        a = self.createInputPin("uri", 'StringPin',"bolt://localhost:7687")
        a = self.createInputPin("user", 'StringPin',"neo4j")
        a = self.createInputPin("password", 'StringPin',"password")

        

        a=self.createOutputPin('driver', 'FCobjPin')
        


    @staticmethod
    def description():
        return Cypher_Driver.__doc__

    @staticmethod
    def category():
        return 'Development'

class Cypher_Session(CypherNodeBase):
    '''
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        
        a=self.createInputPin('driver', 'FCobjPin')
        
                
        a = self.createInputPin("command", 'StringPin',"MATCH (a)-[r]->(b) RETURN a,b")
        self.process = self.createInputPin('process', 'Boolean')
        

        
        a=self.createOutputPin('resultObject', 'FCobjPin')
        a=self.createOutputPin('resultString', 'String')
        a=self.createOutputPin('ids', 'IntPin',structure=StructureType.Array)
        
        #FCobjPin


    @staticmethod
    def description():
        return Cypher_Session.__doc__

    @staticmethod
    def category():
        return 'Development'


class Cypher_LoadCSV(CypherNodeBase):
    '''
    a connection to a database
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        a=self.createInputPin('driver', 'FCobjPin')
        
        a = self.createInputPin("filename", 'StringPin','https://neo4j.com/docs/cypher-manual/4.0/csv/artists.csv')

        self.process = self.createInputPin('withHeaders', 'BoolPin')
        a = self.createInputPin("fieldTerminator", 'StringPin',',')
        
        #LOAD CSV WITH HEADERS FROM 'https://neo4j.com/docs/cypher-manual/4.0/csv/artists-with-headers.csv' AS line
		#CREATE (:Artist { name: line.Name, year: toInteger(line.Year)})
        
        a = self.createInputPin("command", 'StringPin'," CREATE (a:Artist { name: line[1], year: toInteger(line[2])}) return id(a) as id ")
        

        self.process = self.createInputPin('process', 'Boolean')
        a=self.createOutputPin('resultObject', 'FCobjPin')
        a=self.createOutputPin('resultString', 'StringPin')
        a=self.createOutputPin('ids', 'IntPin',structure=StructureType.Array)
        
        

    @staticmethod
    def description():
        return Cypher_LoadCSV.__doc__

    @staticmethod
    def category():
        return 'Development'


class Cypher_Connect(CypherNodeBase):
    '''
    connect nodes 
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        a=self.createInputPin('driver', 'FCobjPin')
        
        a = self.createInputPin("command", 'StringPin'," CREATE (a:Artist { name: line[1], year: toInteger(line[2])}) return id(a) as id ")
        
        self.process = self.createInputPin('process', 'Boolean')
        
        a=self.createOutputPin('resultObject', 'FCobjPin')
        a=self.createOutputPin('resultString', 'StringPin')
        
        a=self.createInputPin('sources', 'IntPin',structure=StructureType.Array)
        a=self.createInputPin('targets', 'IntPin',structure=StructureType.Array)
        a=self.createInputPin('type', 'StringPin',"dir")
        
        # problem ausblenden pin widget geht noch nicht
        #a=self.createInputPin('targets', 'IntPin')
        #a.enableOptions(PinOptions.ArraySupported)
        #a.disableOptions(PinOptions.SupportsOnlyArrays)
        #a.setInputWidgetVariant("None")

        a=self.createOutputPin('ids', 'IntPin',structure=StructureType.Array)
        

    @staticmethod
    def description():
        return Cypher_Connect.__doc__

    @staticmethod
    def category():
        return 'Development'








def nodelist():
    return [
    
    
   Cypher_Driver,
   Cypher_Session,
   Cypher_LoadCSV,
   Cypher_Connect,
   
 
   
]
