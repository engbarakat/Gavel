from neo4j.v1 import GraphDatabase, basic_auth
import timeit
import random

driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "ravel"))
session = driver.session()
session.run('''match (n)-[r]-() return count(n)''')

hostlistready = {}
listoftime = []
listofpath = []


#randomskip = random.randrange(1,16)
#result = session.run('''Match (h:Host) return h.ip AS ip skip {randomoffest} limit 8''', {"randomoffest": randomskip})
result = session.run('''Match (h:Host) return h.ip AS ip ''')
resultlistnotrandom = list(result)
resultlist = random.sample(resultlistnotrandom,300)

for n in xrange(0,len(resultlist), 2):
	hostlistready[resultlist[n]["ip"]] = resultlist[n+1]["ip"]

for key,v in hostlistready.iteritems():
	print key, v
	startt = timeit.default_timer() *1000
	path = session.run('''MATCH (h1:Host {ip:{firstip}})-[:Connected_to]->(sw1:Switch), 
	(h2:Host {ip:{secondip}})-[:Connected_to]->(sw2:Switch) Match p=shortestPath((sw1)-[*]->(sw2)) 
	MERGE (h1)-[pu:Reaches]->(h2) RETURN [n in nodes(p) | n.dpid] ; ''',{"firstip": key, "secondip": v} )
	#try to make the path  as  properity
	#session.run('''MATCH (h1: Host{})''')
	listofpath.append(path)
	endt = timeit.default_timer() *1000
	listoftime.append(endt-startt) 
#	print(summary.statement_type)
	#print summary.counters.contains_updates()
					
#for i in listoftime:
#	print i

print sum(listoftime) / float(len(listoftime)) # instead write to file all results
fo = open("gavelresults64.txt", "wb")
for t in listoftime:
	fo.write(str(t)+'\n')
fo.close()



#for path in listofpath:
#	for record in path:
#		print(", ".join("%s: %s" % (key, record[key]) for key in record.keys()))

#query by full node object or string value of ip
# find solution to crusor object

session.close()
