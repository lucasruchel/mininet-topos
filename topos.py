from mininet.topo import Topo

class SpineLeaf(Topo):

    def build( self, spines=2,leaves=2):
        self.createTopo(spines,leaves)

    def createTopo(self,nroSpines,leaves):
        spines = [] 
        switchNum = 1
        hostNum = 1
        for n in range(nroSpines):
            spines.append(self.addSwitch("s%s" % (switchNum)))
            switchNum += 1


        for n in range(leaves):
            leaf = self.addSwitch("s%s" % (switchNum))
            switchNum += 1

            for spine in spines:
                self.addLink(leaf,spine)

            h = self.addHost("h%s" % (hostNum))
            self.addLink(h,leaf)

            hostNum += 1


