# -*- coding: utf-8 -*-
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.link import TCLink


from config import con_confs, base_topo

from requests import get


class ModelNet(object):

    def __init__(self):
        """
        根据 base_topo 中的num信息，构建拓扑图
        """
        self.host_num = base_topo['host_num']
        self.sw_num = base_topo['sw_num']
        self.con_num = base_topo['con_num']
        self.hosts, self.sw, self.con = [], [], []
        self.net = Mininet(
            controller=None, switch=OVSSwitch, link=TCLink
        )

    def add_device(self):
        """
        根据配置信息向net中添加设备
        """
        self.hosts = [self.net.addHost("h%s" % idx) for idx in xrange(self.host_num)]
        self.sw = [self.net.addSwitch("s%d" % idx) for idx in xrange(self.sw_num)]
        for con_conf in con_confs:
            con = RemoteController(**con_conf)
            self.net.addController(con)
            self.con.append(con)

    def build_net(self):
        """
        设备之间连接创建组网图
        """
        for sw_idx, hosts in base_topo['s2h'].items():
            for idx in hosts:
                self.net.addLink(self.sw[sw_idx], self.hosts[idx])
        self.net.build()
        for con in self.con:
            con.start()
        for con, sws in base_topo['c2s'].items():
            for idx in sws:
                self.sw[idx].start([self.con[con]])

    def ping_test(self):
        self.net.ping()

    def run_net(self):
        """
        启动网络
        """
        self.add_device()
        self.build_net()
        self.net.start()
