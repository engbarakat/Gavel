from neo4j.v1 import GraphDatabase, basic_auth
from operator import attrgetter

from OFcomposer import *

class NetworkFunction():
	def __init__(self,nfid,listofhostednodes):
		self.listofhostednodes = listofhostednodes
		self.nfid = nfid
	
	#def __init__(self, nfid):
		#self.nfid = nfid;
	
	def setlistofhostednodes(self, listofMBs):
		self.listofhostednodes.extend(listofMBs)
		
	def __str__(self):
		return str(self.listofhostednodes)

class Subpath():
	def __init__(self,switcheslist,portslist,cost,lastnode):
		self.switcheslist = switcheslist
		self.portslist = portslist
		self.cost = cost
		self.lastnode = lastnode
	
	def __str__(self):
		return "The switches list is " + str(self.switcheslist) + "\n the port list is " +  str(self.portslist) +"\n and the cost is "+ str(self.cost)
		

def getsubroute(session, src,srctype, dst,dsttype):
	#print"getting shortest path between " + src +" and "+  dst
	#To Do : check if src and dst are the same thing then return only hte cost of processing.
	#implement cost of processing also.
	if src == dst :
		return Subpath(src,0,0,dst)
		pass
	else:
		if (srctype == 0):
			#print"getting shortest path between " + src +" and "+  dst
			#src is host
			result = session.run('''MATCH (h1:Host {ip:{firstip}}), (h2:Switch {dpid:{secondip}}) Match p=allshortestPaths((h1)-[:Connected_to*]->(h2)) return 
			reduce(cost=0, r in relationships(p) |  cost+r.cost) AS cost ,[n in nodes(p)[1..]| n.dpid] as switches, 
			[r in relationships(p)[1..]| r.port1] as ports , h2.dpid as node order by cost ASC limit 1;''',{"firstip": src, "secondip": dst} )
			for pathins in result:
				return Subpath(pathins["switches"],pathins["ports"],pathins["cost"],pathins["node"])
		elif (dsttype == 0):
			#print"getting shortest path between " + src +" and "+  dst
			#dst is host
			result = session.run('''MATCH (h1:Switch {dpid:{firstip}}), (h2:Host {ip:{secondip}}) Match p=allshortestPaths((h1)-[:Connected_to*]->(h2)) return 
			reduce(cost=0, r in relationships(p) |  cost+r.cost) AS cost ,[n in nodes(p)[1..-1]| n.dpid] as switches, 
			[r in relationships(p)[0..]| r.port1] as ports, h2.ip as node  order by cost ASC limit 1;''',{"firstip": src, "secondip": dst} )
			for pathins in result:
				return Subpath(pathins["switches"],pathins["ports"],pathins["cost"],pathins["node"])
		else:
			#print"getting shortest path between " + src +" and "+  dst
			#src and dst are nodes
			result = session.run('''MATCH (h1:Switch {dpid:{firstip}}), (h2:Switch {dpid:{secondip}}) Match p=allshortestPaths((h1)-[:Connected_to*]->(h2)) return 	reduce(cost=0, r in relationships(p) |  cost+r.cost) AS cost ,
			[n in nodes(p)[1..]| n.dpid] as switches, [r in relationships(p)[0..]| r.port1] as ports, h2.dpid as node order by cost ASC limit 1;''',{"firstip": str(src), "secondip": str(dst)} )
			for pathins in result:
				return Subpath(pathins["switches"],pathins["ports"],pathins["cost"],pathins["node"])
	
def getallhostingSwitches(session,listofFun):
	for fn in listofFun:
		result =  session.run('''Match (s1:Switch)-[hosting_MB]-(mb:MiddleBox{dpid:{fnID}}) return s1 as hosting ''',{"fnID",fn})
		for switches in result:
			fn.setlistofhostednodes(switches["hosting"])
	

def asrroutecalculation(session, srcIP,dstIP,listofFun):
	#Change to New Scheme
	#iterate the list of functions --DONE
	#find the shortest path from src to fn1 --DONE
	#return path and cost --DONE
	#calculate the shortest path from fn1 to fn2 and etc..... --DONE
	#function calculate the cost. -- need to find a way to reflect function processing cost.
	#listofsubpath = []
	fullpath= Subpath([],[],0,"")
	lastvisitednode = None
	#print "Welcome to SFC program: we will traverse three functions each one hostes in some switches:"
	for index in range (len(listofFun)):
		listofsubpath = []
		#print "This is fun No " + str(index) + " " + str(listofFun[index].nfid)
		#print "The list of hosting dpid is :" + str(listofFun[index].listofhostednodes)
		if (index ==0):#if it is the first fn
			for mb in listofFun[index].listofhostednodes:
				##print "It hosted in :" + str 
				a = getsubroute(session, srcIP, 0, mb,1)
				#print "In fn No" + str(listofFun[index].nfid) + "The shortest path is \n " + str(a) + " \nfor node " + mb
				listofsubpath.append(a)
			#for temo in listofsubpath:
				##print temo
			templist = min(listofsubpath,key=attrgetter("cost"))
			fullpath.switcheslist.extend(templist.switcheslist)
			fullpath.portslist.extend(templist.portslist)
			fullpath.cost += templist.cost
			fullpath.lastnode = templist.lastnode
			##print fullpath
			##print templist.switcheslist
			lastvisitednode = fullpath.lastnode # to get last visited node
			#print "the last visited node after fn 100 is " + str (lastvisitednode)
		elif(listofFun[index]==listofFun[-1]):#if it is the last fn
			for mb in listofFun[index].listofhostednodes:
				a = getsubroute(session, lastvisitednode, 1, mb,1)
				listofsubpath.append(a) #fix how to get the last node before asking for subpath
				#print "In fn No " + str(listofFun[index].nfid) +  " for node " + mb +" The shortest path is \n" + str(a) 
			templist = min(listofsubpath,key=attrgetter('cost'))
			fullpath.switcheslist.extend(templist.switcheslist)
			fullpath.portslist.extend(templist.portslist)
			fullpath.cost += templist.cost
			fullpath.lastnode = templist.lastnode
			lastvisitednode = fullpath.lastnode
		else:
			for mb in listofFun[index].listofhostednodes:
				##print lastvisitednode, listofFun[index]
				a = getsubroute(session, lastvisitednode, 1, mb,1)
				listofsubpath.append(a) #fix how to get the last node before asking for subpath
				#print "In fn No " + str(listofFun[index].nfid) +  "for node " + mb +" The shortest path is \n" + str(a) 
			#for mo in listofsubpath:
				##print mo
			templist = min(listofsubpath,key=attrgetter('cost'))
			fullpath.switcheslist.extend(templist.switcheslist)
			fullpath.portslist.extend(templist.portslist)
			fullpath.cost += templist.cost
			fullpath.lastnode = templist.lastnode
			#print templist.lastnode
			lastvisitednode = fullpath.lastnode #to get last visited node
	#now get the path from last MB to dstIP
	tempsubpath = getsubroute(session, lastvisitednode, 1, dstIP,0)
	fullpath.switcheslist.extend(tempsubpath.switcheslist)
	fullpath.portslist.extend(tempsubpath.portslist)
	fullpath.cost += tempsubpath.cost
	installpathasr(session,fullpath,srcIP,dstIP)
	updatelinkcost(session,srcIP,dstIP,fullpath)

def installpathasr(session, path, srcIP,dstIP):
	#TODO  1. change cost of the all relationships
	result = session.run('''MATCH (h1:Host {ip:{firstip}}), (h2:Host {ip:{secondip}})
	create (h1)-[pa:SFC_Path{switches:{listofswitches}, ports:{listofports}, SFCID:{sfcid}, cost:{cost}}]->(h2) 
	return pa.cost;''',{"firstip": srcIP, "secondip": dstIP, "listofswitches":path.switcheslist, "listofports":path.portslist, "sfcid": srcIP, "cost": path.cost} )
	#for pathins in result:
		#msgOF("installflow",pathins["pa.switches"],pathins["pa.ports"])#do i need to send some special msg to  switch for the sfc traffic
		#return True 	

def updatelinkcost(session, srcIP, dstIP, path):
	#print path.switcheslist
	#path.switcheslist[0].encode('ascii','ignore')
	#print type(path.switcheslist[0].encode('ascii','ignore'))
	result = session.run('''MATCH (h1:Host {ip:{firstip}})-[r]-> (h2:Switch {dpid:{secondip}}) set r.cost = r.cost+1;''',{"firstip": srcIP, "secondip": path.switcheslist[0]})
	for index in xrange (1,len(path.switcheslist),1):
		if (index==len(path.switcheslist)-1):
			result = session.run('''MATCH (h1:Switch {dpid:{firstip}})-[r]-> (h2:Host {ip:{secondip}}) set r.cost = r.cost+1;''',{"firstip": path.switcheslist[-1], "secondip": dstIP})
		else:
			result = session.run('''MATCH (h1:Switch {dpid:{firstip}})-[r]-> (h2:Switch {dpid:{secondip}}) set r.cost = r.cost+1;''',{"firstip": path.switcheslist[index], "secondip": path.switcheslist[index+1]})
	
				
		
