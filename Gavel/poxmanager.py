#!/usr/bin/env python
"""
Pox-based OpenFlow manager
"""

"""
To Do:
0.Write the main scenario to test the code. 
1. fix lunch function
2. implement packet_In event Done
3.flowstats send and receive implementation.
"""

import pox.openflow.libopenflow_01 as of
from pox.core import core
from pox.lib.recoco import *
from pox.lib.revent import *
from pox.lib.addresses import IPAddr, EthAddr
from pox.lib.util import dpid_to_str
from pox.lib.util import str_to_dpid
from updateGavel import *
from route import *


log = core.getLogger()

class PoxManager(topologyname):
    "Pox-based OpenFlow manager"

    def __init__(self):
        self.datapaths = {}
        self.receiver = []
        self.flowstats = []
        self.dpid_cache = {}
        updateGavel.loaddb(topologyname)

        core.openflow.addListeners(self, priority=0)
        

        def startup():
            core.openflow_discovery.addListeners(self)

        core.call_when_ready(startup, ("openflow", "openflow_discovery"))# will detect link activity by send LLDP to detect topology

    def update_switch_cache(self): 
        #rewrite
        self.db.cursor.execute("SELECT * FROM switches;")
        result = self.db.cursor.fetchall()
        for sw in result:
            self.dpid_cache[sw[1]] = { 'sid' : sw[0],
                                       'dpid' : sw[1],
                                       'ip' : sw[2],
                                       'mac': sw[3],
                                       'name': sw[4] }

    def _handle_ConnectionDown(self, event):
        #when a control connection to the switch is lost
        dpid = "%0.16x" % event.dpid
        del self.datapaths[event.dpid]
        delswitchGavel(dpid)
        
    def _handle_ConnectionUp(self, event):
        #when a control connection to the switch is up
        dpid = "%0.16x" % event.dpid
        #self.update_switch_cache()
        self.datapaths[event.dpid] = event.connection
        addswitchGavel(dpid)

        

    def _handle_LinkEvent(self, event):
        #handel links events
        dpid1 = "%0.16x" % event.link.dpid1
        dpid2 = "%0.16x" % event.link.dpid2
        port1 = event.link.port1
        port2 = event.link.port2
        #sid1 = self.dpid_cache[dpid1]['sid']
        #sid2 = self.dpid_cache[dpid2]['sid']

        if event.removed:
            dellinkGavel(dpid2,port2,dpid1,port1)

            
        elif event.added:
            # does the forward link exist in Postgres?
            addlinkGavel(dpid2,port2,dpid1,port1)
    def _handle_BarrierIn(self, event):
        pass
    def _handle_PacketIn(self, event):
        packet = event.parsed
        if packet.type == ethernet.LLDP_TYPE:
            # Ignore LLDP packets
            return
        srcip = packet.find("ipv4").srcip
        dstip = packet.find("ipv4").dstip
        return route.getroute(installconnection(),str(srcip),str(dstip))
        """call routing app"""
        

    def _handle_FlowStatsReceived(self, event):
        pass

    def requestStats(self):
        "Send all switches a flow statistics request"
        self.flowstats = []
        for connection in core.openflow._connections.values():
            connection.send(of.ofp_stats_request(body=of.ofp_flow_stats_request()))

        

        return True

    def sendBarrier(self, dpid):
        """Send a barrier message
           dpid: datapath id of the switch to receive the barrier"""
        dpid = int(dpid)
        if dpid in self.datapaths:
            dp = self.datapaths[dpid]
            msg = of.ofp_barrier_request()
            dp.send(msg)
            self.perfcounter.start()
            self.log.debug("dpid {0} sent barrier".format(dpid))
        else:
            self.log.debug("dpid {0} not in datapath list".format(dpid))
        return True

    def registerReceiver(self, receiver):
        """Register a new message receiver
           receiver: a ravel.messaging.MessageReceiver object"""
        self.log.info("registering receiver")
        self.receiver.append(receiver)
        receiver.start()
        core.addListener(pox.core.GoingDownEvent, receiver.stop)

    def isRunning(self):
        "returns: true if the controller is running, false otherwise"
        return core.running

    def mk_msg(self, flow):
        """Create a Pox flowmod message from ravel.flow.OfMessage
           flow: a ravel.flow.OfMessage object"""
        msg = of.ofp_flow_mod()
        msg.command = int(flow.command)
        msg.priority = int(flow.priority)
        msg.match = of.ofp_match()
        if flow.match.dl_type is not None:
            msg.match.dl_type = int(flow.match.dl_type)
        if flow.match.nw_src is not None:
            msg.match.nw_src = IPAddr(flow.match.nw_src)
        if flow.match.nw_dst is not None:
            msg.match.nw_dst = IPAddr(flow.match.nw_dst)
        if flow.match.dl_src is not None:
            msg.match.dl_src = EthAddr(flow.match.dl_src)
        if flow.match.dl_dst is not None:
            msg.match.dl_dst = EthAddr(flow.match.dl_dst)
        for outport in flow.actions:
            msg.actions.append(of.ofp_action_output(port=int(outport)))
        return msg

    def send(self, dpid, msg):
        """Send a message to a switch
           dpid: datapath id of the switch
           msg: OpenFlow message"""
        self.log.debug("ravel: flow mod dpid={0}".format(dpid))
        if dpid in self.datapaths:
            dp = self.datapaths[dpid]
            dp.send(msg)
        else:
            self.log.debug("dpid {0} not in datapath list".format(dpid))

    def sendFlowmod(self, flow):
        """Send a flow modification message
           flow: the flow modification message to send"""
        dpid = int(flow.switch.dpid)
        self.send(dpid, self.mk_msg(flow))
    
    def stop(self):
        "Stop the manager (and stop receiving messages from the database)"
        for receiver in self.receiver:
            receiver.stop()
def launch():
    "Start the OpenFlow manager and message receivers"
    ctrl = PoxManager()
    #mq = MsgQueueReceiver(Config.QueueId, ctrl)
    #ctrl.registerReceiver(mq)
    #rpc = RpcReceiver(Config.RpcHost, Config.RpcPort, ctrl)
    #ctrl.registerReceiver(rpc)
    core.register("gavelcontroller", ctrl)
