from threading import Thread
from scapy.all import sendp,Ether,IP

from flows import MacGenerator

class ScapyThread(Thread):

    # Host deve ser derivado do mininet
    def __init__(self,host=None,dst="00:00:00:00:00:02",src="00:00:00:00:00:01"):
        self.host = host
        self.dst = dst
        self.src = src

        self.generator = MacGenerator()

        self.active = True
        



    def run(self):
        while(self.active):
            pck = Ether(src=self.generator.increment(), dst=self.dst)/IP(src="10.1.1.10", dst="10.0.0.2"))
            sendp(pck)

    
    def turnoff(self):
        self.active = False
    


