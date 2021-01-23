# 避坑指南，Elasticsearch 分页查询的两个问题，你一定要知道

Elasticsearch 分页查询有个特点，如果你写一个这样的查询语句：

```python
{
    "from" : 10, "size" : 10,
    "query" : {}
}
```

Elasticsearch 会查询出前 20 条数据，然后截断前 10 条，只返回 10-20 的数据。

这样做带来的副作用很明显，数据量大的话，越到后面查询越慢。

所以针对大数据量的查询，要使用 scroll。这种方式相当于建立了一个游标，标记当前的读取位置，保证下一次查询快速取出数据。

但这两种方式都还有一个小坑需要注意，下面来详细说明。

### from + size 方式

可能会出现的问题：

>Result window is too large, from + size must be less than or equal to: [10000] but was [10010].  See the scroll api for a more efficient way to request large data sets.  This limit can be set by changing the [index.max_result_window] index level setting.

这个报错信息其实已经说的很明确了，通过这种分页方式查询的最大值是 10000，超过 10000 就会报错。

解决办法也很简单，一是针对大数据量查询采用 scroll 方式；二是增加 `index.max_result_window` 值的大小，使其支持查询范围。

推荐使用 scroll 方式。

### scroll 方式

可能会出现的问题：

> Trying to create too many scroll contexts. Must be less than or equal to: [500]. This limit can be set by changing the [search.max_open_scroll_context] setting.

产生这个错误的原因是：

当有大量需要使用 scroll 的请求向 Elasticsearch 请求数据时，系统默认最大 scroll_id 数量是 500，当达到最大值时，导致部分请求没有 scroll_id 可用，产生报错。

特别是在高并发场景下，这种问题可能会更加常见。

解决办法可以增加 `search.max_open_scroll_context` 值的大小。

但这么解决并不好，更好的办法是查询完之后，及时清理 scroll_id。

```python
# python
from elasticsearch import Elasticsearch


client = Elasticsearch(host, http_auth=(username, password), timeout=3600)
es_data = client.search(es_index, query_body, scroll='1m', size=100)
scroll_id = es_data['_scroll_id']
client.clear_scroll(scroll_id=scroll_id)	# 清理方法
```

其实，即使我们不手动清理，等过期之后，游标也会自己释放的，这跟使用时的参数有关。

比如 `scroll='1m'` 代表 1min 后会释放。

但就像我们使用其他资源一样，使用完之后及时释放，养成良好的编码习惯，系统才能更健壮。

**参考文档：**

- https://juejin.cn/post/6844903694241103879

- https://juejin.cn/post/6890891504630366215

**往期精彩：**



