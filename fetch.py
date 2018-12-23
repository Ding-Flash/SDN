# -*- coding: utf-8 -*-
import requests

root = "http://127.0.0.1:5000"


def getdatapath(con):
    """
    :param con: 控制器名字 str类型
    :return: list 所有的datapath:port
    """
    con = "c"+str(con)
    url = root + '/getdatapath/' + con
    datapath = requests.get(url).json()['data']
    return datapath


def getall(con):
    """
    :param con:
    :return: 返回一个字典有所有的流量信息
    """
    con = "c"+str(con)
    url = root + '/getall/' + con
    allflow = requests.get(url).json()
    return allflow


def getflow(con):
    """
    :param con:
    :return: 返回字典 所有流表中的流量信息
    """
    con = "c"+str(con)
    url = root + '/getflow/' + con
    flow_table = requests.get(url).json()
    return flow_table


def getmiss(con):
    """
    :param con:
    :return: 返回字典 所有miss的流量
    """
    con = "c"+str(con)
    url = root + '/getmiss/' + con
    miss = requests.get(url).json()
    return miss
