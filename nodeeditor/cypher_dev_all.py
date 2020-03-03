
from nodeeditor.utils import *
from nodeeditor.say import *


# https://neo4j.com/docs/api/python-driver/current/#installation
from neo4j import GraphDatabase


def createNode2(tx,kid,typ,params):
        cmd="CREATE (p:"+typ+" {$params})"
        return tx.run(  "CREATE (p:"+typ+")"
                        "SET p.a='NEU' "
                       "SET p = $params " 
                        "RETURN p",                    
                       
        kid=kid,typ=typ,params=params)



class Development:
    
    def run_Cypher_Driver(self):
        #uri = "bolt://localhost:7687"
        uri=self.getData('uri')
        user=self.getData('user')
        password=self.getData('password')
        say(uri,user,password)
        
        try:
            #uri = "bolt://localhost:7687"
            #driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))

            driver = GraphDatabase.driver(uri, auth=(user, password))
            say(driver)
            self.setPinObject('driver',driver)

        except Exception as ex:
            sayErr(ex)


    def run_Cypher_Session(self):
        sayl()
        driver=self.getPinObject('driver')
        cmd=self.getData('command')
        say(cmd)
        # cmd="MATCH (a) RETURN a LIMIT 2"
        # MATCH (a:b_spline_curve_with_knots) RETURN a
        
        with driver.session() as session:
             rc = session.run(cmd)
                        
        #say(rc) # <neo4j.BoltStatementResult object at 0x2ae4564fdef0>
        rst=''
        if self.getData('process'):
            for d in rc.data():
                say(d)
                rst += "\n"+str(d)
            self.setData("resultString",rst)
        else:
            self.setData("resultString",None)
            self.setPinObject('resultObject',rc)
            say("##",rc.data())


    def run_Cypher_LoadCSV(self):

        driver=self.getPinObject('driver')
        cmd=self.getData('command')
        filename=self.getData('filename')
        #filename="https://neo4j.com/docs/cypher-manual/4.0/csv/artists.csv"
        
        ft=self.getData('fieldTerminator')
        if self.getData('withHeaders'):
            cmdall="LOAD CSV WITH HEADERS FROM '{}' AS line FIELDTERMINATOR '{}' ".format(filename,ft)
        else:
            cmdall="LOAD CSV FROM '{}' AS line FIELDTERMINATOR '{}' ".format(filename,ft)
        cmdall += " " + cmd
        say(cmdall)
        
        
        with driver.session() as session:
             rc = session.run(cmdall)

                
        rst=''
        ids=[]
        if self.getData('process'):
            for d in rc.data():
                say(d)
                ids += [d['id']]
                rst += "\n"+str(d)
            self.setData("resultString",rst)
            self.setData('ids',ids)
        else:
            self.setData("resultString",None)
            self.setPinObject('resultObject',rc)
            say("##",rc.data())


    def run_Cypher_Connect(self):

        driver=self.getPinObject('driver')
        cmd=self.getData('command')

        sources=self.getData('sources')
        targets=self.getData('targets')

        say(sources)
        say(targets)

        cmdall='''
        
                UNWIND $sources as x 
                UNWIND $targets as y 
                WITH x,y
                
                MATCH (a),(b)
                WHERE id(a)=x and id(b)=y
                MERGE (a)-[t:M_NN_M]->(b)
                return (t)

        '''
        say(cmdall)
        
        with driver.session() as session:
             rc = session.run(cmdall,sources=sources,targets=targets)

        say(rc)
        FreeCAD.rc=rc
        return
                
        rst=''
        ids=[]
        if self.getData('process'):
            for d in rc.data():
                say(d)
                #ids += [d['id']]
                rst += "\n"+str(d)
            self.setData("resultString",rst)
            self.setData('ids',ids)
        else:
            self.setData("resultString",None)
            self.setPinObject('resultObject',rc)
            say("##",rc.data())
                        

'''
MERGE (a{id:185})-[r:REL]->(b{id:185})

UNWIND [185,186,187] as x
WITH x MERGE (a{id:x})-[r:REL]->(b{id:185})

'''
