#!/usr/bin/env python
""" 

Usage: idle_nodes_plus.py [options]

This command shows the idle nodes with number of CPU and memory size

Options:
  -h, --help     show this help message and exit
  -s, --summary  Show summary only

"""
import sys
import subprocess
import datetime
import re
import os,glob,time
import random,math
import numpy as np
import logging
import optparse 

# logging.basicConfig(level=logging.DEBUG, 
#                     format='%(asctime)s - %(levelname)s: %(message)s')
logging.basicConfig(level=logging.DEBUG, 
                    format='%(levelname)s: %(message)s')
# logging.debug('This is a log message.')


# return number of CPU and total memory
def get_node_info(node):
    comm=["qhost", "-h", node]
    res = subprocess.check_output(comm).decode("utf-8").rstrip()
    lines=res.split('\n')
    try:
        mobj=re.search("\s+NCPU",lines[0])
        ncpu=lines[3][mobj.start():mobj.end()]
        mobj=re.search("\w+$",ncpu)
        ncpu=mobj.group()
        ncpu=int(ncpu)
    except:
        ncpu=None

    try:
        mobj=re.search("\s+MEMTOT",lines[0])
        memory=lines[3][mobj.start():mobj.end()]
        mobj=re.search("([0-9.]+)G$",memory)
        memory=mobj.group(1)
        memory=float(memory)
    except:
        memory=None

    return (ncpu,memory)


## main funciton
if __name__=='__main__':
    desc='This command shows the idle nodes with number of CPU and memory size'
    parser = optparse.OptionParser(description=desc)
    parser.add_option("-s", "--summary",
                      action="store_true",
                      default=False,
                      help="Show summary only")

    (options, args) = parser.parse_args()

    comm=["idle-nodes",]
    res = subprocess.check_output(comm).decode("utf-8").rstrip()
    nodes=res.split('\n')
    
    nodes=[node for node in nodes if not re.search('head',node)]
    data=np.zeros((len(nodes),2))

    for idx,node in enumerate(nodes):
        ncpu,memory=get_node_info(node)
        data[idx,0]=ncpu
        data[idx,1]=memory
        if not options.summary:
            print("{}: ncpu={}, memory={}G".format(node,ncpu,memory))

    print('='*30)
    print('There are {} idle nodes.'.format(len(nodes)))
    # logging.debug(data)
    data=data[data[:,0].argsort()]
    udata,count=np.unique(data,axis=0,return_counts = True)
    # logging.debug(udata)
    # logging.debug(count)
    for a,b in zip(udata,count):
        print('There are {} nodes with ncpu={}, memory={}G'.format(
            b,int(a[0]),a[1]))
    print('='*30)

