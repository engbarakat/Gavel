from dcttopo import *
import csv

def exporttocsv(size):
	fattopo = FatTreeTopo(size)
	for s,e in fattopo.coreSwitches.iteritems():
			fattopo.coreSwitches[s] = {'id': s, 'layer': e['layer'], 'dpid': e['dpid']}
	for s,e in fattopo.aggrSwitches.iteritems():
		fattopo.aggrSwitches[s] = {'id': s, 'layer': e['layer'], 'dpid': e['dpid']}
	for s,e in fattopo.edgeSwitches.iteritems():
			fattopo.edgeSwitches[s] = {'id': s, 'layer': e['layer'], 'dpid': e['dpid']}
	for s,e in fattopo.hostList.iteritems():
			fattopo.hostList[s] = {'id': s, 'layer': e['layer'], 'dpid': e['dpid'], 'ip': e['ip'], 'mac':e['mac']}
	with open('switched_to%d.csv'%size, 'w') as csvfile:
		fieldnamesa = ['node1', 'node2', 'port1', 'port2']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnamesa)					
		writer.writeheader()
		for r in fattopo.links(False,False,True):
			if  r[0] not in fattopo.hostList:
				if r[1] not in fattopo.hostList:
					writer.writerow(r[2])
	with open('connected_to%d.csv'%size, 'w') as csvfile:
		fieldnamesa = ['node1', 'node2', 'port1', 'port2']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnamesa)					
		writer.writeheader()
		for r in fattopo.links(False,False,True):
			if  r[0] in fattopo.hostList or r[1] in fattopo.hostList:
					writer.writerow(r[2])	
	with open('switches%d.csv'%size, 'w') as csvfile:
		fieldnames = ['id','layer', 'dpid']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		for s,e in fattopo.coreSwitches.iteritems():
			writer.writerow(e)
		for s,e in fattopo.aggrSwitches.iteritems():
			writer.writerow(e)
		for s,e in fattopo.edgeSwitches.iteritems():
			writer.writerow(e)
	with open('hosts%d.csv'%size, 'w') as csvfile:
		fieldnames = ['id', 'ip', 'layer', 'mac', 'dpid']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		for s,e in fattopo.hostList.iteritems():
			writer.writerow(e)
	'''with open('switchto%d.csv'%size, 'w') as csvfile:
		fieldnames = ['ip', 'layer', 'mac', 'dpid']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		for s,e in fattopo.hostList.iteritems():
			writer.writerow(e)'''

		
	
	
	
	
	
	
for n in [4,8,16,32,64]:
	exporttocsv(n)
