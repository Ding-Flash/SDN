# -*- coding: utf-8 -*-
from flask import Flask, request
import json


app = Flask(__name__)

# datapath集合 元素组成 datapath_id:port
datapath_c0 = set()
datapath_c1 = set()

# 流表监控集合
flow_table_c0 = {}
flow_table_c1 = {}

# 流表中miss流量、
flow_miss_c0 = {}
flow_miss_c1 = {}

# 端口流量监控集合
flow_port_c0 = {}
flow_port_c1 = {}


@app.route("/addall/<con>", methods=['POST'])
def addtable(con):
    if con == "c0":
        flow_port, datapath = flow_port_c0, datapath_c0
    else:
        flow_port, datapath = flow_port_c1, datapath_c1
    data = json.loads(request.data)
    try:
        target = flow_port[data['datapath']]
        for k, v in target.items():
            target[k].append(data[k])
    except KeyError:
        flow_port[data['datapath']] = {
            'rx_packets': [], 'rx_bytes': [], 'rx_errors': [],
            'tx_packets': [], 'tx_bytes': [], 'tx_error': []
        }
        datapath.add(data['datapath'])
    print "%s<->%s port-info update" % (con, data['datapath'])
    return request.data


@app.route('/addflow/<con>', methods=['POST'])
def addflow(con):
    if con == "c0":
        flow_table, datapath = flow_table_c0, datapath_c0
    else:
        flow_table, datapath = flow_table_c1, datapath_c1
    data = json.loads(request.data)
    try:
        target = flow_table[data['datapath']]
        for k, v in target.items():
            target[k].append(data[k])
    except KeyError:
        flow_table[data['datapath']] = {
            'rx_packets': [], 'rx_bytes': [],
            'tx_packets': [], 'tx_bytes': []
        }
        datapath.add(data['datapath'])
    print "%s<->%s flow-info update" % (con, data['datapath'])
    return request.data


@app.route("/addmiss/<con>", methods=['POST'])
def addmiss(con):
    if con == "c0":
        flow_miss= flow_miss_c0
    else:
        flow_miss= flow_miss_c1
    data = json.loads(request.data)
    try:
        target = flow_miss[data['datapath']]
        for k, v in target.items():
            target[k].append(data[k])
    except KeyError:
        flow_miss[data['datapath']] = {
            'packets': [], 'bytes': [],
        }
    print "%s<->%s flow-miss-info update" % (con, data['datapath'])
    return request.data


@app.route('/getall/<con>', methods=['GET'])
def getall(con):
    flow_table = flow_table_c0 if con == "c0" else flow_table_c1
    print "get %s port-info" % con
    return json.dumps(flow_table)


@app.route('/getflow/<con>', methods=['GET'])
def getflow(con):
    flow_table = flow_table_c0 if con == 'c0' else flow_table_c1
    print "get %s flow-info" % con
    return json.dumps(flow_table)


@app.route('/getmiss/<con>', methods=['GET'])
def getmiss(con):
    flow_miss = flow_miss_c0 if con == 'c0' else flow_miss_c1
    print "get %s miss-info" % con
    return json.dumps(flow_miss)


@app.route('/getdatapath/<con>', methods=['GET'])
def getdatapath(con):
    datapath = datapath_c0 if con == 'c0' else datapath_c1
    print "get %s datapath-info" % con
    return json.dumps({'data': list(datapath)})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
