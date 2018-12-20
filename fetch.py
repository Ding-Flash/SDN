# -*- coding: utf-8 -*-
import requests

root = "http://127.0.0.1:5000"


def getdatapath(con):
    """
    :param con: 控制器index int
    :return: list 所有的datapath:port
    """
    url = root + '/getdatapath/' +'c'+ str(con)
    datapath = requests.get(url).json()['data']
    return datapath


def getall(con):
    """
    :param con:
    :return: 返回一个字典有所有的流量信息
    """
    url = root + '/getall/' +'c'+ str(con)
    allflow = requests.get(url).json()
    return allflow


def getflow(con):
    """
    :param con:
    :return: 返回字典 所有流表中的流量信息
    """
    url = root + '/getflow/' +'c'+ str(con)
    flow_table = requests.get(url).json()
    return flow_table


def getmiss(con):
    """
    :param con:
    :return: 返回字典 所有miss的流量
    """
    url = root + '/getmiss/' +'c'+ str(con)
    miss = requests.get(url).json()
    return miss
