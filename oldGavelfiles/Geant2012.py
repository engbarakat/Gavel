#!/usr/bin/python
"""
Custom topology for Mininet, generated by GraphML-Topo-to-Mininet-Network-Generator.
"""
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.node import Node
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.util import dumpNodeConnections


class NodeID(object):
    "Topo node identifier."

    def __init__(self, dpid = None):
        "Init."

        "@param dpid dpid"
        
        # DPID-compatible hashable identifier: opaque 64-bit unsigned int
        self.dpid = dpid

    def __str__(self):
        "String conversion."

        "@return str dpid as string"
        
        return str(self.dpid)

    def name_str(self):
        "Name conversion."

        "@return name name as string"
        
        return str(self.dpid)

    def ip_str(self):
        "Name conversion."

        "@return ip ip as string"
        
        hi = (self.dpid & 0xff0000) >> 16
        mid = (self.dpid & 0xff00) >> 8
        lo = self.dpid & 0xff
        return "10.%i.%i.%i" % (hi, mid, lo)

class ZooNodeID(NodeID):
        "Fat Tree-specific node."

        def __init__(self, pod = 0, sw = 0, host = 0, dpid = None, name = None):
            "Create FatTreeNodeID object from custom params."

            "Either (pod, sw, host) or dpid must be passed in."

            "@param pod pod ID"
            "@param sw switch ID"
            "@param host host ID"
            "@param dpid optional dpid"
            "@param name optional name"
            
            if dpid:
                self.pod = (dpid & 0xff0000) >> 16
                self.sw = (dpid & 0xff00) >> 8
                self.host = (dpid & 0xff)
                self.dpid = dpid
            elif name:
                pod, sw, host = [int(s) for s in name.split('_')]
                self.pod = pod
                self.sw = sw
                self.host = host
                self.dpid = (pod << 16) + (sw << 8) + host
            else:
                self.pod = pod
                self.sw = sw
                self.host = host
                self.dpid = (pod << 16) + (sw << 8) + host

        def __str__(self):
            return "(%i, %i, %i)" % (self.pod, self.sw, self.host)

        def name_str(self):
            "Return name string"
            return "%i_%i_%i" % (self.pod, self.sw, self.host)

        def mac_str(self):
            "Return MAC string"
            return "00:00:00:%02x:%02x:%02x" % (self.pod, self.sw, self.host)

        def ip_str(self):
            "Return IP string"
            return "10.%i.%i.%i" % (self.pod, self.sw, self.host)


def def_nopts(zoonodeid, layer, name = None):
        "Return default dict for a FatTree topo."

        "@param layer layer of node"
        "@param name name of node"
        "@return d dict with layer key/val pair, plus anything else (later)"
        
        d = {'layer': layer}
        if name:
            id = zoonodeid(name = name)
            # For hosts only, set the IP
            if layer == 3:
              d.update({'ip': id.ip_str()})
              d.update({'mac': id.mac_str()})
            d.update({'dpid': "%016x" % id.dpid})
        return d

class GeneratedTopo( Topo ):
    "Internet Topology Zoo Specimen."
    def __init__( self, **opts ):
        "Create a topology."
        # Initialize Topology
        self.switchList={}
        self.hostList={}
        Topo.__init__( self, **opts )

        # add nodes, switches first...
        id_gen_0 = ZooNodeID 
        edge_id = id_gen_0(0,0, 1).name_str()
        edge_opts = def_nopts(id_gen_0,0, edge_id)
        NL = self.addSwitch( edge_id,**edge_opts )
        self.switchList[edge_id] = edge_opts 


        id_gen_1 = ZooNodeID 
        edge_id = id_gen_1(0,1, 1).name_str()
        edge_opts = def_nopts(id_gen_1,0, edge_id)
        BE = self.addSwitch( edge_id,**edge_opts )
        self.switchList[edge_id] = edge_opts 


        id_gen_2 = ZooNodeID 
        edge_id = id_gen_2(0,2, 1).name_str()
        edge_opts = def_nopts(id_gen_2,0, edge_id)
        DK = self.addSwitch( edge_id,**edge_opts )
        self.switchList[edge_id] = edge_opts 


        id_gen_3 = ZooNodeID 
        edge_id = id_gen_3(0,3, 1).name_str()
        edge_opts = def_nopts(id_gen_3,0, edge_id)
        PL = self.addSwitch( edge_id,**edge_opts )
        self.switchList[edge_id] = edge_opts 


        id_gen_4 = ZooNodeID 
        edge_id = id_gen_4(0,4, 1).name_str()
        edge_opts = def_nopts(id_gen_4,0, edge_id)
        DE = self.addSwitch( edge_id,**edge_opts )
        self.switchList[edge_id] = edge_opts 


        id_gen_5 = ZooNodeID 
        edge_id = id_gen_5(0,5, 1).name_str()
        edge_opts = def_nopts(id_gen_5,0, edge_id)
        CZ = self.addSwitch( edge_id,**edge_opts )
        self.switchList[edge_id] = edge_opts 


        id_gen_6 = ZooNodeID 
        edge_id = id_gen_6(0,6, 1).name_str()
        edge_opts = def_nopts(id_gen_6,0, edge_id)
        LU = self.addSwitch( edge_id,**edge_opts )
        self.switchList[edge_id] = edge_opts 


        id_gen_7 = ZooNodeID 
        edge_id = id_gen_7(0,7, 1).name_str()
        edge_opts = def_nopts(id_gen_7,0, edge_id)
        FR = self.addSwitch( edge_id,**edge_opts )
        self.switchList[edge_id] = edge_opts 


        id_gen_8 = ZooNodeID 
        edge_id = id_gen_8(0,8, 1).name_str()
        edge_opts = def_nopts(id_gen_8,0, edge_id)
        CH = self.addSwitch( edge_id,**edge_opts )
        self.switchList[edge_id] = edge_opts 


        id_gen_9 = ZooNodeID 
        edge_id = id_gen_9(0,9, 1).name_str()
        edge_opts = def_nopts(id_gen_9,0, edge_id)
        IT = self.addSwitch( edge_id,**edge_opts )
        self.switchList[edge_id] = edge_opts 


        id_gen_10 = ZooNodeID 
        edge_id = id_gen_10(0,10, 1).name_str()
        edge_opts = def_nopts(id_gen_10,0, edge_id)
        UA = self.addSwitch( edge_id,**edge_opts )
        self.switchList[edge_id] = edge_opts 


        id_gen_11 = ZooNodeID 
        edge_id = id_gen_11(0,11, 1).name_str()
        edge_opts = def_nopts(id_gen_11,0, edge_id)
        MD = self.addSwitch( edge_id,**edge_opts )
        self.switchList[edge_id] = edge_opts 


        id_gen_12 = ZooNodeID 
        edge_id = id_gen_12(0,12, 1).name_str()
        edge_opts = def_nopts(id_gen_12,0, edge_id)
        BG = self.addSwitch( edge_id,**edge_opts )
        self.switchList[edge_id] = edge_opts 


        id_gen_13 = ZooNodeID 
        edge_id = id_gen_13(0,13, 1).name_str()
        edge_opts = def_nopts(id_gen_13,0, edge_id)
        RO = self.addSwitch( edge_id,**edge_opts )
        self.switchList[edge_id] = edge_opts 


        id_gen_14 = ZooNodeID 
        edge_id = id_gen_14(0,14, 1).name_str()
        edge_opts = def_nopts(id_gen_14,0, edge_id)
        TR = self.addSwitch( edge_id,**edge_opts )
        self.switchList[edge_id] = edge_opts 


        id_gen_15 = ZooNodeID 
        edge_id = id_gen_15(0,15, 1).name_str()
        edge_opts = def_nopts(id_gen_15,0, edge_id)
        GR = self.addSwitch( edge_id,**edge_opts )
        self.switchList[edge_id] = edge_opts 


        id_gen_16 = ZooNodeID 
        edge_id = id_gen_16(0,16, 1).name_str()
        edge_opts = def_nopts(id_gen_16,0, edge_id)
        CY = self.addSwitch( edge_id,**edge_opts )
        self.switchList[edge_id] = edge_opts 


        id_gen_17 = ZooNodeID 
        edge_id = id_gen_17(0,17, 1).name_str()
        edge_opts = def_nopts(id_gen_17,0, edge_id)
        IL = self.addSwitch( edge_id,**edge_opts )
        self.switchList[edge_id] = edge_opts 


        id_gen_18 = ZooNodeID 
        edge_id = id_gen_18(0,18, 1).name_str()
        edge_opts = def_nopts(id_gen_18,0, edge_id)
        MT = self.addSwitch( edge_id,**edge_opts )
        self.switchList[edge_id] = edge_opts 


        id_gen_19 = ZooNodeID 
        edge_id = id_gen_19(0,19, 1).name_str()
        edge_opts = def_nopts(id_gen_19,0, edge_id)
        BY = self.addSwitch( edge_id,**edge_opts )
        self.switchList[edge_id] = edge_opts 


        id_gen_20 = ZooNodeID 
        edge_id = id_gen_20(0,20, 1).name_str()
        edge_opts = def_nopts(id_gen_20,0, edge_id)
        MK = self.addSwitch( edge_id,**edge_opts )
        self.switchList[edge_id] = edge_opts 


        id_gen_21 = ZooNodeID 
        edge_id = id_gen_21(0,21, 1).name_str()
        edge_opts = def_nopts(id_gen_21,0, edge_id)
        ME = self.addSwitch( edge_id,**edge_opts )
        self.switchList[edge_id] = edge_opts 


        id_gen_22 = ZooNodeID 
        edge_id = id_gen_22(0,22, 1).name_str()
        edge_opts = def_nopts(id_gen_22,0, edge_id)
        HU = self.addSwitch( edge_id,**edge_opts )
        self.switchList[edge_id] = edge_opts 


        id_gen_23 = ZooNodeID 
        edge_id = id_gen_23(0,23, 1).name_str()
        edge_opts = def_nopts(id_gen_23,0, edge_id)
        SK = self.addSwitch( edge_id,**edge_opts )
        self.switchList[edge_id] = edge_opts 


        id_gen_24 = ZooNodeID 
        edge_id = id_gen_24(0,24, 1).name_str()
        edge_opts = def_nopts(id_gen_24,0, edge_id)
        PT = self.addSwitch( edge_id,**edge_opts )
        self.switchList[edge_id] = edge_opts 


        id_gen_25 = ZooNodeID 
        edge_id = id_gen_25(0,25, 1).name_str()
        edge_opts = def_nopts(id_gen_25,0, edge_id)
        ES = self.addSwitch( edge_id,**edge_opts )
        self.switchList[edge_id] = edge_opts 


        id_gen_26 = ZooNodeID 
        edge_id = id_gen_26(0,26, 1).name_str()
        edge_opts = def_nopts(id_gen_26,0, edge_id)
        RS = self.addSwitch( edge_id,**edge_opts )
        self.switchList[edge_id] = edge_opts 


        id_gen_27 = ZooNodeID 
        edge_id = id_gen_27(0,27, 1).name_str()
        edge_opts = def_nopts(id_gen_27,0, edge_id)
        HR = self.addSwitch( edge_id,**edge_opts )
        self.switchList[edge_id] = edge_opts 


        id_gen_28 = ZooNodeID 
        edge_id = id_gen_28(0,28, 1).name_str()
        edge_opts = def_nopts(id_gen_28,0, edge_id)
        SL = self.addSwitch( edge_id,**edge_opts )
        self.switchList[edge_id] = edge_opts 


        id_gen_29 = ZooNodeID 
        edge_id = id_gen_29(0,29, 1).name_str()
        edge_opts = def_nopts(id_gen_29,0, edge_id)
        AT = self.addSwitch( edge_id,**edge_opts )
        self.switchList[edge_id] = edge_opts 


        id_gen_30 = ZooNodeID 
        edge_id = id_gen_30(0,30, 1).name_str()
        edge_opts = def_nopts(id_gen_30,0, edge_id)
        LT = self.addSwitch( edge_id,**edge_opts )
        self.switchList[edge_id] = edge_opts 


        id_gen_31 = ZooNodeID 
        edge_id = id_gen_31(0,31, 1).name_str()
        edge_opts = def_nopts(id_gen_31,0, edge_id)
        RU = self.addSwitch( edge_id,**edge_opts )
        self.switchList[edge_id] = edge_opts 


        id_gen_32 = ZooNodeID 
        edge_id = id_gen_32(0,32, 1).name_str()
        edge_opts = def_nopts(id_gen_32,0, edge_id)
        IS = self.addSwitch( edge_id,**edge_opts )
        self.switchList[edge_id] = edge_opts 


        id_gen_33 = ZooNodeID 
        edge_id = id_gen_33(0,33, 1).name_str()
        edge_opts = def_nopts(id_gen_33,0, edge_id)
        IE = self.addSwitch( edge_id,**edge_opts )
        self.switchList[edge_id] = edge_opts 


        id_gen_34 = ZooNodeID 
        edge_id = id_gen_34(0,34, 1).name_str()
        edge_opts = def_nopts(id_gen_34,0, edge_id)
        UK = self.addSwitch( edge_id,**edge_opts )
        self.switchList[edge_id] = edge_opts 


        id_gen_35 = ZooNodeID 
        edge_id = id_gen_35(0,35, 1).name_str()
        edge_opts = def_nopts(id_gen_35,0, edge_id)
        NO = self.addSwitch( edge_id,**edge_opts )
        self.switchList[edge_id] = edge_opts 


        id_gen_36 = ZooNodeID 
        edge_id = id_gen_36(0,36, 1).name_str()
        edge_opts = def_nopts(id_gen_36,0, edge_id)
        SE = self.addSwitch( edge_id,**edge_opts )
        self.switchList[edge_id] = edge_opts 


        id_gen_37 = ZooNodeID 
        edge_id = id_gen_37(0,37, 1).name_str()
        edge_opts = def_nopts(id_gen_37,0, edge_id)
        FI = self.addSwitch( edge_id,**edge_opts )
        self.switchList[edge_id] = edge_opts 


        id_gen_38 = ZooNodeID 
        edge_id = id_gen_38(0,38, 1).name_str()
        edge_opts = def_nopts(id_gen_38,0, edge_id)
        EE = self.addSwitch( edge_id,**edge_opts )
        self.switchList[edge_id] = edge_opts 


        id_gen_39 = ZooNodeID 
        edge_id = id_gen_39(0,39, 1).name_str()
        edge_opts = def_nopts(id_gen_39,0, edge_id)
        LV = self.addSwitch( edge_id,**edge_opts )
        self.switchList[edge_id] = edge_opts 



        # ... and now hosts
        host_id = id_gen_0(3,0,1).name_str()
        host_opts = def_nopts(id_gen_0,3, host_id)
        NL_host = self.addHost( host_id,**host_opts )
        self.hostList[host_id] = host_opts 


        host_id = id_gen_1(3,1,2).name_str()
        host_opts = def_nopts(id_gen_1,3, host_id)
        BE_host = self.addHost( host_id,**host_opts )
        self.hostList[host_id] = host_opts 


        host_id = id_gen_2(3,2,3).name_str()
        host_opts = def_nopts(id_gen_2,3, host_id)
        DK_host = self.addHost( host_id,**host_opts )
        self.hostList[host_id] = host_opts 


        host_id = id_gen_3(3,3,4).name_str()
        host_opts = def_nopts(id_gen_3,3, host_id)
        PL_host = self.addHost( host_id,**host_opts )
        self.hostList[host_id] = host_opts 


        host_id = id_gen_4(3,4,5).name_str()
        host_opts = def_nopts(id_gen_4,3, host_id)
        DE_host = self.addHost( host_id,**host_opts )
        self.hostList[host_id] = host_opts 


        host_id = id_gen_5(3,5,6).name_str()
        host_opts = def_nopts(id_gen_5,3, host_id)
        CZ_host = self.addHost( host_id,**host_opts )
        self.hostList[host_id] = host_opts 


        host_id = id_gen_6(3,6,7).name_str()
        host_opts = def_nopts(id_gen_6,3, host_id)
        LU_host = self.addHost( host_id,**host_opts )
        self.hostList[host_id] = host_opts 


        host_id = id_gen_7(3,7,8).name_str()
        host_opts = def_nopts(id_gen_7,3, host_id)
        FR_host = self.addHost( host_id,**host_opts )
        self.hostList[host_id] = host_opts 


        host_id = id_gen_8(3,8,9).name_str()
        host_opts = def_nopts(id_gen_8,3, host_id)
        CH_host = self.addHost( host_id,**host_opts )
        self.hostList[host_id] = host_opts 


        host_id = id_gen_9(3,9,10).name_str()
        host_opts = def_nopts(id_gen_9,3, host_id)
        IT_host = self.addHost( host_id,**host_opts )
        self.hostList[host_id] = host_opts 


        host_id = id_gen_10(3,10,11).name_str()
        host_opts = def_nopts(id_gen_10,3, host_id)
        UA_host = self.addHost( host_id,**host_opts )
        self.hostList[host_id] = host_opts 


        host_id = id_gen_11(3,11,12).name_str()
        host_opts = def_nopts(id_gen_11,3, host_id)
        MD_host = self.addHost( host_id,**host_opts )
        self.hostList[host_id] = host_opts 


        host_id = id_gen_12(3,12,13).name_str()
        host_opts = def_nopts(id_gen_12,3, host_id)
        BG_host = self.addHost( host_id,**host_opts )
        self.hostList[host_id] = host_opts 


        host_id = id_gen_13(3,13,14).name_str()
        host_opts = def_nopts(id_gen_13,3, host_id)
        RO_host = self.addHost( host_id,**host_opts )
        self.hostList[host_id] = host_opts 


        host_id = id_gen_14(3,14,15).name_str()
        host_opts = def_nopts(id_gen_14,3, host_id)
        TR_host = self.addHost( host_id,**host_opts )
        self.hostList[host_id] = host_opts 


        host_id = id_gen_15(3,15,16).name_str()
        host_opts = def_nopts(id_gen_15,3, host_id)
        GR_host = self.addHost( host_id,**host_opts )
        self.hostList[host_id] = host_opts 


        host_id = id_gen_16(3,16,17).name_str()
        host_opts = def_nopts(id_gen_16,3, host_id)
        CY_host = self.addHost( host_id,**host_opts )
        self.hostList[host_id] = host_opts 


        host_id = id_gen_17(3,17,18).name_str()
        host_opts = def_nopts(id_gen_17,3, host_id)
        IL_host = self.addHost( host_id,**host_opts )
        self.hostList[host_id] = host_opts 


        host_id = id_gen_18(3,18,19).name_str()
        host_opts = def_nopts(id_gen_18,3, host_id)
        MT_host = self.addHost( host_id,**host_opts )
        self.hostList[host_id] = host_opts 


        host_id = id_gen_19(3,19,20).name_str()
        host_opts = def_nopts(id_gen_19,3, host_id)
        BY_host = self.addHost( host_id,**host_opts )
        self.hostList[host_id] = host_opts 


        host_id = id_gen_20(3,20,21).name_str()
        host_opts = def_nopts(id_gen_20,3, host_id)
        MK_host = self.addHost( host_id,**host_opts )
        self.hostList[host_id] = host_opts 


        host_id = id_gen_21(3,21,22).name_str()
        host_opts = def_nopts(id_gen_21,3, host_id)
        ME_host = self.addHost( host_id,**host_opts )
        self.hostList[host_id] = host_opts 


        host_id = id_gen_22(3,22,23).name_str()
        host_opts = def_nopts(id_gen_22,3, host_id)
        HU_host = self.addHost( host_id,**host_opts )
        self.hostList[host_id] = host_opts 


        host_id = id_gen_23(3,23,24).name_str()
        host_opts = def_nopts(id_gen_23,3, host_id)
        SK_host = self.addHost( host_id,**host_opts )
        self.hostList[host_id] = host_opts 


        host_id = id_gen_24(3,24,25).name_str()
        host_opts = def_nopts(id_gen_24,3, host_id)
        PT_host = self.addHost( host_id,**host_opts )
        self.hostList[host_id] = host_opts 


        host_id = id_gen_25(3,25,26).name_str()
        host_opts = def_nopts(id_gen_25,3, host_id)
        ES_host = self.addHost( host_id,**host_opts )
        self.hostList[host_id] = host_opts 


        host_id = id_gen_26(3,26,27).name_str()
        host_opts = def_nopts(id_gen_26,3, host_id)
        RS_host = self.addHost( host_id,**host_opts )
        self.hostList[host_id] = host_opts 


        host_id = id_gen_27(3,27,28).name_str()
        host_opts = def_nopts(id_gen_27,3, host_id)
        HR_host = self.addHost( host_id,**host_opts )
        self.hostList[host_id] = host_opts 


        host_id = id_gen_28(3,28,29).name_str()
        host_opts = def_nopts(id_gen_28,3, host_id)
        SL_host = self.addHost( host_id,**host_opts )
        self.hostList[host_id] = host_opts 


        host_id = id_gen_29(3,29,30).name_str()
        host_opts = def_nopts(id_gen_29,3, host_id)
        AT_host = self.addHost( host_id,**host_opts )
        self.hostList[host_id] = host_opts 


        host_id = id_gen_30(3,30,31).name_str()
        host_opts = def_nopts(id_gen_30,3, host_id)
        LT_host = self.addHost( host_id,**host_opts )
        self.hostList[host_id] = host_opts 


        host_id = id_gen_31(3,31,32).name_str()
        host_opts = def_nopts(id_gen_31,3, host_id)
        RU_host = self.addHost( host_id,**host_opts )
        self.hostList[host_id] = host_opts 


        host_id = id_gen_32(3,32,33).name_str()
        host_opts = def_nopts(id_gen_32,3, host_id)
        IS_host = self.addHost( host_id,**host_opts )
        self.hostList[host_id] = host_opts 


        host_id = id_gen_33(3,33,34).name_str()
        host_opts = def_nopts(id_gen_33,3, host_id)
        IE_host = self.addHost( host_id,**host_opts )
        self.hostList[host_id] = host_opts 


        host_id = id_gen_34(3,34,35).name_str()
        host_opts = def_nopts(id_gen_34,3, host_id)
        UK_host = self.addHost( host_id,**host_opts )
        self.hostList[host_id] = host_opts 


        host_id = id_gen_35(3,35,36).name_str()
        host_opts = def_nopts(id_gen_35,3, host_id)
        NO_host = self.addHost( host_id,**host_opts )
        self.hostList[host_id] = host_opts 


        host_id = id_gen_36(3,36,37).name_str()
        host_opts = def_nopts(id_gen_36,3, host_id)
        SE_host = self.addHost( host_id,**host_opts )
        self.hostList[host_id] = host_opts 


        host_id = id_gen_37(3,37,38).name_str()
        host_opts = def_nopts(id_gen_37,3, host_id)
        FI_host = self.addHost( host_id,**host_opts )
        self.hostList[host_id] = host_opts 


        host_id = id_gen_38(3,38,39).name_str()
        host_opts = def_nopts(id_gen_38,3, host_id)
        EE_host = self.addHost( host_id,**host_opts )
        self.hostList[host_id] = host_opts 


        host_id = id_gen_39(3,39,40).name_str()
        host_opts = def_nopts(id_gen_39,3, host_id)
        LV_host = self.addHost( host_id,**host_opts )
        self.hostList[host_id] = host_opts 



        # add edges between switch and corresponding host
        self.addLink( NL , NL_host )
        self.addLink( BE , BE_host )
        self.addLink( DK , DK_host )
        self.addLink( PL , PL_host )
        self.addLink( DE , DE_host )
        self.addLink( CZ , CZ_host )
        self.addLink( LU , LU_host )
        self.addLink( FR , FR_host )
        self.addLink( CH , CH_host )
        self.addLink( IT , IT_host )
        self.addLink( UA , UA_host )
        self.addLink( MD , MD_host )
        self.addLink( BG , BG_host )
        self.addLink( RO , RO_host )
        self.addLink( TR , TR_host )
        self.addLink( GR , GR_host )
        self.addLink( CY , CY_host )
        self.addLink( IL , IL_host )
        self.addLink( MT , MT_host )
        self.addLink( BY , BY_host )
        self.addLink( MK , MK_host )
        self.addLink( ME , ME_host )
        self.addLink( HU , HU_host )
        self.addLink( SK , SK_host )
        self.addLink( PT , PT_host )
        self.addLink( ES , ES_host )
        self.addLink( RS , RS_host )
        self.addLink( HR , HR_host )
        self.addLink( SL , SL_host )
        self.addLink( AT , AT_host )
        self.addLink( LT , LT_host )
        self.addLink( RU , RU_host )
        self.addLink( IS , IS_host )
        self.addLink( IE , IE_host )
        self.addLink( UK , UK_host )
        self.addLink( NO , NO_host )
        self.addLink( SE , SE_host )
        self.addLink( FI , FI_host )
        self.addLink( EE , EE_host )
        self.addLink( LV , LV_host )

        # add edges between switches
        self.addLink( NL , BE)
        self.addLink( NL , DK)
        self.addLink( NL , DE)
        self.addLink( NL , UK)
        self.addLink( NL , LT)
        self.addLink( BE , IE)
        self.addLink( DK , IS)
        self.addLink( DK , NO)
        self.addLink( DK , DE)
        self.addLink( DK , EE)
        self.addLink( DK , SE)
        self.addLink( DK , RU)
        self.addLink( PL , UA)
        self.addLink( PL , BY)
        self.addLink( PL , DE)
        self.addLink( PL , CZ)
        self.addLink( PL , LT)
        self.addLink( DE , CZ)
        self.addLink( DE , LU)
        self.addLink( DE , CH)
        self.addLink( DE , CY)
        self.addLink( DE , IL)
        self.addLink( DE , AT)
        self.addLink( DE , RU)
        self.addLink( CZ , SK)
        self.addLink( LU , FR)
        self.addLink( FR , CH)
        self.addLink( FR , ES)
        self.addLink( FR , UK)
        self.addLink( CH , IT)
        self.addLink( CH , ES)
        self.addLink( IT , ES)
        self.addLink( IT , MT)
        self.addLink( IT , AT)
        self.addLink( IT , GR)
        self.addLink( MD , RO)
        self.addLink( BG , TR)
        self.addLink( BG , MK)
        self.addLink( BG , RO)
        self.addLink( BG , HU)
        self.addLink( BG , GR)
        self.addLink( RO , HU)
        self.addLink( RO , TR)
        self.addLink( GR , AT)
        self.addLink( CY , UK)
        self.addLink( IL , LT)
        self.addLink( ME , HR)
        self.addLink( HU , RS)
        self.addLink( HU , HR)
        self.addLink( HU , SK)
        self.addLink( SK , AT)
        self.addLink( PT , ES)
        self.addLink( PT , UK)
        self.addLink( HR , SL)
        self.addLink( SL , AT)
        self.addLink( LT , LV)
        self.addLink( IS , UK)
        self.addLink( IE , UK)
        self.addLink( NO , SE)
        self.addLink( SE , FI)
        self.addLink( EE , LV)

topos = { 'generated': ( lambda: GeneratedTopo() ) }
# HERE THE CODE DEFINITION OF THE TOPOLOGY ENDS
# the following code produces an executable script working with a remote controller
# and providing ssh access to the the mininet hosts from within the ubuntu vm
