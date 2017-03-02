from neo4j.v1 import GraphDatabase, basic_auth
from collections import deque
from OFcomposer import *
from route import *


	

class Loadbalancer():
	def __init__(self,listofservers,lbIP):
		self.listofserverIPs = deque(listofservers)
		self.lbIP = lbIP
	
	def getnextavailableserver(self):
		self.listofserverIPs.rotate(1)
		return self.listofserverIPs[0]
	def initconnectwithGDB(self):
		driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "ravel"))
		self.session = driver.session()
		self.session.run('''match (n)-[r]-() return count(n)''')
		
	
	def installroutewithlb(self,srcIP):
		self.initconnectwithGDB()
		dstIP = self.getnextavailableserver()
		return getroute(self.session, srcIP, dstIP)
	
	def installroutewithlbonlycypher(self, srcIP):
		# get shortest path 
		pass
		 
		
		
		








