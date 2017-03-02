from neo4j.v1 import GraphDatabase, basic_auth
from firewall import *
from route import *
from loadbalancer import *
import timeit
import random
import itertools
import os
import math

listofblockhosttime = []
listofblockpathtime = []

def ceildiv(a, b):
    return -(-a // b)
    
class resultofblockedhost():
	def __init__(self, hostIP, timetoblock, timetounblock):
		self.hostIP = hostIP
		self.timetoblock = timetoblock
		self.timetounblock = timetounblock

class resultofblockedpath():
	def __init__(self, hostIP, dstIP, timetoblock, timetounblock):
		self.hostIP = hostIP
		self.timetoblock = timetoblock
		self.timetounblock = timetounblock
		self.dstIP = dstIP

def loadftgdb(sizeoffattree):
	print ">>>>>>>neo4j-shell -file new_gdb%s.cypher -host localhost -v" %sizeoffattree
	os.system("neo4j-shell -file new_gdb%s.cypher -host localhost -v" %sizeoffattree)

def runthetest(sizeoffattree,itera,listofpath):
	print ">>>>>>>start the test with size of %s for the time No.%d" %(sizeoffattree,itera)
	driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "ravel"))
	session = driver.session()
	#session.run('''match (n)-[r]-() return count(n)''')
	
	#1. Test blockhost
	pathhostlist = []
	
	
	result = session.run('''Match (h:Host) return h.ip AS ip ''')
	resultlistnotrandom = list(result)
	if len(resultlistnotrandom) < 600:
		for n in range(600/len(resultlistnotrandom)+1):
			#print n
			resultlistnotrandom.extend(resultlistnotrandom)
	#print len(resultlistnotrandom)
	resultlist = random.sample(resultlistnotrandom,600)
	
	
	
	for n in xrange(0,len(resultlist), 2):
		pathhostlist.append ((resultlist[n]["ip"] , resultlist[n+1]["ip"]))

	print len(pathhostlist)
	for host in resultlist:
		astartt = timeit.default_timer() *1000
		blockHost(session, host["ip"])
		aendt = timeit.default_timer() *1000
		bstartt = timeit.default_timer() *1000
		unblockHost(session, host["ip"])
		bendt = timeit.default_timer() *1000
		astartt = timeit.default_timer() *1000
		blockHost(session, host["ip"])
		aendt = timeit.default_timer() *1000
		bstartt = timeit.default_timer() *1000
		unblockHost(session, host["ip"])
		bendt = timeit.default_timer() *1000
		listofblockhosttime.append(resultofblockedhost(host["ip"],aendt-astartt,bendt-bstartt))
		
	for pair in pathhostlist:
		#print pair, pair[0], pair[1]
		astartt = timeit.default_timer() *1000
		blockPath(session,pair[0],pair[1])
		aendt = timeit.default_timer() *1000
		bstartt = timeit.default_timer() *1000
		unblockPath(session,pair[0],pair[1])
		bendt = timeit.default_timer() *1000
		astartt = timeit.default_timer() *1000
		blockPath(session,pair[0],pair[1])
		aendt = timeit.default_timer() *1000
		bstartt = timeit.default_timer() *1000
		unblockPath(session,pair[0],pair[1])
		bendt = timeit.default_timer() *1000
		listofblockpathtime.append(resultofblockedpath(pair[0],pair[1], aendt-astartt,bendt-bstartt))
	
	
	session.close()

def writeresultsHosts(sizeoffattree,listofpath):	
	fo = open("newgavel1.3results%sallblockHost.txt" %sizeoffattree, "wb")
	for a in listofblockhosttime:
		fo.write(str(a.hostIP)+'\t'+str(a.timetoblock) + '\t'+str(a.timetounblock) + '\n')
	fo.close()
	
def writeresultsPats(sizeoffattree,listofpath):	
	fo = open("newgavel1.3results%sallBlockpath.txt" %sizeoffattree, "wb")
	for a in listofblockpathtime:
		fo.write(str(a.hostIP)+'\t'+str(a.dstIP) + '\t'+str(a.timetoblock)+'\t'+str(a.timetounblock) + '\n')
	fo.close()
def plotresults(k):
	os.system("gnuplot plotresults%d.gplt" %k)

listofpadth=[]
for s in ['Geant2012','DT','16','32','64']:
	listofpath=[]
	loadftgdb(s)
	for i in range(1):
		runthetest(s,i,listofpath)
	writeresultsHosts(s,listofpath)
	writeresultsPats(s,listofpath)
	#plotresults(s)
