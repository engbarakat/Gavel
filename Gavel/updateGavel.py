
# contains code to update gavel from pox raised events.
from neo4j.v1 import GraphDatabase, basic_auth


#TODO  check logic from poxmanager original file and implements the functions

def installconnection():
    driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "ravel"))
    return driver.session()

def getnextswitchid():
    session = installconnection()
    result = session.run('''Match (h:Switch) return h.id''')
    listofallsidstring = []
    for s in result:
        listofallsidstring.append(s['h.id'])
    listofsidint = [d.split('_')[0] for d in listofallsidstring]
    return str(max(listofsidint)+1)+"_1_9" #9 for manual insertion  
    
def addswitchGavel(dpid):
    session = installconnection()
    id = getnextswitchid()
    result = session.run("Merge (s:Switch {dpid: {switchdpid}}) on create s.id = {switchid};",{"switchid":id, "switchdpid":dpid})
    

'''def addhostGavel(ipaddr, id, macaddr):
    session = installconnection()
    result = session.run(,{})
    pass

def delhostGavel(ipaddr):
    session = installconnection()
    result = session.run(,{})
    pass'''

def delswitchGavel(dpid):
    session = installconnection()
    result = session.run("Detach delete (n: Switch {dpid:{switchdpid}})",{"switchdpid":dpid})
    



def addlinkGavel(dpid2,port2,dpid1,port1):#no2 is the from and no1 is to // You still need to check the logic from Mininet to make sure that 2 and 1 are from and to
    session = installconnection()
    result = session.run( ''' MATCH (s2:Switch {dpid: {switchdpid2}})
                              MATCH (s1:Switch {dpid: {switchdpid1}})
                              MERGE (s1)-[r:Connected_to]->(s2)
                              ON CREATE SET r.port1 = {row.port1}, r.port2 = {row.port2}, r.node1 = {switchdpid1}, r.node2={switchdpid2},r.cost = {row.port1}
                              MERGE (s2)-[re:Connected_to]->(s1)
                              ON CREATE SET re.port1 = {row.port2}, re.port2 = {row.port1}, re.node1 = {switchdpid2}, re.node2={switchdpid1},re.cost = {row.port2};''',{"row.port1":port1,"row.port2":port2,"switchdpid1":dpid1,"switchdpid2":dpid2})
    

def dellinkGavel(dpid2,port2,dpid1,port1):#no2 is the from and no1 is to
    session = installconnection()
    result = session.run("Match (s1:Switch {dpid:{switchdpid}})-[r]-(s2:Switch {dpid:{switchdpido}}) delete r ",{"switchdpid":dpid2,"switchdpido":dpid1})
