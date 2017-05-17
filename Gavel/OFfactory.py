from mininet.net import macColonHex, netParse, ipAdd
import os
import sys
import subprocess
from updateGavel import getswtichname

OFPC_FLOW_STATS = 1
OFPC_TABLE_STATS = 2
OFPC_PORT_STATS = 4

OFPFC_ADD = 0
OFPFC_MODIFY = 1
OFPFC_MODIFY_STRICT = 2
OFPFC_DELETE = 3
OFPFC_DELETE_STRICT = 4

OFPP_MAX = 65280
OFPP_IN_PORT = 65528
OFPP_TABLE = 65529
OFPP_NORMA = 65530
OFPP_FLOOD = 65531
OFPP_ALL = 65532
OFPP_CONTROLLER = 65533
OFPP_LOCAL = 65534
OFPP_NONE = 65535


class Switch ():
    def __init__(self,dpid):
        self.dpid = dpid
        self.name = getswtichname(dpid)
        
class Match(object):
    "A match object for an OpenFlow flow modification message"

    def __init__(self, nw_src=None, nw_dst=None,
                dl_src=None, dl_dst=None, dl_type=None):
       """nw_src: the source node's network address
          nw_dst: the destination node's network address
          dl_src: the source node's datalink address
          dl_dst: the destination node's datalink address
          dl_type: the datalink type"""
       self.nw_src = nw_src
       self.nw_dst = nw_dst
       self.dl_src = dl_src
       self.dl_dst = dl_dst
       self.dl_type = dl_type

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "[{0},{1},{2},{3},{4}]".format(self.nw_src,
                                              self.nw_dst,
                                              self.dl_src,
                                              self.dl_dst,
                                              self.dl_type)
#TODO: 1. Match class writing
class OfMessage():#from ravel
    "A OpenFlow flow modification message"

    def __init__(self, command=None, priority=1, switch=None,
                 match=None, actions=None):
        """command: an OpenFlow flow modification command
           priority: the flow priority
           switch: the switch to send the message
           match: a match for the flow
           actions: a list of ports to forward matching packets"""
        self.command = command
        self.priority = priority
        self.switch = Switch(switch)
        self.match = match
        self.actions = actions
        if actions is None:
            self.actions = []

    def consume(self, consumer):
        """Consume the message
           consumer: a ravel.of.OfManager instance to consume the message"""
        consumer.sendFlowmod(self)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "{0}: {1} {2}".format(self.command,
                                     self.switch,
                                     self.match)

class BarrierMessage():
    """An OpenFlow barrier message"""

    def __init__(self, dpid):
        "dpid: the dpid of the switch to send the barrier message"
        self.dpid = dpid

    def consume(self, consumer):
        """Consume the message
           consumer: a ravel.of.OfManager instance to consume the message"""
        consumer.sendBarrier(self.dpid)
 

class OvsSender():#from ravel
    "A message sender using ovs-ofctl to communicate with switches"

    command = "/usr/bin/sudo /usr/bin/ovs-ofctl"
    subcmds = { OFPFC_ADD : "add-flow",
                OFPFC_DELETE : "del-flows",
                OFPFC_DELETE_STRICT : "--strict del-flows"
    }

    def __init__(self):
        pass

    def send(self, msg):
        """Send the specified OpenFlow message
           msg: the message to send"""

        # don't need to handle barrier messages
        if not hasattr(msg, 'command'):
            return

        subcmd = OvsSender.subcmds[msg.command]
        

        # TODO: this is different for remote switches (ie, on physical network)
        dest = msg.switch.name

        params = []
        if msg.match.nw_src is not None:
            params.append("nw_src={0}".format(msg.match.nw_src))
        if msg.match.nw_dst is not None:
            params.append("nw_dst={0}".format(msg.match.nw_dst))
        if msg.match.dl_src is not None:
            params.append("dl_src={0}".format(msg.match.dl_src))
        if msg.match.dl_dst is not None:
            params.append("dl_dst={0}".format(msg.match.dl_dst))
        if msg.match.dl_type is not None:
            params.append("dl_type={0}".format(msg.match.dl_type))

        params.append("priority={0}".format(msg.priority))
        actions = ["flood" if a == OFPP_FLOOD else str(a) for a in msg.actions]

        if msg.command == OFPFC_ADD:
            params.append("action=output:" + ",".join(actions))

        paramstr = ",".join(params)
        cmd = "{0} {1} {2} {3}".format(OvsSender.command,
                                       subcmd,
                                       dest,
                                       paramstr)
        ret = os.system(cmd)
        return ret


def _send_msg(command,  sw, src_ip, src_mac, dst_ip, dst_mac, outport, revoutport):#from Ravel, used to send any msg based on the channel, I use here only OVS channel
    conn = OvsSender()
    msg1 = OfMessage(command=command,
                     priority=10,
                     switch=sw,
                     match=Match(nw_src=src_ip, nw_dst=dst_ip, dl_type=0x0800),
                     actions=[outport])

    msg2 = OfMessage(command=command,
                     priority=10,
                     switch=sw,
                     match=Match(nw_src=dst_ip, nw_dst=src_ip, dl_type=0x0800),
                     actions=[revoutport])

    arp1 = OfMessage(command=command,
                     priority=1,
                     switch=sw,
                     match=Match(dl_src=src_mac, dl_type=0x0806),
                     actions=[OFPP_FLOOD])

    arp2 = OfMessage(command=command,
                     priority=1,
                     switch=sw,
                     match=Match(dl_src=dst_mac, dl_type=0x0806),
                     actions=[OFPP_FLOOD])

    conn.send(msg1)
    conn.send(msg2)
    conn.send(arp1)
    conn.send(arp2)
    conn.send(BarrierMessage(sw))

def installpathofmsg(dpid,fport,bport,srcIP,dstIP,srcMAC,dstMAC):
    _send_msg(OFPFC_ADD, dpid, srcIP, srcMAC, dstIP, dstMAC, fport, bport)
    
def deletepathofmsg(dpid,fport,bport,srcIP,dstIP,srcMAC,dstMAC):
    _send_msg(OFPFC_DELETE_STRICT, dpid, srcIP, srcMAC, dstIP, dstMAC, fport, bport)
    
def drophostofmsg(dpid,hostIP,hostMAC):
    _send_msg(OFPP_NONE, dpid, srcIP, srcMAC, dstIP, dstMAC, fport, bport)
    
def undrophostofmsg(dpid,hostIP,hostMAC):
    _send_msg(OFPFC_ADD, dpid, srcIP, srcMAC, dstIP, dstMAC, fport, bport)
    

def droppathofmsg(dpid,srcIP,dstIP,srcMAC,dstMAC):
    _send_msg(OFPP_NONE, dpid, srcIP, srcMAC, dstIP, dstMAC, fport, bport)
def undroppathofmsg(dpid,srcIP,dstIP,srcMAC,dstMAC):
    _send_msg(OFPFC_ADD, dpid, srcIP, srcMAC, dstIP, dstMAC, fport, bport)
