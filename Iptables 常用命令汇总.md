# Iptables 常用命令汇总

### 基本操作

启动 iptables ：

```
service iptables start
```

关闭 iptables ：

```
service iptables stop
```

重启 iptables ：

```
service iptables restart
```

查看 iptables 状态：

```
service iptables status
```

保存 iptables 配置：

```
service iptables save
```

Iptables 服务配置文件：

```
/etc/sysconfig/iptables-config
```

Iptables 规则保存文件：

```
/etc/sysconfig/iptables
```

打开 iptables 转发：

```
echo "1"> /proc/sys/net/ipv4/ip_forward
```

### 常用命令

删除 iptables 现有规则：

```
iptables –F 
```

查看 iptables 规则：

```
iptables –L（iptables –L –v -n）
```

增加一条规则到最后：

```
iptables -A INPUT -i eth0 -p tcp --dport 80 -m state --state NEW,ESTABLISHED -j ACCEPT 
```

添加一条规则到指定位置：

```
iptables -I INPUT 2 -i eth0 -p tcp --dport 80 -m state --state NEW,ESTABLISHED -j ACCEPT 
```

删除一条规则：

```
iptabels -D INPUT 2 
```

修改一条规则：

```
iptables -R INPUT 3 -i eth0 -p tcp --dport 80 -m state --state NEW,ESTABLISHED -j ACCEPT 
```

设置默认策略：

```
iptables -P INPUT DROP 
```

允许远程主机进行 SSH 连接：

```
iptables -A INPUT -i eth0 -p tcp --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT iptables -A OUTPUT -o eth0 -p tcp --sport 22 -m state --state ESTABLISHED -j ACCEPT 
```

允许本地主机进行 SSH 连接：

```
iptables -A OUTPUT -o eth0 -p tcp --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT iptables -A INTPUT -i eth0 -p tcp --sport 22 -m state --state ESTABLISHED -j ACCEPT
```

允许 HTTP 请求：

```
iptables -A INPUT -i eth0 -p tcp --dport 80 -m state --state NEW,ESTABLISHED -j ACCEPT iptables -A OUTPUT -o eth0 -p tcp --sport 80 -m state --state ESTABLISHED -j ACCEPT 
```

限制 ping 192.168.146.3 主机的数据包数，平均 2/s 个，最多不能超过 3 个：

```
iptables -A INPUT -i eth0 -d 192.168.146.3 -p icmp --icmp-type 8 -m limit --limit 2/second --limit-burst 3 -j ACCEPT 
```

限制 SSH 连接速率 ( 默认策略是 DROP)：

```
iptables -I INPUT 1 -p tcp --dport 22 -d 192.168.146.3 -m state --state ESTABLISHED -j ACCEPT  
iptables -I INPUT 2 -p tcp --dport 22 -d 192.168.146.3 -m limit --limit 2/minute --limit-burst 2 -m state --state NEW -j ACCEPT 
```

参考文档：

https://www.91yun.co/archives/1690

https://www.cnblogs.com/Dicky-Zhang/p/5904429.html