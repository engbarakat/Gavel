
# contains code to update gavel from pox raised events.
from neo4j.v1 import GraphDatabase, basic_auth
import os


#TODO  check logic from poxmanager original file and implements the functions

def installconnection():
    driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "gavel"))
    return driver.session()

def getnextswitchid():
    driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "gavel"))
    session = driver.session()
    result = session.run('''Match (h:Switch) return h.id''')
    listofallsidstring = []
    for s in result:
        print s['h.id']
        listofallsidstring.append(s['h.id'])
    listofsidint = [d.split('_')[0] for d in listofallsidstring]
    return str(max(listofsidint)+1)+"_1_9" #9 for manual insertion  
    
def addswitchGavel(dpid,name):
    #ID here has to be stoped and entered manually using the same dpid for future fix""""
    driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "gavel"))
    session = driver.session()
    #id = getnextswitchid() 
    result = session.run("Merge (s:Switch {dpid: {switchdpid}}) on create set s.id = {switchdpid}, s.name = {switchname};",{"switchdpid":dpid,"switchname":name})
    


def delswitchGavel(dpid):
    driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "gavel"))
    session = driver.session()
    result = session.run("match (n: Switch {dpid:{switchdpid}}) Detach delete n;",{"switchdpid":dpid})
    



def addlinkGavel(dpid2,port2,dpid1,port1):#no2 is the from and no1 is to // You still need to check the logic from Mininet to make sure that 2 and 1 are from and to
    driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "gavel"))
    session = driver.session()
    result = session.run( ''' MATCH (s2:Switch {dpid: {switchdpid2}})
                              MATCH (s1:Switch {dpid: {switchdpid1}})
                              MERGE (s1)-[r:Connected_to]->(s2)
                              ON CREATE SET r.port1 = {rowport1}, r.port2 = {rowport2}, r.node1 = {switchdpid1}, r.node2={switchdpid2},r.cost = {rowport1}
                              MERGE (s2)-[re:Connected_to]->(s1)
                              ON CREATE SET re.port1 = {rowport2}, re.port2 = {rowport1}, re.node1 = {switchdpid2}, re.node2={switchdpid1},re.cost = {rowport2};
                              ''',{"rowport1":port1,"rowport2":port2,"switchdpid1":dpid1,"switchdpid2":dpid2})
    

def dellinkGavel(dpid2,port2,dpid1,port1):#no2 is the from and no1 is to
    driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "gavel"))
    session = driver.session()
    result = session.run("Match (s1:Switch {dpid:{switchdpid}})-[r]-(s2:Switch {dpid:{switchdpido}}) delete r ",{"switchdpid":dpid2,"switchdpido":dpid1})
    
def addhostGavel(macaddr,ipaddr,dpid,switchport):
    """
    Add the host and add the connectoin to switch
    """
    driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "gavel"))
    session = driver.session()
    result = session.run("Merge (s:Host {mac: {switchdpid}}) on create set s.id = {switchdpid}, s.ip={hostip};",{"switchdpid":macaddr,"hostip":ipaddr})
    addlinkhostGavel(ipaddr,dpid,switchport)
    

def deletehostGavel(macaddr):
    """
    Make sure to delete all connections that they have in the database
    """
    driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "gavel"))
    session = driver.session()
    result = session.run("match (n: Host {mac:{switchdpid}}) Detach delete n;",{"switchdpid":macaddr})

def addlinkhostGavel(ipaddr,dpid,switchport):
    driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "gavel"))
    session = driver.session()
    hport = -1
    result = session.run( '''MATCH (s:Switch {dpid: {switchdpid2}}) MATCH (h:Host {ip: {hostip1}}) MERGE (h)-[r:Connected_to]->(s)
ON CREATE SET r.port1 = toInt( {rowport1}), r.port2 =toInt( {rowport2}), r.node1 = {hostip1}, r.node2={switchdpid2},r.cost = toInt({rowport2})
MERGE (s)-[re:Connected_to]->(h)
ON CREATE SET re.port1 = toInt({rowport2}), re.port2 = toInt( {rowport1}), re.node1 = {switchdpid2}, re.node2={hostip1},re.cost = toInt({rowport2});
                              ''',{"rowport2":switchport,"hostip1":ipaddr,"switchdpid2":dpid,"rowport1":hport})
    

def loaddb(topologyname = None):
    #load gavel database topology
    driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "gavel"))
    session = driver.session()
    if (topologyname is None):
        os.system("neo4j-shell -file clear.cypher -host localhost -v")
        return True
    os.system("neo4j-shell -file new_gdb%s.cypher -host localhost -v" %topologyname)

def getswtichname(dpid):
    driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "gavel"))
    session = driver.session()
    result = session.run('''MATCH (s:Switch {dpid: {switchdpid1}}) return s.name as name''',{"switchdpid1":dpid})
    for n in result:
        return n["name"]