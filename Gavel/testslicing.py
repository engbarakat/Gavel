from neo4j.v1 import GraphDatabase, basic_auth
import timeit
import random
import itertools
import os
from slicermanager import *
from route import *

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
        
    
    
def createslice(session,size,allhosts,allswitches):
    hostsnumberpossible = [n for n in xrange(2,len(allhosts), 2)]
    switchnumerpossible = [n for n in range(1,len(allswitches))]
    
    hoststobeadded = []
    switchestobeadded = []
    
    for h in random.sample(allhosts,random.sample(hostsnumberpossible,1)[0]):
        hoststobeadded.append(h)
    
    #switchnumerpossible = [n for n in range(5,len(allswitches))]
    switchnumerpossible = [25]
    
    for h in random.sample(allswitches,random.sample(switchnumerpossible,1)[0]):
        switchestobeadded.append(h)
    
    Createslicegavel(session,switchestobeadded, allhosts,str(size))
    print ("** The slice No. {2} with {0} hosts and {1} switch was created\n").format(len(hoststobeadded),len(switchestobeadded),size)
    return Slice(hoststobeadded,switchestobeadded,str(size))
    
def createslicemodified(session,size,allhosts,allswitches):
    Createslicegavel(session,allswitches, allhosts,str(size))
    print ("** The slice No. {2} with {0} hosts and {1} switch was created\n").format(len(allhosts),len(allswitches),size)
    return Slice(allhosts,allswitches,str(size))

def deleteallslices(session):
    session.run('''match (n:Slice) detach delete n''')

def gethostsfromslice(slice):
    hostsinslice = {}
    for n in xrange(0,len(slice.hosts), 2):
        hostsinslice[slice.hosts[n]] = slice.hosts[n+1]
    return hostsinslice

def clearallinstalledpaths(session):
    session.run('''match ()-[r:PathSlice_to]-() delete r''')
    session.run('''match ()-[r:Path]-() delete r''')
        

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
    avgroutingdict = {}
    avgroutinglistperslice=[]
    hoststoroute= []
    listofzerocounted = []
    switchesinslice= []
    
    result = session.run('''Match (h:Host) return h.ip AS ip ''')
    for host in result:
        allhosts.append(host["ip"])
    
    print ("Total hosts fetched are {0}").format(len(allhosts))
    result = session.run('''Match (s:Switch) return s.dpid AS dpid ''')
    for host in result:
        allswitches.append(host["dpid"])
    print ("Total Switches fetched are {0}").format(len(allswitches))
    print "Now we are running in slice No. 0 \n"
    hostlistready = {}
    hostsnumberpossiblezeroslice = [n for n in xrange(2, len(allhosts), 2)]
    
    for h in random.sample(allhosts, random.sample(hostsnumberpossiblezeroslice, 1)[0]):
        hoststoroute.append(h)
    print "For slice No. {0} the route test done between {1} hosts".format("0", len(hoststoroute))  
    for n in xrange(0, len(hoststoroute), 2):
        hostlistready[hoststoroute[n]] = hoststoroute[n + 1]
 
    for key, v in hostlistready.iteritems():
        astartt = timeit.default_timer() * 1000
        result = getroute(key, v, session)
        if (result!= False):
            aendt = timeit.default_timer() * 1000
            switchesinslice.extend(result)
            avgroutinglistperslice.append(aendt - astartt)
            path = Path(key, v, aendt - astartt, 0)
            listofpath.append(path)
#     if len(avgroutinglistperslice) > 0:
#         avgroutingdict[0] = sum(avgroutinglistperslice) / float(len(avgroutinglistperslice))
#     else:
#         avgroutingdict[0] = 0
#     zeroinlist = {0:len(avgroutinglistperslice)}
#     listofzerocounted.append(zeroinlist.copy())
#     #print len(avgroutinglistperslice)
#     del avgroutinglistperslice[:]
    
    for slicesize in range(1,10,1):
        clearallinstalledpaths(session)
        #delete all existing slices
        #deleteallslices(session)
        listofslices.append( createslicemodified(session, slicesize,hoststoroute,allswitches))
            
        for slice in listofslices:
            hostlistinslice =  gethostsfromslice(slice)#hostlist should be ready for routing function process
                #print "Testing routing with   {0} slices  between {1} hosts".format(slicesize, len(slice.hosts))
            for h1,h2 in hostlistinslice.iteritems():
                    
                starttime = timeit.default_timer()*1000
                result = getroute(h1, h2, session)
                endtime = timeit.default_timer()*1000
                if (result!= False):
                    path = Path(h1,h2,endtime-starttime,slicesize)
                    #avgroutinglistperslice.append(endtime-starttime)#how to append to multidimention array
                    listofpath.append(path)
                else:
                    print "failing path at slice size {}".format(slice.name)


def writeresults(sizeoffattree,listofpath):    
    fo = open("JournalGavel%sslice.txt" %sizeoffattree, "wb")
    for a in listofpath:
        fo.write(str(a.host1)+'\t'+str(a.host2) + '\t'+str(a.getpath)+'\t'+str(a.slicesize)+'\n')
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
