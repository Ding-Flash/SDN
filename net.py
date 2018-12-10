from topo import ModelNet
from mininet.log import setLogLevel

from time import sleep
# import threading


def get_flow(modelnet):
    run_time = 5
    while run_time:
        sleep(1)
        run_time -= 1
        modelnet.net.ping()


if __name__ == "__main__":
    setLogLevel('info')
    network = ModelNet()
    # t1 = threading.Thread(target=network.run_net)
    # t2 = threading.Thread(target=get_flow, args=(network,))
    # threads = [t1, t2]
    # for t in threads:
    #     t.start()
    network.run_net()
    get_flow(network)
