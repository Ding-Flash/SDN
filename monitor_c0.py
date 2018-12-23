# -*- coding: utf-8 -*-
# from operator import attrgetter

from ryu.app import simple_switch_13
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib import hub

from collections import defaultdict
import requests
import json


port_url = "http://127.0.0.1:5000/addall/c0"
flow_url = "http://127.0.0.1:5000/addflow/c0"
miss_url = "http://127.0.0.1:5000/addmiss/c0"
sleep_time = 5


class SimpleMonitor(simple_switch_13.SimpleSwitch13):

    def __init__(self, *args, **kwargs):
        super(SimpleMonitor, self).__init__(*args, **kwargs)
        self.datapaths = {}
        self.monitor_thread = hub.spawn(self._monitor)

    @set_ev_cls(ofp_event.EventOFPStateChange,
                [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            if not datapath.id in self.datapaths:
                self.logger.debug('register datapath: %016x', datapath.id)
                self.datapaths[datapath.id] = datapath
        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                self.logger.debug('unregister datapath: %016x', datapath.id)
                del self.datapaths[datapath.id]

    def _monitor(self):
        while True:
            for dp in self.datapaths.values():
                self._request_stats(dp)
            hub.sleep(sleep_time)

    def _request_stats(self, datapath):
        self.logger.debug('send stats request: %016x', datapath.id)
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        req = parser.OFPFlowStatsRequest(datapath)
        datapath.send_msg(req)

        req = parser.OFPPortStatsRequest(datapath, 0, ofproto.OFPP_ANY)
        datapath.send_msg(req)

    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def _flow_stats_reply_handler(self, ev):
        """
        该函数列出的是单个datapath连接的交换机的流表信息
        stat.match['in_port'] in 端口
        stat.match['eth_dst'] 目的地址
        stat.instructions[0].actions[0].port out 端口
        packet_count 转发包的数量
        byte_count   转发的比特数
        """
        body = ev.msg.body
        # self.logger.info('datapath         '
        #                  'in-port  eth-dst           '
        #                  'out-port packets  bytes')
        # self.logger.info('---------------- '
        #                  '-------- ----------------- '
        #                  '-------- -------- --------')
        # for stat in sorted([flow for flow in body if flow.priority == 1],
        #                    key=lambda flow: (flow.match['in_port'],
        #                                      flow.match['eth_dst'])):
        #     self.logger.info('%016x %8x %17s %8x %8d %8d',
        #                      ev.msg.datapath.id,
        #                      stat.match['in_port'], stat.match['eth_dst'],
        #                      stat.instructions[0].actions[0].port,
        #                      stat.packet_count, stat.byte_count)
        flow_table = sorted([flow for flow in body if flow.priority == 1], key=lambda flow: (flow.match['in_port'], flow.match['eth_dst']))
        ports = set()
        rx_packts, rx_bytes = defaultdict(list), defaultdict(list)
        tx_packts, tx_bytes = defaultdict(list), defaultdict(list)
        for stat in flow_table:
            in_port = stat.match['in_port']
            out_port = stat.instructions[0].actions[0].port
            ports.add(in_port), ports.add(out_port)
            rx_packts[in_port].append(stat.packet_count)
            rx_bytes[in_port].append(stat.byte_count)
            tx_packts[out_port].append(stat.packet_count)
            tx_bytes[out_port].append(stat.byte_count)
        for port in ports:
            data = {
                'datapath': str(ev.msg.datapath.id)+":"+str(port),
                'rx_packets': sum(rx_packts[port]),
                'rx_bytes': sum(rx_bytes[port]),
                'tx_packets': sum(tx_packts[port]),
                'tx_bytes': sum(tx_bytes[port])
            }
            print "c0 update %s flow-info" % data['datapath']
            requests.post(url=flow_url, data=json.dumps(data))

        flow_miss = [flow for flow in body if flow.priority == 0]
        m_packts, m_bytes = 0, 0
        for stat in flow_miss:
            m_packts += stat.packet_count
            m_bytes += stat.byte_count
        data = {
            'datapath': str(ev.msg.datapath.id),
            'packets': m_packts,
            'bytes': m_bytes,
        }
        print "c0 update %s flow-miss-info" % data['datapath']
        requests.post(url=miss_url, data=json.dumps(data))

    @set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)
    def _port_stats_reply_handler(self, ev):
        """
        该函数列出的是单个datapath中所有端口的流量
        ev.msg.datapath.id 被监控的datapath id
        stat.port_no    被监控的端口号
             rx_packets 该端口接收包的数量
             rx_bytes   该端口接收到的比特数
             rx_errors  该端口收到错误包的个数
             tx_packets 该端口发送包的数量
             tx_bytes   该端口发送的比特数
             tx_errors  该端口发送错误包的个数
        """
        body = ev.msg.body
        # self.logger.info('datapath         port     '
        #                  'rx-pkts  rx-bytes rx-error '
        #                  'tx-pkts  tx-bytes tx-error')
        # self.logger.info('---------------- -------- '
        #                  '-------- -------- -------- '
        #                  '-------- -------- --------')
        # for stat in sorted(body, key=attrgetter('port_no')):
        #     self.logger.info('%016x %8x %8d %8d %8d %8d %8d %8d',
        #                      ev.msg.datapath.id, stat.port_no,
        #                      stat.rx_packets, stat.rx_bytes, stat.rx_errors,
        #                      stat.tx_packets, stat.tx_bytes, stat.tx_errors)
        for stat in body:
            data = {
                'datapath': str(ev.msg.datapath.id)+":"+str(stat.port_no),
                'rx_packets': stat.rx_packets,
                'rx_bytes': stat.rx_bytes,
                'rx_errors': stat.rx_errors,
                'tx_packets': stat.tx_packets,
                'tx_bytes': stat.tx_bytes,
                'tx_error': stat.tx_packets
            }
            print "c0 update %s port-info" % data['datapath']
            requests.post(url=port_url, data=json.dumps(data))
