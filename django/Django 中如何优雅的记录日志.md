# Django 中如何优雅的记录日志

日志是个好东西，但却并不是所有人都愿意记，直到出了问题才追悔莫及，长叹一声，当初要是记日志就好了。

但记日志却是个技术活，不能什么都不记，但也不能什么都记。如果记了很多没用的信息，反而给查日志排错的过程增加很多困难。

所以，日志要记录在程序的关键节点，而且内容要简洁，传递信息要准确。要清楚的反应出程序当时的状态，时间，错误信息等。

只有做到这样，我们才能在第一时间找到问题，并且解决问题。

## logging 结构

在 Django 中使用 Python 的标准库 logging 模块来记录日志，关于 logging 的配置，我这里不做过多介绍，只写其中最重要的四个部分：`Loggers`、`Handlers`、`Filters` 和 `Formatters`。

### Loggers

`Logger` 即**记录器**，是日志系统的入口。它有三个重要的工作：

- 向应用程序（也就是你的项目）公开几种方法，以便运行时记录消息
- 根据传递给 `Logger` 的消息的严重性，确定消息是否需要处理
- 将需要处理的消息传递给所有感兴趣的处理器 `Handler`

每一条写入 `Logger` 的消息都是一条日志记录，每一条日志记录都包含级别，代表对应消息的严重程度。常用的级别如下：

- `DEBUG`：排查故障时使用的低级别系统信息，通常开发时使用
- `INFO`：一般的系统信息，并不算问题
- `WARNING`：描述系统发生小问题的信息，但通常不影响功能
- `ERROR`：描述系统发生大问题的信息，可能会导致功能不正常
- `CRITICAL`：描述系统发生严重问题的信息，应用程序有崩溃的风险

当 `Logger` 处理一条消息时，会将自己的日志级别和这条消息配置的级别做对比。如果消息的级别匹配或者高于 `Logger` 的日志级别，它就会被进一步处理，否则这条消息就会被忽略掉。

当 `Logger` 确定了一条消息需要处理之后，会把它传给 `Handler`。

### Handlers

`Handler` 即**处理器**，它的主要功能是决定如何处理 `Logger` 中的每一条消息，比如把消息输出到屏幕、文件或者 Email 中。

和 `Logger` 一样，`Handler` 也有级别的概念。如果一条日志记录的级别不匹配或者低于 `Handler` 的日志级别，则会被 `Handler` 忽略。

一个 `Logger` 可以有多个 `Handler`，每一个 `Handler` 可以有不同的日志级别。这样就可以根据消息的重要性不同，来提供不同类型的输出。例如，你可以添加一个 `Handler` 把 `ERROR` 和 `CRITICAL` 消息发到你的 Email，再添加另一个 `Handler` 把所有的消息（包括 `ERROR` 和 `CRITICAL` 消息）保存到文件里。

### Filters

`Filter` 即**过滤器**。在日志记录从 `Logger` 传到 `Handler` 的过程中，使用 `Filter` 来做额外的控制。例如，只允许某个特定来源的 `ERROR` 消息输出。

`Filter` 还被用来在日志输出之前对日志记录做修改。例如，当满足一定条件时，把日志级别从 `ERROR` 降到 `WARNING` 。

`Filter` 在 `Logger` 和 `Handler` 中都可以添加，多个 `Filter` 可以链接起来使用，来做多重过滤操作。

### Formaters

`Formatter` 即**格式化器**，主要功能是确定最终输出的形式和内容。

## 实现方式

说了这么多理论，是时候来看看具体怎么实现了。

其实最简单的方式就是直接在文件开头 `import`，然后程序中调用，像下面这样：

```python
# import the logging library
import logging

# Get an instance of a logger
logging.basicConfig(
    format='%(asctime)s - %(pathname)s[%(lineno)d] - %(levelname)s: %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

def my_view(request, arg1, arg):
    ...
    if bad_mojo:
        # Log an error message
        logger.error('Something went wrong!')
```

但这种方式并不好，如果在每个文件开头都这样写一遍，第一是麻烦，第二是如果哪天要改变输出日志格式，那每个文件都要改一遍，还不累死。

很显然，如果能封装成一个类，用的时候调用这个类，修改的时候也只需要修改这一个地方，是不是就解决这个问题了呢？

### 自定义类

下面来看看具体这个类怎么封装：

```python
class CommonLog(object):
    """
    日志记录
    """
    def __init__(self, logger, logname='web-log'):
        self.logname = os.path.join(settings.LOGS_DIR, '%s' % logname)
        self.logger = logger
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s', '%Y-%m-%d %H:%M:%S')

    def __console(self, level, message):
        # 创建一个FileHandler，用于写到本地
        fh = logging.handlers.TimedRotatingFileHandler(self.logname, when='MIDNIGHT', interval=1, encoding='utf-8')
        # fh = logging.FileHandler(self.logname, 'a', encoding='utf-8')
        fh.suffix = '%Y-%m-%d.log'
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)

        # 创建一个StreamHandler,用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)

        if level == 'info':
            self.logger.info(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)

        # 这两行代码是为了避免日志输出重复问题
        self.logger.removeHandler(ch)
        self.logger.removeHandler(fh)
        # 关闭打开的文件
        fh.close()

    def debug(self, message):
        self.__console('debug', message)

    def info(self, message):
        self.__console('info', message)

    def warning(self, message):
        self.__console('warning', message)

    def error(self, message):
        self.__console('error', message)
```

这是我在项目中还在用的一段代码，生成的文件按天进行切分。

当时写这段代码，有个问题折腾了我很久，就是显示代码报错行数的问题。当 `formatter` 配置 `%(lineno)d` 时，每次并不是显示实际的报错行，而是显示日志类中的代码行，但这样显示就失去意义了，所以也就没有配置，用了 `%(name)s` 来展示实际的调用文件。

其实，如果只是为了排错方便，记录一些日志，这个类基本可以满足要求。但如果要记录访问系统的所有请求日志，那就无能为力了，因为不可能手动在每个接口代码加日志，也没必要。

这个时候，很自然就能想到 Django 中间件了。

### Django 中间件

中间件日志代码一共分三个部分，分别是：`Filters` 代码，`middleware` 代码，`settings` 配置，如下：

```python
local = threading.local()


class RequestLogFilter(logging.Filter):
    """
    日志过滤器
    """

    def filter(self, record):
        record.sip = getattr(local, 'sip', 'none')
        record.dip = getattr(local, 'dip', 'none')
        record.body = getattr(local, 'body', 'none')
        record.path = getattr(local, 'path', 'none')
        record.method = getattr(local, 'method', 'none')
        record.username = getattr(local, 'username', 'none')
        record.status_code = getattr(local, 'status_code', 'none')
        record.reason_phrase = getattr(local, 'reason_phrase', 'none')

        return True
      

class RequestLogMiddleware(MiddlewareMixin):
    """
    将request的信息记录在当前的请求线程上。
    """

    def __init__(self, get_response=None):
        self.get_response = get_response
        self.apiLogger = logging.getLogger('web.log')

    def __call__(self, request):

        try:
            body = json.loads(request.body)
        except Exception:
            body = dict()

        if request.method == 'GET':
            body.update(dict(request.GET))
        else:
            body.update(dict(request.POST))

        local.body = body
        local.path = request.path
        local.method = request.method
        local.username = request.user
        local.sip = request.META.get('REMOTE_ADDR', '')
        local.dip = socket.gethostbyname(socket.gethostname())

        response = self.get_response(request)
        local.status_code = response.status_code
        local.reason_phrase = response.reason_phrase
        self.apiLogger.info('system-auto')

        return response
```

`settings.py` 文件配置：

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
  	# 自定义中间件添加在最后
    'lib.log_middleware.RequestLogMiddleware'
]

LOGGING = {
    # 版本
    'version': 1,
    # 是否禁止默认配置的记录器
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '{"time": "%(asctime)s", "level": "%(levelname)s", "method": "%(method)s", "username": "%(username)s", "sip": "%(sip)s", "dip": "%(dip)s", "path": "%(path)s", "status_code": "%(status_code)s", "reason_phrase": "%(reason_phrase)s", "func": "%(module)s.%(funcName)s:%(lineno)d",  "message": "%(message)s"}',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    # 过滤器
    'filters': {
        'request_info': {'()': 'lib.log_middleware.RequestLogFilter'},
    },
    'handlers': {
        # 标准输出
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        # 自定义 handlers，输出到文件
        'restful_api': {
            'level': 'DEBUG',
            # 时间滚动切分
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, 'web-log.log'),
            'formatter': 'standard',
            # 调用过滤器
            'filters': ['request_info'],
            # 每天凌晨切分
            'when': 'MIDNIGHT',
            # 保存 30 天
            'backupCount': 30,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False
        },
        'web.log': {
            'handlers': ['restful_api'],
            'level': 'INFO',
            # 此记录器处理过的消息就不再让 django 记录器再次处理了
            'propagate': False
        },
    }
}
```

通过这种方式，只要过 Django 的请求就都会有日志，不管是 web 还是 Django admin。具体记录哪些字段可以根据项目需要进行获取和配置。

有一点需要注意的是，通过 `request.user` 来获取用户名只适用于 `session` 的认证方式，因为 `session` 认证之后会将用户名赋值给 `request.user`，所以才能取得到。

假设用 `jwt` 方式认证，`request.user` 是没有值的。想要获取用户名可以有两种方式：一是在日志中间件中解析 `jwt cookie` 获取用户名，但这种方式并不好，更好的方法是重写 `jwt` 认证，将用户名赋值给 `request.user`，这样就可以在其他任何地方调用 `request.user` 来取值了。

以上就是在 Django 中记录日志的全部内容，希望大家都能好好记日志，因为一定会用得上。



**参考文档：**

https://docs.djangoproject.com/en/2.1/topics/logging/

https://www.dusaiphoto.com/article/detail/68/

https://juejin.im/post/5c34306cf265da616624a48c

https://www.xiaomastack.com/2019/01/11/record-api-log/

**往期精彩：**

