# ryu-manager monitor.py --ofp-tcp-listen-port=6633
con_confs = [
    {
        "name": "c1",
        "ip": "127.0.0.1",
        "port": 6633
    },
    {
        "name": "c2",
        "ip": "127.0.0.1",
        "port": 6634
    }
]

base_topo = {
    'host_num': 4,
    'sw_num': 2,
    'con_num': 2,
    's2h': {
        0: [0, 1],
        1: [2, 3]
    },
    'c2s': {
        0: [0],
        1: [1]
    }
}
