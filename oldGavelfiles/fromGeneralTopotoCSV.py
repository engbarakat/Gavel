#this code should convert any topology to csv files which make it easy to import by graph database.

from DeutscheTelekom import * # import the topology file here 
import csv

def exporttocsv(size):
	gentopo = GeneratedTopo() # call your lamda function to create the topology objects
	print  (gentopo.links())
	for s,e in gentopo.switchList.iteritems():
			gentopo.switchList[s] = {'id': s, 'layer': e['layer'], 'dpid': e['dpid']}
			print gentopo.switchList[s]
	for s,e in gentopo.hostList.iteritems():
			gentopo.hostList[s] = {'id': s, 'layer': e['layer'], 'dpid': e['dpid'], 'ip': e['ip'], 'mac':e['mac']}
	
	
	# start with switch_to relationship between switches
	with open('switched_to%s.csv'%size, 'w') as csvfile:
		fieldnamesa = ['node1', 'node2', 'port1', 'port2']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnamesa)					
		writer.writeheader()
		for r in gentopo.links(False,False,True):
			if  r[0] in gentopo.switchList and r[1] in gentopo.switchList:
					writer.writerow(r[2])	
	
	with open('connected_to%s.csv'%size, 'w') as csvfile:
		fieldnamesa = ['node1', 'node2', 'port1', 'port2']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnamesa)					
		writer.writeheader()
		for r in gentopo.links(False,False,True):
			if  r[0] in gentopo.hostList: 
				writer.writerow(r[2])
			if r[1] in gentopo.hostList:
				writer.writerow(r[2])
	
	with open('switches%s.csv'%size, 'w') as csvfile:
		fieldnames = ['id','layer', 'dpid']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		for s,e in gentopo.switchList.iteritems():
			writer.writerow(e)
	
	with open('hosts%s.csv'%size, 'w') as csvfile:
		fieldnames = ['id', 'ip', 'layer', 'mac', 'dpid']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		for s,e in gentopo.hostList.iteritems():
			writer.writerow(e)
	


	
	
exporttocsv('DT')
