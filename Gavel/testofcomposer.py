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

import os
import sys
import subprocess

def preexec_fn():
    # don't forward signals to child process
    # we need this when starting a Pox subprocess, so that SIGINTs from the CLI
    # aren't forwarded to Pox, causing it to terminate early
    os.setpgrp()

def append_path(path):
    path = os.path.expanduser(path)
    print path
    if "PYTHONPATH" not in os.environ:
        os.environ["PYTHONPATH"] = ""

    sys.path = os.environ["PYTHONPATH"].split(":") + sys.path

    if path is None or path == "":
        path = "."

    if path not in sys.path:
        sys.path.append(path)
    print sys.path


install_path = os.path.dirname(os.path.abspath(__file__))
install_path = os.path.normpath(os.path.join(install_path, ".."))
print install_path

pox = os.path.join("/home/gavel/pox", "pox.py")
cargs = ["log.level","--DEBUG","openflow.of_01","poxmanager","openflow.discovery"]

append_path(install_path)
env = os.environ.copy()
env["PYTHONPATH"] = ":".join(sys.path)
print env["PYTHONPATH"]
subprocess.Popen([pox] + cargs,env=env)
#subprocess.Popen([pox] + cargs,env=env,preexec_fn = preexec_fn)
#,stdout=open("/tmp/pox.log", "wb"),stderr=open("/tmp/pox.err", "wb")