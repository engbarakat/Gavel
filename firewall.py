from neo4j.v1 import GraphDatabase, basic_auth
from OFcomposer import *
from route import *


def blockHost(session,hostIP):
	
	result = session.run('''Match (h1:Host{ip:{firstip}}) -[r:Connected_to]->(s2:Switch) REMOVE h1:Host SET h1:blockedHost return  distinct s2.dpid; ''',{"firstip": hostIP} )
	for hostblocked in result:
		msgOF("blockHost",hostIP,hostblocked['s2.dpid'])
		return
	return False
	#print "Blocking Host with IP %s was NOT successful! Are you sure it exists?!"%hostIP
	

def blockPath(session, srcIP,dstIP):
	#Note what about blocking Path which is not exists? how to prevent it in future?
	#what about create new path
	result = session.run('''MATCH (h1:Host{ip:{firstip}}) -[r:Path_to]-(h2:Host{ip:{secondip}}) CREATE (h1)-[r2:Blockedpath_to]->(h2) SET r2 = r WITH r, r2  DELETE r return r2.switches; ''',{"firstip": srcIP, "secondip": dstIP} )
	for sw in result:
		if sw["r2.switches"] is not None:
			print "Blocking Path from %s to %s was successful"%(srcIP,dstIP)
			#print sw["switch"] # get switch DPID
			msgOF("blockPath",srcIP,dstIP)
			return
		return
	result = session.run('''MATCH (h1:Host {ip:{firstip}}), (h2:Host {ip:{secondip}}) Match p=shortestPath((h1)-[:Connected_to*]->(h2)) with h1,h2, p
	create (h1)-[pa:Blockedpath_to{switches:[n in nodes(p)[1..-1]| n.dpid], ports:[r in rels(p)[1..]| r.port1]}]->(h2) return pa.switches, pa.ports;''',{"firstip": srcIP, "secondip": dstIP} )
	#print "Blocking Path from %s to %s was NOT successful! Are you sure it exists?!"%(srcIP,dstIP)


def unblockHost(session, hostIP):
	
	result = session.run('''Match (h1:blockedHost{ip:{firstip}}) -[r:Connected_to]->(s2:Switch) REMOVE h1:blockedHost SET h1:Host return  distinct s2.dpid;''',{"firstip": hostIP} )
	for hostblocked in result:
		msgOF("unblockHost",hostblocked['s2.dpid'])
		return
	return False
	#print "Unblocking Host with IP %s was NOT successful! Are you sure it exists or already not blocked?!"%hostIP


def unblockPath(session, srcIP,dstIP):
	#Note what about blocking Path which is not exists? how to prevent it in future?
	#what about create new path
	result = session.run('''MATCH (h1:Host{ip:{firstip}}) -[r:Blockedpath_to]-(h2:Host{ip:{secondip}}) CREATE (h1)-[r2:Path_to]->(h2) SET r2 = r WITH r, r2  DELETE r return r2.switches; ''',{"firstip": srcIP, "secondip": dstIP} )
	for sw in result:
		if sw["r2.switches"] is not None:
			#print "Unblocking Path from %s to %s was successful"%(srcIP,dstIP)
			#print sw["switch"] # get switch DPID
			msgOF("unblockPath",srcIP,dstIP)
		return
	return False
	#print "Unblocking Path from %s to %s was NOT successful! Are you sure it exists or already not blocked?!"%(srcIP,dstIP)

