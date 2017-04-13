from neo4j.v1 import GraphDatabase, basic_auth
from OFcomposer import *


def getrouteold(session, srcIP, dstIP):
	resultroute = session.run('''MATCH (h1:Host {ip:{firstip}}), (h2:Host {ip:{secondip}}) Match p=shortestPath((h1)-[:Connected_to*]->(h2)) 
		 RETURN [n in nodes(p)[1..-2]| n.dpid] as switch, [r in rels(p)[1..-1]| r.port1] as port ; ''',{"firstip": srcIP, "secondip": dstIP} )
	for path in resultroute:
		result = session.run('''Create (p1:Path{from:{firstip}, to:{secondip}, switches:{nodelist}, 
		ports:{relslist}});''',{"firstip": srcIP, "secondip": dstIP, "nodelist":path['switch'],"relslist":path["port"]} )
		if path:
			return True
		return False
def getroute(session, srcIP, dstIP):
	# check if a relationship exists
	# check if the type is correct
	# return to the user
	resultroute = session.run('''Match (Host{ip:{firstip}}) -[r]-(Host{ip:{secondip}}) return distinct type(r)''',{"firstip": srcIP, "secondip": dstIP} )
	for relationship in resultroute:
		print  relationship["type(r)"]
		if relationship["type(r)"] != "Path_to" :
			print "Path between %s and %s is blocked or not possible"%(srcIP,dstIP)
			return False
		print "Path already installed check your switches!"
	
	result = session.run('''MATCH (h1:Host {ip:{firstip}}), (h2:Host {ip:{secondip}}) Match p=shortestPath((h1)-[:Connected_to*]->(h2)) with h1,h2, p
	create (h1)-[pa:Path_to{switches:[n in nodes(p)[1..-1]| n.dpid], ports:[r in rels(p)[1..]| r.port1]}]->(h2) return pa.switches, pa.ports;''',{"firstip": srcIP, "secondip": dstIP} )
	for pathins in result:
		msgOF("installflow",switches = pathins["pa.switches"],portsforward = pathins["pa.ports"],portsbackward = None , src = srcIP, dst =dstIP )
		return True
	return False


