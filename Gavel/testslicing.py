from neo4j.v1 import GraphDatabase, basic_auth
import timeit
import random
import itertools
import os
from slicermanager import *
from __main__ import name

class Path:
    def __init__(self,host1, host2, getpath, size):
        self.host1 = host1
        self.host2 = host2
        self.getpath = getpath
        self.slicesize = size

class Slice:
    def __init__(self,hosts,switches,name):
        self.hosts = hosts
        self.switches = switches
        self.name = name
        
    
    
def createslice(size,allhosts,allswitches):
    hostsnumberpossible = xrange(1,len(allhosts), 2)
    switchnumerpossible = xrange(1,len(allswitches), 2)
    
    hoststobeadded = []
    switchestobeadded = []
    
    for h in random.sample(allhosts,random.sample(hostsnumberpossible,1)):
        hoststobeadded.append(h)
    for h in random.sample(allswitches,random.sample(switchnumerpossible,1)):
        switchestobeadded.append(h)
    
    Createslice(session,switchestobeadded, hoststobeadded,str(size))
    return Slice(hoststobeadded,switchestobeadded,str(size))
    
def selecthostsfromslice(slice):
    hostsinslice = []
    for n in xrange(0,len(slice.hosts), 2):
        hostsinslice[hosts[n]] = hosts[n+1]
        return hostsinslice
def clearallinstalledpaths(session):
    pass    

def loadftgdb(sizeoffattree):
    print ">>>>>>>neo4j-shell -file new_gdb%s.cypher -host localhost -v" %sizeoffattree
    os.system("neo4j-shell -file new_gdb%s.cypher -host localhost -v" %sizeoffattree)

def runthetest(topologyname,itera,listofpath):
    print ">>>>>>>start the test with size of %s for the time No.%d" %(topologyname,itera)
    driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "gavel"))
    session = driver.session()
    session.run('''match (n)-[r]-() return count(n)''')
    listofslices = []
    allhosts = []
    allswitches = []
    
    result = session.run('''Match (h:Host) return h.ip AS ip ''')
    for host in result:
        allhosts.append(host["ip"])
    
    result = session.run('''Match (s:Switch) return s.dpid AS dpid ''')
    for host in result:
        allswitches.append(host["dpid"])
    
    for slicesize in range(21):
        listofslices.append( createslice(slicesize,allhosts,allswitches))
        clearallinstalledpath(session)
        for slice in listofslices:
            hostlistinslice =  selecthostsfromslice(slice)#hostlist should be ready for routing function process
            for h1,h2 in hostlistinslice.iteritems():
                starttime = timeit.default_timer()*1000
                Routeinslice(session, h1,h2,slice.name)
                endtime = timeit.default_timer()*1000
                path = Path(key,v,endtime-starttime,slicesize)
                listofpath.append(path)
    
    
    
    
    hostlistready = {}
    listoftimea = []
    listoftimeb = []
    switchlist= ["0000000000001701","0000000000001d01","0000000000001c01","0000000000001b01","0000000000001601","0000000000001a01"]
    hostlist= ["10.3.29.30","10.3.26.27"]
    result = session.run('''Match (h:Switch) return h.dpid AS dpid ''')
    resultlistnotrandom = list(result)
    for x in random.sample(resultlistnotrandom,38):
        switchlist.append(x["dpid"]) 
     
     
    result = session.run('''Match (h:Host) return h.ip AS ip ''')
    resultlistnotrandom = list(result)
    for h in random.sample(resultlistnotrandom,10):
        hostlist.append(h["ip"]) 
#     print switchlist,hostlist
    Createslice(session,switchlist, hostlist,"Osamah")
    #print resultlist
    #resultlist = list(result)

    for n in xrange(0,len(hostlist), 2):
        hostlistready[hostlist[n]] = hostlist[n+1]

    for key,v in hostlistready.iteritems():
        #print key, v
        astartt = timeit.default_timer() *1000
        Routeinslice(session,key,v,"slice")
        aendt = timeit.default_timer() *1000
        path = Path(key,v,aendt-astartt,0)
        listofpath.append(path)
        ########################################################################################################

def writeresults(sizeoffattree,listofpath):    
    fo = open("JournalGavel%sslice.txt" %sizeoffattree, "wb")
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
    #writeresults(s,listofpath)
    #writeresultsPats(s,listofpath)
    #plotresults(s)
