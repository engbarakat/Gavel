from neo4j.v1 import GraphDatabase, basic_auth
import timeit
import random
import itertools
import os


class Path:
	def __init__(self,host1, host2, getpath, writepath):
		self.host1 = host1
		self.host2 = host2
		self.getpath = getpath
		self.writepath = writepath
def loadftgdb(sizeoffattree):
	print ">>>>>>>neo4j-shell -file new_gdb%s.cypher -host localhost -v" %sizeoffattree
	os.system("neo4j-shell -file new_gdb%s.cypher -host localhost -v" %sizeoffattree)

def runthetest(sizeoffattree,itera,listofpath):
	print ">>>>>>>start the test with size of %s for the time No.%d" %(sizeoffattree,itera)
	driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "ravel"))
	session = driver.session()
	session.run('''match (n)-[r]-() return count(n)''')
	session.run('''match (r:Path) delete r''')
	session.run('''CREATE INDEX ON :Path(from);''')
	session.run(''' CREATE INDEX ON :Path(to);''')
	hostlistready = {}
	listoftimea = []
	
	listoftimeb = []
	
	result = session.run('''Match (h:Host) return h.ip AS ip ''')
	resultlistnotrandom = list(result)
	resultlist = random.sample(resultlistnotrandom,38)
	#print list(result)
	#resultlist = list(result)

	for n in xrange(0,len(resultlist), 2):
		hostlistready[resultlist[n]["ip"]] = resultlist[n+1]["ip"]

	for key,v in hostlistready.iteritems():
		#print key, v
		astartt = timeit.default_timer() *1000
		result = session.run('''MATCH (h1:Host {ip:{firstip}}), (h2:Host {ip:{secondip}}) Match p=shortestPath((h1)-[:Connected_to*]->(h2)) 
		 RETURN [n in nodes(p)[1..-2]| n.dpid] as switch, [r in rels(p)[1..-1]| r.port1] as port ; ''',{"firstip": key, "secondip": v} )
		aendt = timeit.default_timer() *1000
		
		bstartt = timeit.default_timer() *1000
		for path in result:
			#print path['switch'], path['port']
			#'''MATCH (h1:Host {ip:{firstip}}), (h2:Host {ip:{secondip}}) Match p=shortestPath((h1)-[:Connected_to*]->(h2)) with h1,h2, p
	#create (h1)-[pa:Path_to{switches:[n in nodes(p)[1..-1]| n.dpid], ports:[r in rels(p)[1..]| r.port1]}]->(h2) return pa.switches, pa.ports;'''
			result = session.run('''MATCH (h1:Host {ip:{firstip}}), (h2:Host {ip:{secondip}}) create (h1)-[pa:Path_to{switches:{nodelist}, ports:{relslist}}]->(h2)
			;''',{"firstip": key, "secondip": v, "nodelist":path['switch'],"relslist":path["port"]} )
		bendt = timeit.default_timer() *1000
		path = Path(key,v,aendt-astartt,bendt-bstartt)
		listofpath.append(path)
		#listoftimea.append(aendt-astartt)
		#listoftimeb.append(bendt-bstartt) 

	
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
		runthetest(s,i,listofpath)
	writeresults(s,listofpath)
	#plotresults(s)
