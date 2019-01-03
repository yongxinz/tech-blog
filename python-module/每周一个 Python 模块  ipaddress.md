# 每周一个 Python 模块 | ipaddress

`ipaddress`模块包括用于处理 IPv4 和 IPv6 网络地址的类。这些类支持验证，查找网络上的地址和主机以及其他常见操作。

## 地址

最基本的对象代表网络地址本身。传递字符串，整数或字节序列给 `ip_address()` 来构造地址。返回值是 `IPv4Address` 或 `IPv6Address` 实例，具体取决于所使用的地址类型。

```python
import binascii
import ipaddress


ADDRESSES = [
    '10.9.0.6',
    'fdfd:87b5:b475:5e3e:b1bc:e121:a8eb:14aa',
]

for ip in ADDRESSES:
    addr = ipaddress.ip_address(ip)
    print('{!r}'.format(addr))
    print('   IP version:', addr.version)
    print('   is private:', addr.is_private)
    print('  packed form:', binascii.hexlify(addr.packed))
    print('      integer:', int(addr))
    print()
    
# output
# IPv4Address('10.9.0.6')
#    IP version: 4
#    is private: True
#   packed form: b'0a090006'
#       integer: 168361990
# 
# IPv6Address('fdfd:87b5:b475:5e3e:b1bc:e121:a8eb:14aa')
#    IP version: 6
#    is private: True
#   packed form: b'fdfd87b5b4755e3eb1bce121a8eb14aa'
#       integer: 337611086560236126439725644408160982186
```

还可以用这个方法来校验 IP 地址是否合法：

```python
import ipaddress


def  is_ip_Valid(ipaddr):
    try:
        ipaddress.ip_address(ipaddr);
        return True;
    except :
        return False;
     
if __name__ == '__main__':
    print(is_ip_Valid('2001:db8::'));
    print(is_ip_Valid('192.168.168.1'));
```

## 网络

网络是由一系列地址组成的，通常用地址和掩码这种形式来表示。

```python
import ipaddress

NETWORKS = [
    '10.9.0.0/24',
    'fdfd:87b5:b475:5e3e::/64',
]

for n in NETWORKS:
    net = ipaddress.ip_network(n)
    print('{!r}'.format(net))
    print('     is private:', net.is_private)
    print('      broadcast:', net.broadcast_address)
    print('     compressed:', net.compressed)
    print('   with netmask:', net.with_netmask)
    print('  with hostmask:', net.with_hostmask)
    print('  num addresses:', net.num_addresses)
    print()
    
# output
# IPv4Network('10.9.0.0/24')
#      is private: True
#       broadcast: 10.9.0.255
#      compressed: 10.9.0.0/24
#    with netmask: 10.9.0.0/255.255.255.0
#   with hostmask: 10.9.0.0/0.0.0.255
#   num addresses: 256
# 
# IPv6Network('fdfd:87b5:b475:5e3e::/64')
#      is private: True
#       broadcast: fdfd:87b5:b475:5e3e:ffff:ffff:ffff:ffff
#      compressed: fdfd:87b5:b475:5e3e::/64
#    with netmask: fdfd:87b5:b475:5e3e::/ffff:ffff:ffff:ffff::
#   with hostmask: fdfd:87b5:b475:5e3e::/::ffff:ffff:ffff:ffff
#   num addresses: 18446744073709551616
```

与地址一样，IPv4 和 IPv6网络有两种网络类。每个类提供用于访问与网络相关联的值的属性或方法，例如广播地址和可供主机使用的网络上的地址。

网络实例是可迭代的，并产生网络上的地址。

```python
import ipaddress

NETWORKS = [
    '10.9.0.0/24',
    'fdfd:87b5:b475:5e3e::/64',
]

for n in NETWORKS:
    net = ipaddress.ip_network(n)
    print('{!r}'.format(net))
    for i, ip in zip(range(3), net):
        print(ip)
    print()
    
# output
# IPv4Network('10.9.0.0/24')
# 10.9.0.0
# 10.9.0.1
# 10.9.0.2
# 
# IPv6Network('fdfd:87b5:b475:5e3e::/64')
# fdfd:87b5:b475:5e3e::
# fdfd:87b5:b475:5e3e::1
# fdfd:87b5:b475:5e3e::2
```

此示例仅打印一些地址，因为 IPv6 网络可以包含的地址远多于输出中的地址。

迭代网络会产生地址，但并非所有地址都对主机有效。例如，网络的基地址和广播地址。要查找网络上常规主机可以使用的地址，请使用 `hosts()` 方法，该方法会生成一个生成器。

```python
import ipaddress

NETWORKS = [
    '10.9.0.0/24',
    'fdfd:87b5:b475:5e3e::/64',
]

for n in NETWORKS:
    net = ipaddress.ip_network(n)
    print('{!r}'.format(net))
    for i, ip in zip(range(3), net.hosts()):
        print(ip)
    print()
    
# output
# IPv4Network('10.9.0.0/24')
# 10.9.0.1
# 10.9.0.2
# 10.9.0.3
# 
# IPv6Network('fdfd:87b5:b475:5e3e::/64')
# fdfd:87b5:b475:5e3e::1
# fdfd:87b5:b475:5e3e::2
# fdfd:87b5:b475:5e3e::3
```

将此示例的输出与前一示例进行比较表明，主机地址不包括在整个网络上进行迭代时生成的第一个值。

除了迭代器协议之外，网络还支持`in` 操作，来确定地址是否是网络的一部分。

```python
import ipaddress


NETWORKS = [
    ipaddress.ip_network('10.9.0.0/24'),
    ipaddress.ip_network('fdfd:87b5:b475:5e3e::/64'),
]

ADDRESSES = [
    ipaddress.ip_address('10.9.0.6'),
    ipaddress.ip_address('10.7.0.31'),
    ipaddress.ip_address('fdfd:87b5:b475:5e3e:b1bc:e121:a8eb:14aa'),
    ipaddress.ip_address('fe80::3840:c439:b25e:63b0'),
]


for ip in ADDRESSES:
    for net in NETWORKS:
        if ip in net:
            print('{}\nis on {}'.format(ip, net))
            break
    else:
        print('{}\nis not on a known network'.format(ip))
    print()
    
# output
# 10.9.0.6
# is on 10.9.0.0/24
# 
# 10.7.0.31
# is not on a known network
# 
# fdfd:87b5:b475:5e3e:b1bc:e121:a8eb:14aa
# is on fdfd:87b5:b475:5e3e::/64
# 
# fe80::3840:c439:b25e:63b0
# is not on a known network
```

`in`使用网络掩码来测试地址，因此它比扩展网络上的完整地址列表更有效。

## 接口

网络接口表示网络上的特定地址，并且可以由主机地址和网络前缀或网络掩码表示。

```python
import ipaddress


ADDRESSES = [
    '10.9.0.6/24',
    'fdfd:87b5:b475:5e3e:b1bc:e121:a8eb:14aa/64',
]


for ip in ADDRESSES:
    iface = ipaddress.ip_interface(ip)
    print('{!r}'.format(iface))
    print('network:\n  ', iface.network)
    print('ip:\n  ', iface.ip)
    print('IP with prefixlen:\n  ', iface.with_prefixlen)
    print('netmask:\n  ', iface.with_netmask)
    print('hostmask:\n  ', iface.with_hostmask)
    print()
    
# output
# IPv4Interface('10.9.0.6/24')
# network:
#    10.9.0.0/24
# ip:
#    10.9.0.6
# IP with prefixlen:
#    10.9.0.6/24
# netmask:
#    10.9.0.6/255.255.255.0
# hostmask:
#    10.9.0.6/0.0.0.255
# 
# IPv6Interface('fdfd:87b5:b475:5e3e:b1bc:e121:a8eb:14aa/64')
# network:
#    fdfd:87b5:b475:5e3e::/64
# ip:
#    fdfd:87b5:b475:5e3e:b1bc:e121:a8eb:14aa
# IP with prefixlen:
#    fdfd:87b5:b475:5e3e:b1bc:e121:a8eb:14aa/64
# netmask:
#    fdfd:87b5:b475:5e3e:b1bc:e121:a8eb:14aa/ffff:ffff:ffff:ffff::
# hostmask:
#    fdfd:87b5:b475:5e3e:b1bc:e121:a8eb:14aa/::ffff:ffff:ffff:ffff
```

接口对象具有分别访问完整网络和地址的属性，以及表达接口和网络掩码的几种不同方式。

相关文档：

https://pymotw.com/3/ipaddress/index.html