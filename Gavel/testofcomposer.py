"""
In this file, the test for ofcomposer takes place. 
The test scenario as follows:
0. run pox with loading modules correctly. 
pox pathtomodule/poxmanager.py openflow.of_01 openflow.discovery
1. run mininet with the topology. (diamond and linear, then later with more complicated topology)
2. run Gavel and let it build the topology.
3. check that Gavel detects the topology correctly.
4. start do ping test in mininet and see how Gavel responds to it.

Another test scenario
a. start mininet and gavel with the same topology file. 
b. start call routing and sfc and other functions on Gavel and check if OFcomposer responds accordingly.
"""




