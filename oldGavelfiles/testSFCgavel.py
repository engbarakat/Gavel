from neo4j.v1 import GraphDatabase, basic_auth
from firewall import *
from route import *
from loadbalancer import *
from ASRroute import *
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
	
	
	
	hostlistready = {}
	listoftimea = []
	listoftimeb = []
	result = session.run('''Match (h:Switch) return h.dpid AS dpid ''')
	resultlistnotrandom = list(result)
	resultlist = random.sample(resultlistnotrandom,9)
	NFone = NetworkFunction(100,[resultlist[0]["dpid"],resultlist[4]["dpid"],resultlist[3]["dpid"]])
	NFtwo = NetworkFunction(200,[resultlist[7]["dpid"],resultlist[2]["dpid"],resultlist[1]["dpid"]])
	NFthree = NetworkFunction(300,[resultlist[8]["dpid"],resultlist[6]["dpid"],resultlist[5]["dpid"]])
	listofSFC = [NFone,NFtwo,NFthree]
	
	result = session.run('''Match (h:Host) return h.ip AS ip ''')
	resultlistnotrandom = list(result)
	resultlist = random.sample(resultlistnotrandom,20)
	#print resultlist
	#resultlist = list(result)

	for n in xrange(0,len(resultlist), 2):
		hostlistready[resultlist[n]["ip"]] = resultlist[n+1]["ip"]

	for key,v in hostlistready.iteritems():
		#print key, v
		astartt = timeit.default_timer() *1000
		asrroutecalculation(session, key,v,listofSFC)
		aendt = timeit.default_timer() *1000
		
#		bstartt = timeit.default_timer() *1000
#		for path in result:
#			#print path['switch'], path['port']
#			result = session.run('''Create (p1:Path{from:{firstip}, to:{secondip}, switches:{nodelist}, ports:{relslist}});''',{"firstip": key, "secondip": v, "nodelist":path['switch'],"relslist":path["port"]} )
#		bendt = timeit.default_timer() *1000
		path = Path(key,v,aendt-astartt,0)
		listofpath.append(path)
		########################################################################################################

	
	session.close()

def writeresults(sizeoffattree,listofpath):	
	fo = open("JournalGavel%sSFC.txt" %sizeoffattree, "wb")
	for a in listofpath:
		fo.write(str(a.host1)+'\t'+str(a.host2) + '\t'+str(a.getpath)+'\t'+str(a.writepath) + '\n')
	fo.close()
def plotresults(k):
	os.system("gnuplot plotresults%d.gplt" %k)

listofpadth=[]
#NFone = NetworkFunction(100,[('0000000000000401',1),('0000000000001d01',2),('0000000000002401',4)])
#NFtwo = NetworkFunction(200,[('0000000000001b01',11),('0000000000001901',9),('0000000000002601',6)])
#NFthree = NetworkFunction(300,[('0000000000000e01',12),('0000000000001601',6),('0000000000001001',10)])
 
for s in ['Geant2012']:
	listofpath=[]
	loadftgdb(s)
	for i in range(1):
		runthetest(s,i,listofpath)
	writeresults(s,listofpath)
	#writeresultsPats(s,listofpath)
	#plotresults(s)
