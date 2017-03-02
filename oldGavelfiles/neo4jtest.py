from py2neo import *
from dcttopo import *

fattopo = FatTreeTopo(64)
nodelist = {}
nodehostlist = {}
print "CoreSwitch*************"
#for s,e in fattopo.coreSwitches.iteritems():
#	print fattopo.coreSwitches[s] ,e
'''
for s,e in fattopo.edgeSwitches.iteritems():
	print s,e

for s,e in fattopo.hostList.iteritems():
	print s,e
print "AggSwitch*************"
for s in fattopo.AggSwitchList:
	print s
print "EdgeSwitch*************"
for s in fattopo.EdgeSwitchList:
	print s
print "Host*************"
for s in fattopo.HostList:
	print s
print "Links"
for s in fattopo.LinkList:
	print s

print "links *************"

for m in fattopo.links(False,False,True):
	print m[2]['node1']
	
'''

for s,e in fattopo.coreSwitches.iteritems():
	nodelist[s] = Node("Switch", **e)
for s,e in fattopo.aggrSwitches.iteritems():
	nodelist[s] = Node("Switch", **e)
for s,e in fattopo.edgeSwitches.iteritems():
	nodelist[s] = Node("Switch", **e)
for s,e in fattopo.hostList.iteritems():
	nodehostlist[s] = Node("Host", **e)
authenticate("localhost:7474", "neo4j", "ravel")
gx = Graph()
gx.delete_all()
#tx = gx.begin()
#for key, value in nodelist.iteritems():
	#print key, value
	#gx.create(value)
for r in fattopo.links(False,False,True):
	#print r [0] , r[1],nodelist[r[2]['node1']]["dpid"]
	#pass
	if r[2]['node1'] in nodehostlist.keys():
		#print "we found %s in first hostkeys" % r[2]['node1']
		gx.merge(Relationship(nodehostlist[r[2]['node1']],"Connected_to",nodelist[r[2]['node2']], port1 = r[2]['port1'], port2 = r[2]['port2'],\
		 node1 = nodehostlist[r[2]['node1']]["dpid"], node2 = nodelist[r[2]['node2']]["dpid"]))
	elif r[2]['node2'] in nodehostlist.keys():
		#print "we found %s in second hostkeys" % r[2]['node2']
		gx.merge(Relationship(nodehostlist[r[2]['node2']],"Connected_to",nodelist[r[2]['node1']], port1 = r[2]['port2'], port2 = r[2]['port1'],\
		node1 = nodehostlist[r[2]['node2']]["dpid"], node2 = nodelist[r[2]['node1']]["dpid"]))
	else:
		#print " %s and %s are switches" % (r[2]['node1'], r[2]['node2'])
		gx.merge(Relationship(nodelist[r[2]['node1']],"Switched_to",nodelist[r[2]['node2']], port1 = r[2]['port1'], port2 = r[2]['port2'],\
		node1 = nodelist[r[2]['node1']]["dpid"], node2 = nodelist[r[2]['node2']]["dpid"])) #do dpid instead of node1 node2
		gx.merge(Relationship(nodelist[r[2]['node2']],"Switched_to",nodelist[r[2]['node1']], port1 = r[2]['port2'], port2 = r[2]['port1'],\
		node1 = nodelist[r[2]['node2']]["dpid"], node2 = nodelist[r[2]['node1']]["dpid"])) # try to load database 64 and then 
	#print tr
	#gx.create(tr)
''
#tx.commit()
'''
LOAD CSV WITH HEADERS FROM "file:///connected_to32.csv" AS row
MATCH (s:Switch {id: row.node2})
MATCH (h:Host {id: row.node1})
MERGE (h)-[pu:Connected_to]->(s)
ON CREATE SET pu.port1 = toInt(row.port1), pu.port2 = toInt(row.port2), pu.node1 = h.ip, pu.node2=s.dpid;

USING PERIODIC COMMIT 10000
LOAD CSV WITH HEADERS FROM "file:///switched_to32.csv" AS row
MATCH (s2:Switch {id: row.node2})
MATCH (s1:Switch {id: row.node1})
MERGE (s1)-[pu:Switched_to]->(s2)
ON CREATE SET pu.port1 = toInt(row.port1), pu.port2 = toInt(row.port2), pu.node1 = s1.dpid, pu.node2=s2.dpid;

USING PERIODIC COMMIT 10000
LOAD CSV WITH HEADERS FROM "file:///switched_to32.csv" AS row
MATCH (s2:Switch {id: row.node2})
MATCH (s1:Switch {id: row.node1})
MERGE (s2)-[pu:Switched_to]->(s1)
ON CREATE SET pu.port1 = toInt(row.port2), pu.port2 = toInt(row.port1), pu.node1 = s2.dpid, pu.node2=s1.dpid;
'''
