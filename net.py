from mininet.cli import CLI

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.log import lg, info, output
from mininet.topolib import TreeNet
from topo import network
from time import sleep
from fetch import getall
from algorithm import *

class SingleSwitchTopo(Topo):
    "Single switch connected to n hosts."
    def build(self, n=2):
        switch = self.addSwitch('s1')
        # Python's range(N) generates 0..N-1
        for h in range(n):
            host = self.addHost('h%s' % (h + 1))
            self.addLink(host, switch)

'''
bandwidth = 1M, each log get nearly 2 million bytes, to specify==1867320
bandwidth = 2M, each log get nearly 4 million bytes, to specify==3867696
'''

def ping_increase(hosts_list, udpBw='1M', period=200, port=5001):
    for i in range(0,8,2):
        hosts = [hosts_list[i], hosts_list[i + 1]]
        ping_single(hosts, udpBw)

def ping_increase_morethan_2million():
    pass

def ping_decrease(udpBw='2M', period=60, port=5001):
    for i in range(0,8,2):
        hosts = [hosts_list[i], hosts_list[i + 1]]
        ping_single(hosts, udpBw)


def ping_balance(udpBw='6M', period=60, port=5001):
    pass


def ping_single(hosts=None, udpBw='10M', period=200, port=5001):
    if not hosts:
        return
    else:
        assert len(hosts) == 2
    client, server = hosts
    filename = '1.out'
    output('*** Iperf: testing bandwidth between %s and %s\n'  % ( client.name, server.name ))
    iperfArgs = 'iperf -u '
    bwArgs = '-b ' + udpBw + ' '
    print ("***start server***")
    server.cmd(iperfArgs + '-s -i 1' + ' > /home/dadan/' + filename + '&' )
    print ("***start client***")
    for i in range(3):
        print ("the " + str(i) + " times")
        client.cmd(iperfArgs + '-t '+ str(period) + ' -c ' + server.IP() + ' ' + bwArgs +' > /home/dadan/' + 'client' + filename + '&')
        sleep(3)

def ping_random(hosts, bw, period=60):
    base_port = 5001
    server_list = []
    host_list = [h for h in hosts]
    
    _len = len(host_list)
    for i in xrange(0, _len):
        client = host_list[i]
        server = client
        while( server == client ):
            server = random.choice(host_list)
        server_list.append(server)
        ping_single(hosts = [client, server], udpBw=bw, period=period, port=base_port)
        sleep(.05)
        base_port += 1
    
    sleep(period)
    print "test has done"

if __name__ == "__main__":
    hosts_name = ['h1','h2','h3','h4','h5','h6','h7','h8']
    net = network()
    # net.start()
    hosts_lists = [net.get(h) for h in hosts_name]
    ping_single([hosts_lists[0], hosts_lists[1]], '3M')
    ping_single([hosts_lists[2], hosts_lists[3]], '3M')
    ping_single([hosts_lists[4], hosts_lists[5]], '1M')
    ping_single([hosts_lists[6], hosts_lists[7]], '1M')
    # ping_increase(hosts_lists)   
    balance(net)
    printtopo()
    CLI(net)
