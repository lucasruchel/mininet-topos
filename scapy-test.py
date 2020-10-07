#!/usr/bin/python3
# encoding: utf-8

from scapy.all import sendp,Ether, IP
from flows import MacGenerator
import sys, time



generator = MacGenerator()
executions = 1

if len(sys.argv) == 2:
    executions = int(sys.argv[1])



for i in range(executions):
    sendp(Ether(src=generator.increment(), dst="00:00:00:00:00:02")/IP(src="10.1.1.10", dst="10.0.0.2"))
    time.sleep(0.001)
