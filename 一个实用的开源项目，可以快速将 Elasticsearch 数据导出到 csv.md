# 一个实用的开源项目，可以快速将 Elasticsearch 数据导出到 csv

在实际业务中，数据导出应该算是一个强需求了，很多场景都用得到。

如果是 MySQL 的话，则无需多言，支持导出的工具一大堆，根据自己需求选择即可。

那有没有对 Elasticsearch 导出支持比较好的工具呢？

虽然没有 MySQL 那么多，但肯定是有的。如果部署了 Kibana，那一定是首选，不止导出功能强大，还有一整套可视化功能，很实用。

没有 Kibana 的话也别慌，今天就给大家推荐一款命令行导出工具：**es2csv**。

源码地址：https://github.com/taraslayshchuk/es2csv

该项目使用 Python 编写，既支持 Lucene 原生语法查询，也支持 DSL 语法查询。还可以在多个索引中同时检索，并且只获取自己关注的字段，非常高效。

用法介绍：

```python
$ es2csv [-h] -q QUERY [-u URL] [-a AUTH] [-i INDEX [INDEX ...]]
         [-D DOC_TYPE [DOC_TYPE ...]] [-t TAGS [TAGS ...]] -o FILE
         [-f FIELDS [FIELDS ...]] [-S FIELDS [FIELDS ...]] [-d DELIMITER]
         [-m INTEGER] [-s INTEGER] [-k] [-r] [-e] [--verify-certs]
         [--ca-certs CA_CERTS] [--client-cert CLIENT_CERT]
         [--client-key CLIENT_KEY] [-v] [--debug]

Arguments:
 -q, --query QUERY                        Query string in Lucene syntax.               [required]
 -o, --output-file FILE                   CSV file location.                           [required]
 -u, --url URL                            Elasticsearch host URL. Default is http://localhost:9200.
 -a, --auth                               Elasticsearch basic authentication in the form of username:password.
 -i, --index-prefixes INDEX [INDEX ...]   Index name prefix(es). Default is ['logstash-*'].
 -D, --doc-types DOC_TYPE [DOC_TYPE ...]  Document type(s).
 -t, --tags TAGS [TAGS ...]               Query tags.
 -f, --fields FIELDS [FIELDS ...]         List of selected fields in output. Default is ['_all'].
 -S, --sort FIELDS [FIELDS ...]           List of <field>:<direction> pairs to sort on. Default is [].
 -d, --delimiter DELIMITER                Delimiter to use in CSV file. Default is ",".
 -m, --max INTEGER                        Maximum number of results to return. Default is 0.
 -s, --scroll-size INTEGER                Scroll size for each batch of results. Default is 100.
 -k, --kibana-nested                      Format nested fields in Kibana style.
 -r, --raw-query                          Switch query format in the Query DSL.
 -e, --meta-fields                        Add meta-fields in output.
 --verify-certs                           Verify SSL certificates. Default is False.
 --ca-certs CA_CERTS                      Location of CA bundle.
 --client-cert CLIENT_CERT                Location of Client Auth cert.
 --client-key CLIENT_KEY                  Location of Client Cert Key.
 -v, --version                            Show version and exit.
 --debug                                  Debug mode on.
 -h, --help                               show this help message and exit
```

看参数就知道，功能覆盖还是相当全面的，而且作者也给了很多使用例子，相当贴心。

https://github.com/taraslayshchuk/es2csv/blob/master/docs/EXAMPLES.rst

其实，我还有一个需求，就是除了命令行导出外，希望能有一个公共方法，可以在我自己的程序中调用，然后导出文件。

所以，在原项目基础上，新增了一个程序 **es2csv_lib.py**。这样，如果在开发过程中，如果有从 Elasticsearch 导出的需求，直接调用公共方法即可。

此程序调用参数和命令行方式基本一致：

```python
class Es2csv:

    def __init__(self, opts):
        self.opts = opts
        self.url = self.opts.get('url', '')
        self.auth = self.opts.get('auth', '')
        self.index_prefixes = self.opts.get('index_prefixes', [])
        self.sort = self.opts.get('sort', [])
        self.fields = self.opts.get('fields', [])
        self.query = self.opts.get('query', {})
        self.tags = self.opts.get('tags', [])
        self.output_file = self.opts.get('output_file', 'export.csv')
        self.raw_query = self.opts.get('raw_query', True)
        self.delimiter = self.opts.get('delimiter', ',')
        self.max_results = self.opts.get('max_results', 0)
        self.scroll_size = self.opts.get('scroll_size', 100)
        self.meta_fields = self.opts.get('meta_fields', [])
        self.debug_mode = self.opts.get('debug_mode', False)

        self.num_results = 0
        self.scroll_ids = []
        self.scroll_time = '30m'

        self.csv_headers = list(META_FIELDS) if self.opts['meta_fields'] else []
        self.tmp_file = '{}.tmp'.format(self.output_file)
```

使用方法：

```python
from es2csv_lib import Es2csv


es = Es2csv(*args)
es.export_csv()
```

源码地址：https://github.com/yongxinz/es2csv

还有一点需要说明，源项目作者推荐使用版本是：Python 2.7.x，Elasticsearch 5.x。我新增的代码使用测试版本是：Python 3.6.8，Elasticsearch 5.6.12。

感兴趣的同学可以自己去看源码，或者给我留言都可以。

以上。

**往期精彩：**

