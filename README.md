## 环境配置说明

### 代码下载
```
git clone git@github.com:Ding-Flash/SDN.git
```

### 系统 
需要在ubuntu系统下执行 请自行安装ubuntu

### python版本
需要python版本为2.7 需要安装pip

### mininet安装
[mininet安装地址](http://mininet.org/download/#option-2-native-installation-from-source)
使用下载源码方式安装mininet

### 依赖安装

```
pip install -r requirements.txt
```

### 运行代码
首先运行flask，控制器和交换机使用flask进行通信
```
python web.py
```
启动控制器，现在先模拟最简单的场景，启动两个控制器
```
ryu-manager monitor_c0.py --ofp-tcp-listen-port=6633
ryu-manager monitor_c1.py --ofp-tcp-listen-port=6634
```

### 编写测试代码
新建py文件，从topo.py引入network,通过
```
net = netowrk()
```
可获得Mininet对象，该对象的所有属性和方法可以去官网查看，从fetch.py文件中引入各种方法，获取到控制器下所有交换机的流量。
1. `getdatapath(con)`获取到控制器con下的所有的datapath，由datapath:port组成。
2. `getall(con)`获得所有流量信息
3. `getmiss(con)` 获得发送给控制器的流量

**交换器切换控制器**
1. 使用net获取到交换机 `s1 = net.get('s1')`
2. `s1.start([c0, c1])`


