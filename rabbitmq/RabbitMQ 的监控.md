# RabbitMQ 的监控

上两篇文章介绍了：

- [Mac 环境下 RabbitMQ 的安装](<https://github.com/yongxinz/tech-blog/blob/master/rabbitmq/Mac%20%E7%8E%AF%E5%A2%83%E4%B8%8B%20RabbitMQ%20%E7%9A%84%E5%AE%89%E8%A3%85.md>)
- [RabbitMQ 的六种工作模式（附 Python 代码）](<https://github.com/yongxinz/tech-blog/blob/master/rabbitmq/RabbitMQ%20%E7%9A%84%E5%85%AD%E7%A7%8D%E5%B7%A5%E4%BD%9C%E6%A8%A1%E5%BC%8F%EF%BC%8C%E7%9C%8B%E8%BF%99%E4%B8%80%E7%AF%87%E5%B0%B1%E5%A4%9F%E4%BA%86%EF%BC%88%E9%99%84%20Python%20%E4%BB%A3%E7%A0%81%EF%BC%89.md>)

接下来说说监控的相关内容。

监控还是非常重要的，特别是在生产环境。磁盘满了，队列积压严重，如果我们还不知道，老板肯定会怀疑，莫不是这家伙要跑路？

而且我现在就遇到了这样的情况，主要是队列积压的问题。由于量不是很大，所以磁盘空间倒不是很担心，但有时程序执行会报错，导致队列一直消费不下去，这就很让人尴尬了。

查了一些资料，总结了一下。想要了解 RabbitMQ 的运行状态，主要有三种途径：Management UI，rabbitmqctl 命令和 REST API。

## Management UI

![management-ui.png](http://ww1.sinaimg.cn/large/0061a0TTly1gdqzj5nxxqj31400lydin.jpg)

RabbitMQ 给我们提供了丰富的 Web 管理功能，通过页面，我们能看到 RabbitMQ 的整体运行状况，交换机和队列的状态等，还可以进行人员管理和权限配置，相当全面。

但如果想通过页面来监控，那出不出问题只能靠缘分。看到出问题了，是运气好，看不到出问题，那是必然。

这也是我当前的现状，所以为了避免出现大问题，得赶紧改变一下。

备注：通过 http://127.0.0.1:15672 来访问 Web 页面，默认情况下用户名和密码都是 guest，但生产环境下都应该改掉的。

## rabbitmqctl 命令

与前端页面对应的就是后端的命令行命令了，同样非常丰富。平时自己测试，或者临时查看一些状态时，也能用得上。但就我个人使用感觉来说，用的并不是很多。

我总结一些还算常用的，列在下面，大家各取所需：

```python
# 启动服务
rabbitmq-server

# 停止服务
rabbitmqctl stop

# vhost 增删查
rabbitmqctl add_vhost
rabbitmqctl delete_vhost
rabbitmqctl list_vhosts

# 查询交换机
rabbitmqctl list_exchanges

# 查询队列
rabbitmqctl list_queues

# 查看消费者信息
rabbitmqctl list_consumers

# user 增删查
rabbitmqctl add_user
rabbitmqctl delete_user
rabbitmqctl list_users
```

## REST API

终于来到重点了，对于程序员来说，看到有现成的 API 可以调用，那真是太幸福了。

自动化监控和一些需要批量的操作，通过调用 API 来实现是最好的方式。比如有一些需要初始化的用户和权限，就可以通过脚本来一键完成，而不是通过页面逐个添加，简单又快捷。

下面是一些常用的 API：

```python
# 概括信息
curl -i -u guest:guest http://localhost:15672/api/overview

# vhost 列表
curl -i -u guest:guest http://localhost:15672/api/vhosts

# channel 列表
curl -i -u guest:guest http://localhost:15672/api/channels
      
# 节点信息
curl -i -u guest:guest http://localhost:15672/api/nodes
      
# 交换机信息
curl -i -u guest:guest http://localhost:15672/api/exchanges
      
# 队列信息
curl -i -u guest:guest http://localhost:15672/api/queues
```

就我现在遇到的情况来说，`overview` 和 `queues` 这两个 API 就可以满足我的需求，大家也可以根据自己项目的实际情况来选择。

API 返回内容是 json，而且字段还是挺多的，刚开始看会感觉一脸懵，具体含义对照官网的解释和实际情况来慢慢琢磨，弄懂也不是很困难。

下面代码包含了 API 请求以及返回结果的解析，可以在测试环境下执行，稍加更改就可以应用到生产环境。

```python
import json
import logging
import optparse

import requests

logging.basicConfig(
    format='%(asctime)s - %(pathname)s[%(lineno)d] - %(levelname)s: %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


class RabbitMQMoniter(object):
    """
    RabbitMQ Management API
    """
    def __init__(self, host='', port=15672, username='guest', password='guest'):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def call_api(self, path):
        logger.info('call rabbit api to get data on ' + path)

        headers = {'content-type': 'application/json'}
        url = '{0}://{1}:{2}/api/{3}'.format('http', self.host, self.port, path)
        res = requests.get(url, headers=headers, auth=(self.username, self.password))

        return res.json()

    def list_queues(self):
        """
        curl -i -u guest:guest http://localhost:15672/api/queues  
        return: list
        """
        queues = []
        for queue in self.call_api('queues'):
            element = {
                'vhost': queue['vhost'],
                'queue': queue['name']
            }
            queues.append(element)
            logger.info('get queue ' + queue['vhost'] + '/' + queue['name'])
        return queues

    def list_nodes(self):
        """
        curl -i -u guest:guest http://localhost:15672/api/nodes
        return: list
        """
        nodes = []
        for node in self.call_api('nodes'):
            name = node['name'].split('@')[1]
            element = {
                'node': name,
                'node_type': node['type']
            }
            nodes.append(element)
            logger.info('get nodes ' + name + '/' + node['type'])
        return nodes

    def check_queue(self):
        """
        check queue
        """
        for queue in self.call_api('queues'):
            self._get_queue_data(queue)
        return True

    def _get_queue_data(self, queue):
        """
        get queue data
        """
        for item in ['memory', 'messages', 'messages_ready', 'messages_unacknowledged', 'consumers']:
            key = 'rabbitmq.queues[{0},queue_{1},{2}]'.format(queue['vhost'], item, queue['name'])
            value = queue.get(item, 0)
            logger.info('queue data: - %s %s' % (key, value))

        for item in ['deliver_get', 'publish']:
            key = 'rabbitmq.queues[{0},queue_message_stats_{1},{2}]'.format(queue['vhost'], item, queue['name'])
            value = queue.get('message_stats', {}).get(item, 0)
            logger.info('queue data: - %s %s' % (key, value))

    def check_aliveness(self):
        """
        check alive
        """
        return self.call_api('aliveness-test/%2f')['status']

    def check_overview(self, item):
        """
        check overview
        """
        if item in ['channels', 'connections', 'consumers', 'exchanges', 'queues']:
            return self.call_api('overview').get('object_totals').get(item, 0)
        elif item in ['messages', 'messages_ready', 'messages_unacknowledged']:
            return self.call_api('overview').get('queue_totals').get(item, 0)
        elif item == 'message_stats_deliver_get':
            return self.call_api('overview').get('message_stats', {}).get('deliver_get', 0)
        elif item == 'message_stats_publish':
            return self.call_api('overview').get('message_stats', {}).get('publish', 0)
        elif item == 'message_stats_ack':
            return self.call_api('overview').get('message_stats', {}).get('ack', 0)
        elif item == 'message_stats_redeliver':
            return self.call_api('overview').get('message_stats', {}).get('redeliver', 0)
        elif item == 'rabbitmq_version':
            return self.call_api('overview').get('rabbitmq_version', 'None')

    def check_server(self, item, node_name):
        """
        check server
        """
        node_name = node_name.split('.')[0]
        for nodeData in self.call_api('nodes'):
            if node_name in nodeData['name']:
                return nodeData.get(item, 0)
        return 'Not Found'


def main():
    """
    Command-line
    """
    choices = ['list_queues', 'list_nodes', 'queues', 'check_aliveness', 'overview', 'server']

    parser = optparse.OptionParser()
    parser.add_option('--username', help='RabbitMQ API username', default='guest')
    parser.add_option('--password', help='RabbitMQ API password', default='guest')
    parser.add_option('--host', help='RabbitMQ API host', default='127.0.0.1')
    parser.add_option('--port', help='RabbitMQ API port', type='int', default=15672)
    parser.add_option('--check', type='choice', choices=choices, help='Type of check')
    parser.add_option('--metric', help='Which metric to evaluate', default='')
    parser.add_option('--node', help='Which node to check (valid for --check=server)')
    (options, args) = parser.parse_args()

    if not options.check:
        parser.error('At least one check should be specified')

    logger.info('start running ...')

    api = RabbitMQMoniter(username=options.username, password=options.password, host=options.host, port=options.port)

    if options.check == 'list_queues':
        logger.info(json.dumps({'data': api.list_queues()}, indent=4, separators=(',', ':')))
    elif options.check == 'list_nodes':
        logger.info(json.dumps({'data': api.list_nodes()}, indent=4, separators=(',', ':')))
    elif options.check == 'queues':
        logger.info(api.check_queue())
    elif options.check == 'check_aliveness':
        logger.info(api.check_aliveness())
    elif options.check == 'overview':
        if not options.metric:
            parser.error('Missing required parameter: "metric"')
        else:
            if options.node:
                logger.info(api.check_overview(options.metric))
            else:
                logger.info(api.check_overview(options.metric))
    elif options.check == 'server':
        if not options.metric:
            parser.error('Missing required parameter: "metric"')
        else:
            if options.node:
                logger.info(api.check_server(options.metric, options.node))
            else:
                logger.info(api.check_server(options.metric, api.host))


if __name__ == '__main__':
    main()
```

调用及返回：

```python
python3 rabbitmq_status.py --check list_queues

# 2020-04-12 14:33:15,298 - rabbitmq_status.py[142] - INFO: start running ...
# 2020-04-12 14:33:15,298 - rabbitmq_status.py[26] - INFO: call rabbit api to get data on queues
# 2020-04-12 14:33:15,312 - rabbitmq_status.py[46] - INFO: get queue //task_queue
# 2020-04-12 14:33:15,312 - rabbitmq_status.py[147] - INFO: {
#     "data":[
#         {
#             "vhost":"/",
#             "queue":"task_queue"
#         }
#     ]
# }
```

通过对返回结果进行解析，就可以判断 RabbitMQ 的整体运行状态，如果发生超阈值的情况，可以发送告警或邮件，来达到监控的效果。

针对队列积压情况的监控判断，有两种方式：一是设置队列积压长度阈值，如果超过阈值即告警；二是保存最近五次的积压长度，如果积压逐渐增长并超阈值，即告警。

第二种方式更好，判断更加精准，误告可能性小，但实现起来也更复杂。

这里只是提一个思路，等后续再把实践结果和代码分享出来。或者大家有哪些更好的方法吗？欢迎留言交流。



**源码地址：** 

https://github.com/yongxinz/tech-blog/tree/master/rabbitmq/src

**参考文档：** 

https://www.rabbitmq.com/monitoring.html

https://blog.51cto.com/john88wang/1745824

