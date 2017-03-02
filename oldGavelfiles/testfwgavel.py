from neo4j.v1 import GraphDatabase, basic_auth
from firewall import *
from route import *
from loadbalancer import *
import timeit
import random
import itertools
import os


def loadftgdb(sizeoffattree):
	print ">>>>>>>neo4j-shell -file new_gdb%s.cypher -host localhost -v" %sizeoffattree
	os.system("neo4j-shell -file new_gdb%s.cypher -host localhost -v" %sizeoffattree)

def runthetest(sizeoffattree,itera,listofpath):
	print ">>>>>>>start the test with size of %s for the time No.%d" %(sizeoffattree,itera)
	driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "ravel"))
	session = driver.session()
	session.run('''match (n)-[r]-() return count(n)''')
	
	#1. Test blockhost
	
	blockHost(session, "10.3.33.34")
	if getroute(session, "10.3.33.34", "10.3.2.3"):
		print "problem in FW! as src"
	else:
		print "FW working as src"
	
	if getroute(session, "10.3.2.3", "10.3.33.34"):
		print "problem in FW! as dst"
	else:
		print "FW working dst"
	
	#2. Test Unblockhost
	unblockHost(session, "10.3.33.34")
	if getroute(session, "10.3.33.34", "10.3.2.3"):
		print "unblock worked"
	else:
		print "unblock is not working!"
	#3. Test blockPath
	blockPath(session,"10.3.33.34", "10.3.2.3") 
	blockPath(session,"10.3.33.34", "10.3.30.31")
	lb = Loadbalancer(["10.3.30.31","10.3.33.34"],"10.3.2.3")
	lb.installroutewithlb("10.3.35.36")
	lb.installroutewithlb("10.3.37.38")
	lb.installroutewithlb("10.3.29.30")

	#4. Test unblockpath
	#################################################################################################
	#hostlistready = {}
	#listoftimea = []
	
	#listoftimeb = []
	
	#result = session.run('''Match (h:Host) return h.ip AS ip ''')
	#resultlistnotrandom = list(result)
	#resultlist = random.sample(resultlistnotrandom,38)
	#print list(result)
	#resultlist = list(result)

	#for n in xrange(0,len(resultlist), 2):
#		hostlistready[resultlist[n]["ip"]] = resultlist[n+1]["ip"]

#	for key,v in hostlistready.iteritems():
#		#print key, v
#		astartt = timeit.default_timer() *1000
#		result = session.run('''MATCH (h1:Host {ip:{firstip}}), (h2:Host {ip:{secondip}}) Match p=shortestPath((h1)-[:Connected_to*]->(h2)) 
#		 RETURN [n in nodes(p)[1..-2]| n.dpid] as switch, [r in rels(p)[1..-1]| r.port1] as port ; ''',{"firstip": key, "secondip": v} )
#		aendt = timeit.default_timer() *1000
		
#		bstartt = timeit.default_timer() *1000
#		for path in result:
#			#print path['switch'], path['port']
#			result = session.run('''Create (p1:Path{from:{firstip}, to:{secondip}, switches:{nodelist}, ports:{relslist}});''',{"firstip": key, "secondip": v, "nodelist":path['switch'],"relslist":path["port"]} )
#		bendt = timeit.default_timer() *1000
#		path = Path(key,v,aendt-astartt,bendt-bstartt)
#		listofpath.append(path)
		########################################################################################################

	
	session.close()

def writeresults(sizeoffattree,listofpath):	
	fo = open("newPostergavelresults%sall.txt" %sizeoffattree, "wb")
	for a in listofpath:
		fo.write(str(a.host1)+'\t'+str(a.host2) + '\t'+str(a.getpath)+'\t'+str(a.writepath) + '\n')
	fo.close()
def plotresults(k):
	os.system("gnuplot plotresults%d.gplt" %k)

listofpath=[]
for s in ['DT']:
	listofpath=[]
	loadftgdb(s)
	for i in range(1):
		pass
		#runthetest(s,i,listofpath)
	#writeresults(s,listofpath)
	#plotresults(s)
