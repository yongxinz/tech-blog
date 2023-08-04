## Elasticsearch 基本概念

Index：Elasticsearch用来存储数据的逻辑区域，它类似于关系型数据库中的database 概念。一个index可以在一个或者多个shard上面，同时一个shard也可能会有多个replicas。

Document：Elasticsearch里面存储的实体数据，类似于关系数据中一个table里面的一行数据。

document由多个field组成，不同的document里面同名的field一定具有相同的类型。document里面field可以重复出现，也就是一个field会有多个值，即multivalued。

Document type：为了查询需要，一个index可能会有多种document，也就是document type. 它类似于关系型数据库中的 table 概念。但需要注意，不同document里面同名的field一定要是相同类型的。

Mapping：它类似于关系型数据库中的 schema 定义概念。存储field的相关映射信息，不同document type会有不同的mapping。

下图是ElasticSearch和关系型数据库的一些术语比较：



Relationnal database | Elasticsearch
---|---
Database| Index
Table | Type
Row | Document
Column | Field
Schema | Mapping
Schema | Mapping
Index | Everything is indexed
SQL | Query DSL
SELECT * FROM table… | GET http://…
UPDATE table SET | PUT http://…


## Python Elasticsearch DSL 使用简介

连接 Es：

```python
import elasticsearch

es = elasticsearch.Elasticsearch([{'host': '127.0.0.1', 'port': 9200}])
```

先看一下搜索，`q` 是指搜索内容，空格对 `q` 查询结果没有影响，`size` 指定个数，`from_` 指定起始位置，`filter_path` 可以指定需要显示的数据，如本例中显示在最后的结果中的只有 `_id` 和 `_type`。

```python
res_3 = es.search(index="bank", q="Holmes", size=1, from_=1)
res_4 = es.search(index="bank", q=" 39225    5686 ", size=1000, filter_path=['hits.hits._id', 'hits.hits._type'])
```

查询指定索引的所有数据：

其中，index 指定索引，字符串表示一个索引；列表表示多个索引，如 `index=["bank", "banner", "country"]`；正则形式表示符合条件的多个索引，如 `index=["apple*"]`，表示以 `apple` 开头的全部索引。

`search` 中同样可以指定具体 `doc-type`。


```python
from elasticsearch_dsl import Search

s = Search(using=es, index="index-test").execute()
print s.to_dict()
```

根据某个字段查询，可以多个查询条件叠加：

```python
s = Search(using=es, index="index-test").query("match", sip="192.168.1.1")
s = s.query("match", dip="192.168.1.2")
s = s.excute()
```

多字段查询：

```python
from elasticsearch_dsl.query import MultiMatch, Match

multi_match = MultiMatch(query='hello', fields=['title', 'content'])
s = Search(using=es, index="index-test").query(multi_match)
s = s.execute()

print s.to_dict()
```

还可以用 `Q()` 对象进行多字段查询，`fields` 是一个列表，`query` 为所要查询的值。


```python
from elasticsearch_dsl import Q

q = Q("multi_match", query="hello", fields=['title', 'content'])
s = s.query(q).execute()

print s.to_dict()
```

`Q()` 第一个参数是查询方法，还可以是 `bool`。

```python

q = Q('bool', must=[Q('match', title='hello'), Q('match', content='world')])
s = s.query(q).execute()

print s.to_dict()
```

通过 `Q()` 进行组合查询，相当于上面查询的另一种写法。

```python
q = Q("match", title='python') | Q("match", title='django')
s = s.query(q).execute()
print(s.to_dict())
# {"bool": {"should": [...]}}

q = Q("match", title='python') & Q("match", title='django')
s = s.query(q).execute()
print(s.to_dict())
# {"bool": {"must": [...]}}

q = ~Q("match", title="python")
s = s.query(q).execute()
print(s.to_dict())
# {"bool": {"must_not": [...]}}
```

过滤，在此为范围过滤，`range` 是方法，`timestamp` 是所要查询的 `field` 名字，`gte` 为大于等于，`lt` 为小于，根据需要设定即可。

关于 `term` 和 `match` 的区别，`term` 是精确匹配，`match` 会模糊化，会进行分词，返回匹配度分数，（`term` 如果查询小写字母的字符串，有大写会返回空即没有命中，`match` 则是不区分大小写都可以进行查询，返回结果也一样）

```python
# 范围查询
s = s.filter("range", timestamp={"gte": 0, "lt": time.time()}).query("match", country="in")
# 普通过滤
res_3 = s.filter("terms", balance_num=["39225", "5686"]).execute()
```

其他写法：

```python
s = Search()
s = s.filter('terms', tags=['search', 'python'])
print(s.to_dict())
# {'query': {'bool': {'filter': [{'terms': {'tags': ['search', 'python']}}]}}}

s = s.query('bool', filter=[Q('terms', tags=['search', 'python'])])
print(s.to_dict())
# {'query': {'bool': {'filter': [{'terms': {'tags': ['search', 'python']}}]}}}
s = s.exclude('terms', tags=['search', 'python'])
# 或者
s = s.query('bool', filter=[~Q('terms', tags=['search', 'python'])])
print(s.to_dict())
# {'query': {'bool': {'filter': [{'bool': {'must_not': [{'terms': {'tags': ['search', 'python']}}]}}]}}}
```

聚合可以放在查询，过滤等操作的后面叠加，需要加 `aggs`。

`bucket` 即为分组，其中第一个参数是分组的名字，自己指定即可，第二个参数是方法，第三个是指定的 `field`。

`metric` 也是同样，`metric` 的方法有 `sum`、`avg`、`max`、`min` 等，但是需要指出的是，有两个方法可以一次性返回这些值，`stats` 和 `extended_stats`，后者还可以返回方差等值。

```python
# 实例1
s.aggs.bucket("per_country", "terms", field="timestamp").metric("sum_click", "stats", field="click").metric("sum_request", "stats", field="request")

# 实例2
s.aggs.bucket("per_age", "terms", field="click.keyword").metric("sum_click", "stats", field="click")

# 实例3
s.aggs.metric("sum_age", "extended_stats", field="impression")

# 实例4
s.aggs.bucket("per_age", "terms", field="country.keyword")

# 实例5，此聚合是根据区间进行聚合
a = A("range", field="account_number", ranges=[{"to": 10}, {"from": 11, "to": 21}])

res = s.execute()
```
最后依然要执行 `execute()`，此处需要注意，`s.aggs` 操作不能用变量接收（如 `res=s.aggs`，这个操作是错误的），聚合的结果会保存到 `res` 中显示。


排序
```python
s = Search().sort(
    'category',
    '-title',
    {"lines" : {"order" : "asc", "mode" : "avg"}}
)
```

分页
```python
s = s[10:20]
# {"from": 10, "size": 10}
```

一些扩展方法，感兴趣的同学可以看看：

```python
s = Search()

# 设置扩展属性使用`.extra()`方法
s = s.extra(explain=True)

# 设置参数使用`.params()`
s = s.params(search_type="count")

# 如要要限制返回字段，可以使用`source()`方法
# only return the selected fields
s = s.source(['title', 'body'])
# don't return any fields, just the metadata
s = s.source(False)
# explicitly include/exclude fields
s = s.source(include=["title"], exclude=["user.*"])
# reset the field selection
s = s.source(None)

# 使用dict序列化一个查询
s = Search.from_dict({"query": {"match": {"title": "python"}}})

# 修改已经存在的查询
s.update_from_dict({"query": {"match": {"title": "python"}}, "size": 42})
```

参考文档：

http://fingerchou.com/2017/08/12/elasticsearch-dsl-with-python-usage-1/

http://fingerchou.com/2017/08/13/elasticsearch-dsl-with-python-usage-2/

https://blog.csdn.net/JunFeng666/article/details/78251788