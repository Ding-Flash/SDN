from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.node import RemoteController, OVSSwitch
from mininet.link import TCLink

from mininet.cli import CLI

from config import con_confs, init_topo


class ModelNet(object):

    def __init__(self, con_num=1, sw_num=3, host_num=6):
        self.con_num = con_num
        self.sw_num = sw_num
        self.hosts_num = host_num
        self.con = []
        self.sw = []
        self.hosts = []
        self.net = Mininet(
            controller=None, switch=OVSSwitch, link=TCLink
        )

    def add_device(self):
        self.sw = [self.net.addSwitch("s%d" % (idx+1)) for idx in xrange(self.sw_num)]
        for con_conf in con_confs:
            con = RemoteController(**con_conf)
            self.net.addController(con)
            self.con.append(con)
        self.hosts = [self.net.addHost("h%s" % (idx+1)) for idx in xrange(self.hosts_num)]

    def build_net(self):
        for idx, sw in enumerate(self.sw):
            self.net.addLink(sw, self.hosts[idx*2])
            self.net.addLink(sw, self.hosts[idx*2 + 1])
        self.net.build()

        for con in self.con:
            con.start()

        for con, sw_idxs in init_topo.items():
            for sw_idx in sw_idxs:
                self.sw[sw_idx].start([self.con[con]])

    def run_net(self):
        self.add_device()
        self.build_net()
        CLI(self.net)


if __name__ == "__main__":
    setLogLevel('info')
    network = ModelNet()
    network.run_net()
