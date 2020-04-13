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
