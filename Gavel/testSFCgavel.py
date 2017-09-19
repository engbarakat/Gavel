from neo4j.v1 import GraphDatabase, basic_auth
from firewall import *
from route import *
#from loadbalancer import *
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
	
def installMBs(session, Switches, numberofMBs):
	#get random number of random switches to host each MB
	#1. create MBs and return their dpid in list--create node
	#2. for every MB select random no. of host and then select radnomly the same number of swich
	#3. associate the MB with the choosen switch.
	listofMBs = []
	for x in range(numberofMBs):
		session.run('''CREATE (:MiddelBox {id: {MBid}, dpid: {MBdpid} });''',{"MBid":str(x),"MBdpid":"mb30"+str(x)})
# 		NoofHosts =random.randint(2,3)
		#print NoofHosts
		NoofHosts =2
		switchlist =  random.sample(Switches,NoofHosts)
		session.run('''Match (m:MiddelBox{dpid: {MBdpid}}) Match (s:Switch) where s.dpid in {slist} 
		MERGE (m)-[r:Hosts]-(s) ON CREATE SET r.cost= {scostmb};''',{"MBdpid":"mb30"+str(x),"slist":switchlist,"scostmb":random.randint(2,9)})
		listofMBs.append(NetworkFunction("mb30"+str(x),switchlist))
	return listofMBs

def clearallMBs(session):
	session.run('''Match (m:MiddelBox) detach delete m;''')
def runthetest(sizeoffattree,itera,listofpathforallMBs):
	listofpath = []
	print ">>>>>>>start the test with size of %s for the time No.%d" %(sizeoffattree,itera)
	driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "gavel"))
	session = driver.session()
	session.run('''match (n)-[r]-() return count(n)''')
	
	
	
	hostlistready = {}
	listoftimea = []
	listoftimeb = []
	result = session.run('''Match (h:Switch) return h.dpid AS dpid ''')
	resultlistnotrandom = list(result)
	switchlist = []
	resultlist = []
	for s in resultlistnotrandom:
		switchlist.append(s["dpid"])
	#print switchlist
	'''resultlist = random.sample(resultlistnotrandom,9)
	NFone = NetworkFunction(100,[resultlist[0]["dpid"],resultlist[4]["dpid"],resultlist[3]["dpid"]])
	NFtwo = NetworkFunction(200,[resultlist[7]["dpid"],resultlist[2]["dpid"],resultlist[1]["dpid"]])
	NFthree = NetworkFunction(300,[resultlist[8]["dpid"],resultlist[6]["dpid"],resultlist[5]["dpid"]])'''
	#numberofMBs = 4
	for numberofMBs in range(3,8):
		listofpath = []
		clearallMBs(session)
		listofSFC = installMBs(session, switchlist, numberofMBs)
		print listofSFC
		result = session.run('''Match (h:Host) return h.ip AS ip ''')
		resultlistnotrandom = list(result)
		hostsnumberpossible = [n for n in xrange(2,len(resultlistnotrandom), 2)]
		for h in random.sample(resultlistnotrandom,random.sample(hostsnumberpossible,1)[0]):
			resultlist.append(h)
		#resultlist = random.sample(resultlistnotrandom,20)
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
			listofpathforallMBs[numberofMBs]= listofpath
		########################################################################################################

	
	

def writeresults(sizeoffattree,listofpath):	
	fo = open("JournalGavel%sSFC.txt" %sizeoffattree, "wb")
	for mbnumber in listofpath:
		for a in listofpath[mbnumber]:
			fo.write(str(a.host1)+'\t'+str(a.host2) + '\t'+str(a.getpath)+'\t'+str(a.writepath) +'\t'+str(mbnumber)+ '\n')
	fo.close()
def plotresults(k):
	os.system("gnuplot plotresults%d.gplt" %k)

listofpadth=[]
#NFone = NetworkFunction(100,[('0000000000000401',1),('0000000000001d01',2),('0000000000002401',4)])
#NFtwo = NetworkFunction(200,[('0000000000001b01',11),('0000000000001901',9),('0000000000002601',6)])
#NFthree = NetworkFunction(300,[('0000000000000e01',12),('0000000000001601',6),('0000000000001001',10)])
 
for s in ['Geant2012']:
	listofpathforallMBs={}
	loadftgdb(s)
	for i in range(1):
		runthetest(s,i,listofpathforallMBs)
	writeresults(s,listofpathforallMBs)
	#writeresultsPats(s,listofpath)
	#plotresults(s)
