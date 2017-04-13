def installpathofmsg(dpid,fport,bport,srcIP,dstIP):
	pass
def deletepathofmsg(dpid,fport,bport,srcIP,dstIP):
	pass
def drophostofmsg(dpid,hostIP):
	pass
def undrophostofmsg(dpid,hostIP):
	pass

def installpath(**kwargs):#switches = pathins["pa.switches"],portsforward = pathins["pa.ports"],portsbackward = None , src = srcIP, dst =dstIP
	for switch, fport,bport in zip(kwargs['switches'],kwargs['portsforward'],kwargs['portsbackward']):
		print "install path now in {0}, with fport {1}, and backport {2}".format(switch,fport,bport)
		installpathofmsg(switch,fport,bport,kwargs['src'],kwargs['dst']) 
	

def deletepath(**kwargs):
	for switch, fport,bport in zip(kwargs['switches'],kwargs['portsforward'],kwargs['portsbackward']):
		print "install path now in {0}, with fport {1}, and backport {2}".format(switch,fport,bport)
		deletepathofmsg(switch,fport,bport,kwargs['src'],kwargs['dst'])

def blockhost(**kwargs):
	for switch in kwargs['switch']:
		drophostofmsg(switch, kwargs['blockedHost'])

def unblockhost(**kwargs):
	for switch in kwargs['switch']:
		undrophostofmsg(switch, kwargs['blockedHost'])

def blockpath(**kwargs):
	pass

def unblockpath(**kwargs):
	pass
def installsfc(**kwargs):
	pass


def msgOF(msgtosend,**kwargs):
	options = {'installflow':installpath,
			   'deleteflow':deletepath,
			   'blockHost':blockhost,
			   'unblockHost':unblockhost,
			   'blockPath':blockpath,
			   'unblockPath':unblockpath,
			   'installsfc':installsfc
			
			}
	options[msgtosend](**kwargs)
	#print msgtosend + " OF message sent !"
	#installpath will do it into two directions
	pass


