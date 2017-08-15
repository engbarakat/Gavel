from neo4j.v1 import GraphDatabase, basic_auth




def Createslicegavel(session,listofswitches, listofhosts,slice):
    """Create a network slice"""
    #driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "gavel"))
    #session = driver.session()
    result = session.run("Create (:Slice {name:{slicename}})", {"slicename":slice})
    for host in listofhosts:
        session.run('''Match (h:Host{ip:{hostip}})
                       Match (l:Slice{name:{slicename}})
                       Merge (h)-[:Member_of]->(l)''',{"slicename":slice,"hostip":host})
    for switch in listofswitches:
        session.run('''Match (h:Switch{dpid:{hostip}})
                       Match (l:Slice{name:{slicename}})
                       Merge (h)-[:Member_of]->(l)''',{"slicename":slice,"hostip":switch})
        

#     result = session.run( ''' MATCH (h:Host) where h.ip in  {hostlist}
#                             Match (s:Switch) where s.dpid in  {switchlist}
#                             match (l:Slice{name:{slicename}}) with h,s,l
#                             Create (h)-[:Member_of]->(l) 
#                             Create (s)-[:Member_of]->(l) ;''',{"slicename":slice,"hostlist":listofhosts,"switchlist":listofswitches})
    

def Routeinslice(session,src,dst,slice):
    #driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "gavel"))
    #session = driver.session()
    result = session.run('''Match (l:Slice{name:{slicename}})
                            MATCH (h1:Host{ip:{srcip}})-[]->(l)
                            MATCH (h2:Host{ip:{dstip}})-[]->(l)
                            Match p=allshortestpaths((h1)-[:Connected_to*]->(h2))
                            where All (x in filter (x in Nodes(p) where x:Switch) where (x)-[:Member_of]-(l)) 
                            with h1,h2,l,p order by length(p) Limit 1 
                            create (h1)-[pa:PathSlice_to{switches:[n in nodes(p)[1..-1]| n.dpid], fports:[r in rels(p)[1..]| r.port1],bports:[r in rels(p)[..-1]| r.port2]}]->(h2) 
                            return pa.switches, pa.fports, pa.bports, h1.mac, h2.mac;''',{"slicename":slice,"srcip":src,"dstip":dst})
    return result
