# 每周一个 Python 模块 | socket

`Socket` 提供了标准的 BSD Socket API，以便使用 BSD 套接字接口通过网络进行通信。它包括用于处理实际数据通道的类，还包括与网络相关的功能，例如将服务器的名称转换为地址以及格式化要通过网络发送的数据。

## 寻址、协议族和套接字类型

socket 是由程序用来传递数据或通过互联网通信的信道的一个端点。套接字有两个主要属性来控制它们发送数据的方式： 地址族控制所使用的 OSI 网络层协议， 以及套接字类型控制传输层协议。

Python 支持三种地址族。最常见的是 `AF_INET`，用于 IPv4 网络寻址。IPv4 地址长度为四个字节，通常表示为四个数字的序列，每八字节一个，用点分隔（例如，`10.1.1.5`和`127.0.0.1`）。这些值通常被称为 IP 地址。

`AF_INET6`用于IPv6 网络寻址。IPv6 是网络协议的下一代版本，支持 IPv4 下不可用的 128 位地址，流量整型和路由功能。IPv6 的采用率持续增长，特别是随着云计算的发展，以及由于物联网项目而添加到网络中的额外设备的激增。

`AF_UNIX`是 Unix 域套接字（UDS）的地址族，它是 POSIX 兼容系统上可用的进程间通信协议。UDS 的实现允许操作系统将数据直接从一个进程传递到另一个进程，而无需通过网络堆栈。这比使用 `AF_INET` 更高效，但由于文件系统用作寻址的命名空间，因此 UDS 仅限于同一系统上的进程。使用 UDS 而不是其他 IPC 机制（如命名管道或共享内存）的吸引力在于编程接口与 IP 网络相同，因此应用程序可以在单个主机上运行时高效通信。

注意：`AF_UNIX`常量仅定义在支持 UDS 的系统上。

套接字类型通常用 `SOCK_DGRAM` 处理面向消息的数据报传输，用 `SOCK_STREAM` 处理面向字节流的传输。数据报套接字通常与 UDP（用户数据报协议）相关联 ，它们提供不可靠的单个消息传递。面向流的套接字与 TCP（传输控制协议）相关联 。它们在客户端和服务器之间提供字节流，通过超时管理，重传和其他功能确保消息传递或故障通知。

大多数提供大量数据的应用程序协议（如 HTTP）都是基于 TCP 构建的，因为它可以在自动处理消息排序和传递时更轻松地创建复杂的应用程序。UDP 通常用于消息不太重要的协议（例如通过 DNS 查找名称），或者用于多播（将相同数据发送到多个主机）。UDP 和 TCP 都可以与 IPv4 或 IPv6 寻址一起使用。

注意：Python 的`socket`模块还支持其他套接字类型，但不太常用，因此这里不做介绍。有关更多详细信息，请参阅标准库文档。

### 在网络上查找主机

`socket` 包含与网络域名服务接口相关的功能，因此程序可以将服务器主机名转换为其数字网络地址。虽然程序在使用它们连接服务器之前不需要显式转换地址，但在报错时，包含数字地址以及使用的名称会很有用。

要查找当前主机的正式名称，可以使用 `gethostname()`。

```python
import socket

print(socket.gethostname())	# apu.hellfly.net
```

返回的名称取决于当前系统的网络设置，如果位于不同的网络（例如连接到无线 LAN 的笔记本电脑），则可能会更改。

使用 `gethostbyname()` 将服务器名称转换为它的数字地址。

```python
import socket

HOSTS = [
    'apu',
    'pymotw.com',
    'www.python.org',
    'nosuchname',
]

for host in HOSTS:
    try:
        print('{} : {}'.format(host, socket.gethostbyname(host)))
    except socket.error as msg:
        print('{} : {}'.format(host, msg))
        
# output
# apu : 10.9.0.10
# pymotw.com : 66.33.211.242
# www.python.org : 151.101.32.223
# nosuchname : [Errno 8] nodename nor servname provided, or not known
```

如果当前系统的 DNS 配置在搜索中包含一个或多个域，则 name 参数不必要是完整的名称（即，它不需要包括域名以及基本主机名）。如果找不到该名称，则会引发 `socket.error` 类型异常。

要访问服务器的更多命名信息，请使用 `gethostbyname_ex()`。它返回服务器的规范主机名，别名以及可用于访问它的所有可用 IP 地址。

```python
import socket

HOSTS = [
    'apu',
    'pymotw.com',
    'www.python.org',
    'nosuchname',
]

for host in HOSTS:
    print(host)
    try:
        name, aliases, addresses = socket.gethostbyname_ex(host)
        print('  Hostname:', name)
        print('  Aliases :', aliases)
        print(' Addresses:', addresses)
    except socket.error as msg:
        print('ERROR:', msg)
    print()
    
# output
# apu
#   Hostname: apu.hellfly.net
#   Aliases : ['apu']
#  Addresses: ['10.9.0.10']
# 
# pymotw.com
#   Hostname: pymotw.com
#   Aliases : []
#  Addresses: ['66.33.211.242']
# 
# www.python.org
#   Hostname: prod.python.map.fastlylb.net
#   Aliases : ['www.python.org', 'python.map.fastly.net']
#  Addresses: ['151.101.32.223']
# 
# nosuchname
# ERROR: [Errno 8] nodename nor servname provided, or not known
```

拥有服务器的所有已知 IP 地址后，客户端可以实现自己的负载均衡或故障转移算法。

使用`getfqdn()` 将部分名称转换为一个完整的域名。

```python
import socket

for host in ['apu', 'pymotw.com']:
    print('{:>10} : {}'.format(host, socket.getfqdn(host)))
    
# output
#        apu : apu.hellfly.net
# pymotw.com : apache2-echo.catalina.dreamhost.com
```

如果输入是别名，则返回的名称不一定与输入参数匹配，例如此处的 `www`。

当服务器地址可用时，使用`gethostbyaddr()` 对名称执行“反向”查找。

```python
import socket

hostname, aliases, addresses = socket.gethostbyaddr('10.9.0.10')

print('Hostname :', hostname)	# Hostname : apu.hellfly.net
print('Aliases  :', aliases)	# Aliases  : ['apu']
print('Addresses:', addresses)	# Addresses: ['10.9.0.10']
```

返回值是一个元组，包含完整主机名，别名以及与该名称关联的所有 IP 地址。

### 查找服务信息

除 IP 地址外，每个套接字地址还包括一个整数端口号。许多应用程序可以在同一主机上运行，监听单个 IP 地址，但一次只能有一个套接字可以使用该地址的端口。IP 地址，协议和端口号的组合唯一地标识通信信道，并确保通过套接字发送的消息到达正确的目的地。

某些端口号是为特定协议预先分配的。例如，使用 SMTP 的电子邮件服务器之间的通信，使用 TCP 在端口号 25 上进行，而 Web 客户端和服务器使用端口 80 进行 HTTP 通信。可以使用 `getservbyname()` 查找具有标准化名称的网络服务的端口号。

```python
import socket
from urllib.parse import urlparse

URLS = [
    'http://www.python.org',
    'https://www.mybank.com',
    'ftp://prep.ai.mit.edu',
    'gopher://gopher.micro.umn.edu',
    'smtp://mail.example.com',
    'imap://mail.example.com',
    'imaps://mail.example.com',
    'pop3://pop.example.com',
    'pop3s://pop.example.com',
]

for url in URLS:
    parsed_url = urlparse(url)
    port = socket.getservbyname(parsed_url.scheme)
    print('{:>6} : {}'.format(parsed_url.scheme, port))
    
# output
#   http : 80
#  https : 443
#    ftp : 21
# gopher : 70
#   smtp : 25
#   imap : 143
#  imaps : 993
#   pop3 : 110
#  pop3s : 995
```

虽然标准化服务不太可能改变端口，但是在未来添加新服务时，通过系统调用来查找而不是硬编码会更灵活。

要反转服务端口查找，使用`getservbyport()`。

```python
import socket
from urllib.parse import urlunparse

for port in [80, 443, 21, 70, 25, 143, 993, 110, 995]:
    url = '{}://example.com/'.format(socket.getservbyport(port))
    print(url)
    
# output
# http://example.com/
# https://example.com/
# ftp://example.com/
# gopher://example.com/
# smtp://example.com/
# imap://example.com/
# imaps://example.com/
# pop3://example.com/
# pop3s://example.com/
```

反向查找对于从任意地址构造服务的 URL 非常有用。

可以使用 `getprotobyname()` 检索分配给传输协议的编号。

```python
import socket


def get_constants(prefix):
    """Create a dictionary mapping socket module
    constants to their names.
    """
    return {
        getattr(socket, n): n for n in dir(socket) if n.startswith(prefix)
    }


protocols = get_constants('IPPROTO_')

for name in ['icmp', 'udp', 'tcp']:
    proto_num = socket.getprotobyname(name)
    const_name = protocols[proto_num]
    print('{:>4} -> {:2d} (socket.{:<12} = {:2d})'.format(
        name, proto_num, const_name,
        getattr(socket, const_name)))
    
# output
# icmp ->  1 (socket.IPPROTO_ICMP =  1)
#  udp -> 17 (socket.IPPROTO_UDP  = 17)
#  tcp ->  6 (socket.IPPROTO_TCP  =  6)
```

协议号的值是标准化的，用前缀 `IPPROTO_` 定义为常量。

### 查找服务器地址

`getaddrinfo()` 将服务的基本地址转换为元组列表，其中包含建立连接所需的所有信息。每个元组的内容会有所不同，包含不同的网络地址族或协议。

```python
import socket


def get_constants(prefix):
    """Create a dictionary mapping socket module
    constants to their names.
    """
    return {
        getattr(socket, n): n for n in dir(socket) if n.startswith(prefix)
    }


families = get_constants('AF_')
types = get_constants('SOCK_')
protocols = get_constants('IPPROTO_')

for response in socket.getaddrinfo('www.python.org', 'http'):

    # Unpack the response tuple
    family, socktype, proto, canonname, sockaddr = response

    print('Family        :', families[family])
    print('Type          :', types[socktype])
    print('Protocol      :', protocols[proto])
    print('Canonical name:', canonname)
    print('Socket address:', sockaddr)
    print()
    
# output
# Family        : AF_INET
# Type          : SOCK_DGRAM
# Protocol      : IPPROTO_UDP
# Canonical name:
# Socket address: ('151.101.32.223', 80)
# 
# Family        : AF_INET
# Type          : SOCK_STREAM
# Protocol      : IPPROTO_TCP
# Canonical name:
# Socket address: ('151.101.32.223', 80)
# 
# Family        : AF_INET6
# Type          : SOCK_DGRAM
# Protocol      : IPPROTO_UDP
# Canonical name:
# Socket address: ('2a04:4e42:8::223', 80, 0, 0)
# 
# Family        : AF_INET6
# Type          : SOCK_STREAM
# Protocol      : IPPROTO_TCP
# Canonical name:
# Socket address: ('2a04:4e42:8::223', 80, 0, 0)
```

该程序演示了如何查找 `www.python.org` 的连接信息。

`getaddrinfo()`采用几个参数来过滤结果列表。`host`和`port`是必传参数。可选的参数是`family`， `socktype`，`proto`，和`flags`。可选值应该是`0`或由 `socket` 定义的常量之一。

```python
import socket


def get_constants(prefix):
    """Create a dictionary mapping socket module
    constants to their names.
    """
    return {
        getattr(socket, n): n for n in dir(socket) if n.startswith(prefix)
    }


families = get_constants('AF_')
types = get_constants('SOCK_')
protocols = get_constants('IPPROTO_')

responses = socket.getaddrinfo(
    host='www.python.org',
    port='http',
    family=socket.AF_INET,
    type=socket.SOCK_STREAM,
    proto=socket.IPPROTO_TCP,
    flags=socket.AI_CANONNAME,
)

for response in responses:
    # Unpack the response tuple
    family, socktype, proto, canonname, sockaddr = response

    print('Family        :', families[family])
    print('Type          :', types[socktype])
    print('Protocol      :', protocols[proto])
    print('Canonical name:', canonname)
    print('Socket address:', sockaddr)
    print()
    
# output
# Family        : AF_INET
# Type          : SOCK_STREAM
# Protocol      : IPPROTO_TCP
# Canonical name: prod.python.map.fastlylb.net
# Socket address: ('151.101.32.223', 80)
```

由于`flags`包含`AI_CANONNAME`，服务器的规范名称（可能与主机具有别名时用于查找的值不同）包含在结果中。如果没有该标志，则规范名称将保留为空。

### IP 地址表示

用 C 编写的网络程序使用数据类型将 IP 地址表示为二进制值（而不是通常在 Python 程序中的字符串地址）。要在 Python 表示和 C 表示之间转换 IPv4 地址，请使用`structsockaddr`、`inet_aton()` 和 `inet_ntoa()`。

```python
import binascii
import socket
import struct
import sys

for string_address in ['192.168.1.1', '127.0.0.1']:
    packed = socket.inet_aton(string_address)
    print('Original:', string_address)
    print('Packed  :', binascii.hexlify(packed))
    print('Unpacked:', socket.inet_ntoa(packed))
    print()
    
# output
# Original: 192.168.1.1
# Packed  : b'c0a80101'
# Unpacked: 192.168.1.1
# 
# Original: 127.0.0.1
# Packed  : b'7f000001'
# Unpacked: 127.0.0.1
```

打包格式中的四个字节可以传递给 C 库，通过网络安全传输，或者紧凑地保存到数据库中。

相关函数 `inet_pton()` 和 `inet_ntop()` 支持 IPv4 和 IPv6，根据传入的地址族参数生成适当的格式。

```python
import binascii
import socket
import struct
import sys

string_address = '2002:ac10:10a:1234:21e:52ff:fe74:40e'
packed = socket.inet_pton(socket.AF_INET6, string_address)

print('Original:', string_address)
print('Packed  :', binascii.hexlify(packed))
print('Unpacked:', socket.inet_ntop(socket.AF_INET6, packed))

# output
# Original: 2002:ac10:10a:1234:21e:52ff:fe74:40e
# Packed  : b'2002ac10010a1234021e52fffe74040e'
# Unpacked: 2002:ac10:10a:1234:21e:52ff:fe74:40e
```

IPv6 地址已经是十六进制值，因此将打包版本转换为一系列十六进制数字会生成类似于原始值的字符串。

## TCP/IP 客户端和服务端

Sockets 可以作为服务端并监听传入消息，或作为客户端连接其他应用程序。连接 TCP/IP 套接字的两端后，通信是双向的。

### 服务端

此示例程序基于标准库文档中的示例程序，接收传入的消息并将它们回送给发送方。它首先创建一个 TCP/IP 套接字，然后用 `bind()` 将套接字与服务器地址相关联。地址是`localhost`指当前服务器，端口号是 10000。

```python
# socket_echo_server.py
import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            print('received {!r}'.format(data))
            if data:
                print('sending data back to the client')
                connection.sendall(data)
            else:
                print('no data from', client_address)
                break

    finally:
        # Clean up the connection
        connection.close()
```

调用`listen()`将套接字置于服务器模式，并用 `accept()`等待传入连接。整数参数表示后台排队的连接数，当连接数超出时，系统会拒绝。此示例仅期望一次使用一个连接。

`accept()`返回服务器和客户端之间的开放连接以及客户端的地址。该连接实际上是另一个端口上的不同套接字（由内核分配）。从连接中用 `recv()` 读取数据并用 `sendall()` 传输数据。

与客户端通信完成后，需要使用 `close()` 清理连接。此示例使用 `try:finally`块来确保`close()`始终调用，即使出现错误也是如此。

### 客户端

客户端程序的 `socket` 设置与服务端的不同。它不是绑定到端口并监听，而是用于`connect()`将套接字直接连接到远程地址。

```python
# socket_echo_client.py
import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

try:

    # Send data
    message = b'This is the message.  It will be repeated.'
    print('sending {!r}'.format(message))
    sock.sendall(message)

    # Look for the response
    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print('received {!r}'.format(data))

finally:
    print('closing socket')
    sock.close()
```

建立连接后，数据可以通过 `sendall()` 发送 `recv()` 接收。发送整个消息并收到同样的回复后，关闭套接字以释放端口。

### 运行客户端和服务端

客户端和服务端应该在单独的终端窗口中运行，以便它们可以相互通信。服务端输出显示传入的连接和数据，以及发送回客户端的响应。

```python
$ python3 socket_echo_server.py
starting up on localhost port 10000
waiting for a connection
connection from ('127.0.0.1', 65141)
received b'This is the mess'
sending data back to the client
received b'age.  It will be'
sending data back to the client
received b' repeated.'
sending data back to the client
received b''
no data from ('127.0.0.1', 65141)
waiting for a connection
```

客户端输出显示传出消息和来自服务端的响应。

```python
$ python3 socket_echo_client.py
connecting to localhost port 10000
sending b'This is the message.  It will be repeated.'
received b'This is the mess'
received b'age.  It will be'
received b' repeated.'
closing socket
```

### 简易客户端连接

通过使用便捷功能`create_connection()`连接到服务端，TCP/IP 客户端可以节省一些步骤 。该函数接受一个参数，一个包含服务器地址的双值元组，并派生出用于连接的最佳地址。

```python
import socket
import sys


def get_constants(prefix):
    """Create a dictionary mapping socket module
    constants to their names.
    """
    return {
        getattr(socket, n): n for n in dir(socket) if n.startswith(prefix)
    }


families = get_constants('AF_')
types = get_constants('SOCK_')
protocols = get_constants('IPPROTO_')

# Create a TCP/IP socket
sock = socket.create_connection(('localhost', 10000))

print('Family  :', families[sock.family])
print('Type    :', types[sock.type])
print('Protocol:', protocols[sock.proto])
print()

try:

    # Send data
    message = b'This is the message.  It will be repeated.'
    print('sending {!r}'.format(message))
    sock.sendall(message)

    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print('received {!r}'.format(data))

finally:
    print('closing socket')
    sock.close()
    
# output
# Family  : AF_INET
# Type    : SOCK_STREAM
# Protocol: IPPROTO_TCP
# 
# sending b'This is the message.  It will be repeated.'
# received b'This is the mess'
# received b'age.  It will be'
# received b' repeated.'
# closing socket
```

`create_connection()`用`getaddrinfo()` 方法获得可选参数，并`socket`使用创建成功连接的第一个配置返回已打开的连接参数。`family`，`type`和`proto`属性可以用来检查返回的类型是 socket 类型。

### 选择监听地址

将服务端绑定到正确的地址非常重要，以便客户端可以与之通信。前面的示例都用 `'localhost'` 作为 IP 地址，但这样有一个限制，只有在同一服务器上运行的客户端才能连接。使用服务器的公共地址（例如 `gethostname()` 的返回值）来允许其他主机进行连接。修改上面的例子，让服务端监听通过命令行参数指定的地址。

```python
# socket_echo_server_explicit.py
import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address given on the command line
server_name = sys.argv[1]
server_address = (server_name, 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)
sock.listen(1)

while True:
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('client connected:', client_address)
        while True:
            data = connection.recv(16)
            print('received {!r}'.format(data))
            if data:
                connection.sendall(data)
            else:
                break
    finally:
        connection.close()
```

对客户端程序进行类似的修改。

```python
# socket_echo_client_explicit.py
import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port on the server
# given by the caller
server_address = (sys.argv[1], 10000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

try:

    message = b'This is the message.  It will be repeated.'
    print('sending {!r}'.format(message))
    sock.sendall(message)

    amount_received = 0
    amount_expected = len(message)
    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print('received {!r}'.format(data))

finally:
    sock.close()
```

使用参数 `hubert` 启动服务端， `netstat`命令显示它正在监听指定主机的地址。

```python
$ host hubert.hellfly.net

hubert.hellfly.net has address 10.9.0.6

$ netstat -an | grep 10000

Active Internet connections (including servers)
Proto Recv-Q Send-Q  Local Address          Foreign Address        (state)
...
tcp4       0      0  10.9.0.6.10000         *.*                    LISTEN
...
```

在另一台主机上运行客户端，`hubert.hellfly.net` 作为参数：

```python
$ hostname

apu

$ python3 ./socket_echo_client_explicit.py hubert.hellfly.net
connecting to hubert.hellfly.net port 10000
sending b'This is the message.  It will be repeated.'
received b'This is the mess'
received b'age.  It will be'
received b' repeated.'
```

服务端输出是：

```python
$ python3 socket_echo_server_explicit.py hubert.hellfly.net
starting up on hubert.hellfly.net port 10000
waiting for a connection
client connected: ('10.9.0.10', 33139)
received b''
waiting for a connection
client connected: ('10.9.0.10', 33140)
received b'This is the mess'
received b'age.  It will be'
received b' repeated.'
received b''
waiting for a connection
```

许多服务端具有多个网络接口，因此也会有多个 IP 地址连接。为每个 IP 地址运行服务端肯定是不明智的，可以使用特殊地址`INADDR_ANY` 同时监听所有地址。尽管 `socket` 为 `INADDR_ANY` 定义了一个常量，但它是一个整数，必须先将其转换为点符号分隔的字符串地址才能传递给 `bind()`。作为更方便的方式，使用“ `0.0.0.0`”或空字符串（`''`）就可以了，而不是进行转换。

```python
import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address given on the command line
server_address = ('', 10000)
sock.bind(server_address)
print('starting up on {} port {}'.format(*sock.getsockname()))
sock.listen(1)

while True:
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('client connected:', client_address)
        while True:
            data = connection.recv(16)
            print('received {!r}'.format(data))
            if data:
                connection.sendall(data)
            else:
                break
    finally:
        connection.close()
```

要查看套接字使用的实际地址，可以使用 `getsockname()` 方法。启动服务后，再次运行 `netstat` 会显示它正在监听任何地址上的传入连接。

```python
$ netstat -an

Active Internet connections (including servers)
Proto Recv-Q Send-Q  Local Address    Foreign Address  (state)
...
tcp4       0      0  *.10000          *.*              LISTEN
...
```

## 用户数据报客户端和服务端

用户数据报协议（UDP）与 TCP/IP 的工作方式不同。TCP 是面向字节流的，所有数据以正确的顺序传输，UDP 是面向消息的协议。UDP 不需要长连接，因此设置 UDP 套接字更简单一些。另一方面，UDP 消息必须适合单个数据报（对于 IPv4，这意味着它们只能容纳 65,507 个字节，因为 65,535 字节的数据包也包含头信息）并且不能保证传送与 TCP 一样可靠。

### 服务端

由于没有连接本身，服务器不需要监听和接收连接。它只需要 `bind()` 地址和端口，然后等待单个消息。

```python
# socket_echo_server_dgram.py 
import socket
import sys

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

while True:
    print('\nwaiting to receive message')
    data, address = sock.recvfrom(4096)

    print('received {} bytes from {}'.format(len(data), address))
    print(data)

    if data:
        sent = sock.sendto(data, address)
        print('sent {} bytes back to {}'.format(sent, address))
```

使用 `recvfrom()` 从套接字读取消息，然后按照客户端地址返回数据。

### 客户端

UDP 客户端与服务端类似，但不需要 `bind()`。它用 `sendto()`将消息直接发送到服务算，并用 `recvfrom()`接收响应。

```python
# socket_echo_client_dgram.py 
import socket
import sys

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 10000)
message = b'This is the message.  It will be repeated.'

try:

    # Send data
    print('sending {!r}'.format(message))
    sent = sock.sendto(message, server_address)

    # Receive response
    print('waiting to receive')
    data, server = sock.recvfrom(4096)
    print('received {!r}'.format(data))

finally:
    print('closing socket')
    sock.close()
```

### 运行客户端和服务端

运行服务端会产生：

```python
$ python3 socket_echo_server_dgram.py
starting up on localhost port 10000

waiting to receive message
received 42 bytes from ('127.0.0.1', 57870)
b'This is the message.  It will be repeated.'
sent 42 bytes back to ('127.0.0.1', 57870)

waiting to receive message
```

客户端输出是：

```python
$ python3 socket_echo_client_dgram.py
sending b'This is the message.  It will be repeated.'
waiting to receive
received b'This is the message.  It will be repeated.'
closing socket
```

## Unix 域套接字

从程序员的角度来看，使用 Unix 域套接字和 TCP/IP 套接字有两个本质区别。首先，套接字的地址是文件系统上的路径，而不是包含服务器名称和端口的元组。其次，在套接字关闭后，在文件系统中创建的表示套接字的节点仍然存在，并且每次服务端启动时都需要删除。通过在设置部分进行一些更改，使之前的服务端程序支持 UDS。

创建 socket 时使用地址族 `AF_UNIX`。绑定套接字和管理传入连接方式与 TCP/IP 套接字相同。

```python
# socket_echo_server_uds.py 
import socket
import sys
import os

server_address = './uds_socket'

# Make sure the socket does not already exist
try:
    os.unlink(server_address)
except OSError:
    if os.path.exists(server_address):
        raise

# Create a UDS socket
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# Bind the socket to the address
print('starting up on {}'.format(server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            print('received {!r}'.format(data))
            if data:
                print('sending data back to the client')
                connection.sendall(data)
            else:
                print('no data from', client_address)
                break

    finally:
        # Clean up the connection
        connection.close()
```

还需要修改客户端设置以使用 UDS。它应该假定套接字的文件系统节点存在，因为服务端通过绑定到该地址来创建它。发送和接收数据在 UDS 客户端中的工作方式与之前的 TCP/IP 客户端相同。

```python
# socket_echo_client_uds.py 
import socket
import sys

# Create a UDS socket
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = './uds_socket'
print('connecting to {}'.format(server_address))
try:
    sock.connect(server_address)
except socket.error as msg:
    print(msg)
    sys.exit(1)

try:

    # Send data
    message = b'This is the message.  It will be repeated.'
    print('sending {!r}'.format(message))
    sock.sendall(message)

    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print('received {!r}'.format(data))

finally:
    print('closing socket')
    sock.close()
```

程序输出大致相同，并对地址信息进行适当更新。服务端显示收到的消息并将其发送回客户端。

```python
$ python3 socket_echo_server_uds.py
starting up on ./uds_socket
waiting for a connection
connection from
received b'This is the mess'
sending data back to the client
received b'age.  It will be'
sending data back to the client
received b' repeated.'
sending data back to the client
received b''
no data from
waiting for a connection
```

客户端一次性发送消息，并以递增方式接收部分消息。

```python
$ python3 socket_echo_client_uds.py
connecting to ./uds_socket
sending b'This is the message.  It will be repeated.'
received b'This is the mess'
received b'age.  It will be'
received b' repeated.'
closing socket
```

### 权限

由于 UDS 套接字由文件系统上的节点表示，因此可以使用标准文件系统权限来控制服务端的访问。

```python
$ ls -l ./uds_socket

srwxr-xr-x  1 dhellmann  dhellmann  0 Aug 21 11:19 uds_socket

$ sudo chown root ./uds_socket

$ ls -l ./uds_socket

srwxr-xr-x  1 root  dhellmann  0 Aug 21 11:19 uds_socket
```

以非`root`用户运行客户端会导致错误，因为该进程无权打开套接字。

```python
$ python3 socket_echo_client_uds.py

connecting to ./uds_socket
[Errno 13] Permission denied
```

### 父子进程之间的通信

为了在 Unix 下进行进程间通信，通过 `socketpair()` 函数来设置 UDS 套接字很有用。它创建了一对连接的套接字，当子进程被创建后，在父进程和子进程之间进行通信。

```python
import socket
import os

parent, child = socket.socketpair()

pid = os.fork()

if pid:
    print('in parent, sending message')
    child.close()
    parent.sendall(b'ping')
    response = parent.recv(1024)
    print('response from child:', response)
    parent.close()

else:
    print('in child, waiting for message')
    parent.close()
    message = child.recv(1024)
    print('message from parent:', message)
    child.sendall(b'pong')
    child.close()
    
# output
# in parent, sending message
# in child, waiting for message
# message from parent: b'ping'
# response from child: b'pong'
```

默认情况下，会创建一个 UDS 套接字，但也可以传递地址族，套接字类型甚至协议选项来控制套接字的创建方式。

## 组播

点对点连接可以处理大量通信需求，但随着直接连接数量的增加，同时给多个接收者传递相同的信息变得具有挑战性。分别向每个接收者发送消息会消耗额外的处理时间和带宽，这对于诸如流式视频或音频之类的应用来说可能是个问题。使用组播一次向多个端点传递消息可以使效率更高。

组播消息通过 UDP 发送，因为 TCP 是一对一的通信系统。组播地址（称为 组播组）是为组播流量保留的常规 IPv4 地址范围（224.0.0.0到230.255.255.255）的子集。这些地址由网络路由器和交换机专门处理，因此发送到该组的邮件可以通过 Internet 分发给已加入该组的所有收件人。

注意：某些托管交换机和路由器默认禁用组播流量。如果在使用示例程序时遇到问题，请检查网络硬件设置。

### 发送组播消息

修改上面的客户端程序使其向组播组发送消息，然后报告它收到的所有响应。由于无法知道预期会有多少响应，因此它会使用套接字的超时值来避免在等待答案时无限期地阻塞。

套接字还需要配置消息的生存时间值（TTL）。TTL 控制接收数据包的网络数量。使用`IP_MULTICAST_TTL` 和 `setsockopt()` 设置 TTL。默认值`1`表示路由器不会将数据包转发到当前网段之外。该值最大可达 `255`，并且应打包为单个字节。

```python
# socket_multicast_sender.py 
import socket
import struct
import sys

message = b'very important data'
multicast_group = ('224.3.29.71', 10000)

# Create the datagram socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set a timeout so the socket does not block
# indefinitely when trying to receive data.
sock.settimeout(0.2)

# Set the time-to-live for messages to 1 so they do not
# go past the local network segment.
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

try:

    # Send data to the multicast group
    print('sending {!r}'.format(message))
    sent = sock.sendto(message, multicast_group)

    # Look for responses from all recipients
    while True:
        print('waiting to receive')
        try:
            data, server = sock.recvfrom(16)
        except socket.timeout:
            print('timed out, no more responses')
            break
        else:
            print('received {!r} from {}'.format(data, server))

finally:
    print('closing socket')
    sock.close()
```

发件人的其余部分看起来像 UDP 客户端，除了它需要多个响应，因此使用循环调用 `recvfrom()` 直到超时。

### 接收组播消息

建立组播接收器的第一步是创建 UDP 套接字。创建常规套接字并绑定到端口后，可以使用`setsockopt()`更改`IP_ADD_MEMBERSHIP`选项将其添加到组播组。选项值是组播组地址的 8 字节打包表示，后跟服务端监听流量的网络接口，由其 IP 地址标识。在这种情况下，接收端使用 `INADDR_ANY` 所有接口。

```python
# socket_multicast_receiver.py 
import socket
import struct
import sys

multicast_group = '224.3.29.71'
server_address = ('', 10000)

# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the server address
sock.bind(server_address)

# Tell the operating system to add the socket to
# the multicast group on all interfaces.
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Receive/respond loop
while True:
    print('\nwaiting to receive message')
    data, address = sock.recvfrom(1024)

    print('received {} bytes from {}'.format(len(data), address))
    print(data)

    print('sending acknowledgement to', address)
    sock.sendto(b'ack', address)
```

接收器的主循环就像常规的 UDP 服务端一样。

### 示例输出

此示例显示在两个不同主机上运行的组播接收器。`A`地址`192.168.1.13`和`B`地址 `192.168.1.14`。

```python
[A]$ python3 socket_multicast_receiver.py

waiting to receive message
received 19 bytes from ('192.168.1.14', 62650)
b'very important data'
sending acknowledgement to ('192.168.1.14', 62650)

waiting to receive message

[B]$ python3 source/socket/socket_multicast_receiver.py

waiting to receive message
received 19 bytes from ('192.168.1.14', 64288)
b'very important data'
sending acknowledgement to ('192.168.1.14', 64288)

waiting to receive message
```

发件人正在主机上运行`B`。

```python
[B]$ python3 socket_multicast_sender.py
sending b'very important data'
waiting to receive
received b'ack' from ('192.168.1.14', 10000)
waiting to receive
received b'ack' from ('192.168.1.13', 10000)
waiting to receive
timed out, no more responses
closing socket
```

消息被发送一次，并且接收到两个传出消息的确认，分别来自主机`A`和`B`。

## 发送二进制数据

套接字传输字节流。这些字节可以包含编码为字节的文本消息，如前面示例中所示，或者它们也可以是由 struct 打包到缓冲区中的二进制数据。

此客户端程序将整数，两个字符的字符串和浮点值，编码为可传递到套接字以进行传输的字节序列。

```python
# socket_binary_client.py 
import binascii
import socket
import struct
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
sock.connect(server_address)

values = (1, b'ab', 2.7)
packer = struct.Struct('I 2s f')
packed_data = packer.pack(*values)

print('values =', values)

try:
    # Send data
    print('sending {!r}'.format(binascii.hexlify(packed_data)))
    sock.sendall(packed_data)
finally:
    print('closing socket')
    sock.close()
```

在两个系统之间发送多字节二进制数据时，重要的是要确保连接的两端都知道字节的顺序，以及如何将它们解压回原来的结构。服务端程序使用相同的 `Struct`说明符来解压缩接收的字节，以便按正确的顺序还原它们。

```python
# socket_binary_server.py 
import binascii
import socket
import struct
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
sock.bind(server_address)
sock.listen(1)

unpacker = struct.Struct('I 2s f')

while True:
    print('\nwaiting for a connection')
    connection, client_address = sock.accept()
    try:
        data = connection.recv(unpacker.size)
        print('received {!r}'.format(binascii.hexlify(data)))

        unpacked_data = unpacker.unpack(data)
        print('unpacked:', unpacked_data)

    finally:
        connection.close()
```

运行客户端会产生：

```python
$ python3 source/socket/socket_binary_client.py
values = (1, b'ab', 2.7)
sending b'0100000061620000cdcc2c40'
closing socket
```

服务端显示它收到的值：

```python
$ python3 socket_binary_server.py

waiting for a connection
received b'0100000061620000cdcc2c40'
unpacked: (1, b'ab', 2.700000047683716)

waiting for a connection
```

浮点值在打包和解包时会丢失一些精度，否则数据会按预期传输。要记住的一件事是，取决于整数的值，将其转换为文本然后传输而不使用 `struct` 可能更高效。整数`1`在表示为字符串时使用一个字节，但在打包到结构中时使用四个字节。

## 非阻塞通信和超时

默认情况下，配置 socket 来发送和接收数据，当套接字准备就绪时会阻塞程序执行。调用`send()`等待缓冲区空间可用于传出数据，调用`recv()`等待其他程序发送可读取的数据。这种形式的 I/O 操作很容易理解，但如果两个程序最终都在等待另一个发送或接收数据，则可能导致程序低效，甚至死锁。

有几种方法可以解决这种情况。一种是使用单独的线程分别与每个套接字进行通信。但是，这可能会引入其他复杂的问题，即线程之间的通信。另一个选择是将套接字更改为不阻塞的，如果尚未准备好处理操作，则立即返回。使用`setblocking()`方法更改套接字的阻止标志。默认值为`1`，表示阻止。`0`表示不阻塞。如果套接字已关闭阻塞并且尚未准备好，则会引发 `socket.error` 错误。

另一个解决方案是为套接字操作设置超时时间，调用 `settimeout()` 函数，参数是一个浮点值，表示在确定套接字未准备好之前要阻塞的秒数。超时到期时，引发 `timeout` 异常。

相关文档：

https://pymotw.com/3/socket/index.html