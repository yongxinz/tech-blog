# 每周一个 Python 模块 | contextlib

用于创建和使用上下文管理器的实用程序。

`contextlib` 模块包含用于处理上下文管理器和 `with` 语句的实用程序。

## Context Manager API

上下文管理器负责一个代码块内的资源，从进入块时创建到退出块后清理。例如，文件上下文管理器 API，在完成所有读取或写入后来确保它们已关闭。

```python
with open('/tmp/pymotw.txt', 'wt') as f:
    f.write('contents go here')
# file is automatically closed
```

`with` 语句启用了上下文管理器，API 涉及两种方法：当执行流进入内部代码块时运行 `__enter__()` 方法，它返回要在上下文中使用的对象。当执行流离开 `with` 块时，调用上下文管理器的 `__exit__()` 方法来清理正在使用的任何资源。

```python
class Context:

    def __init__(self):
        print('__init__()')

    def __enter__(self):
        print('__enter__()')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('__exit__()')


with Context():
    print('Doing work in the context')
    
# output
# __init__()
# __enter__()
# Doing work in the context
# __exit__()
```

组合上下文管理器和 `with` 语句是一种更简洁的 `try:finally` 块，即使引发了异常，也总是调用上下文管理器的 `__exit__()` 方法。

`__enter__()` 方法可以返回与 `as` 子句中指定的名称关联的任何对象。在此示例中，`Context` 返回使用打开上下文的对象。

```python
class WithinContext:

    def __init__(self, context):
        print('WithinContext.__init__({})'.format(context))

    def do_something(self):
        print('WithinContext.do_something()')

    def __del__(self):
        print('WithinContext.__del__')


class Context:

    def __init__(self):
        print('Context.__init__()')

    def __enter__(self):
        print('Context.__enter__()')
        return WithinContext(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Context.__exit__()')


with Context() as c:
    c.do_something()
    
# output
# Context.__init__()
# Context.__enter__()
# WithinContext.__init__(<__main__.Context object at 0x101f046d8>)
# WithinContext.do_something()
# Context.__exit__()
# WithinContext.__del__
```

与变量关联的值 `c` 是返回的 `__enter__()` 对象，该对象不一定是 `Context` 在 `with` 语句中创建的实例。

`__exit__()` 方法接收包含 `with` 块中引发的任何异常的详细信息的参数。

```python
class Context:

    def __init__(self, handle_error):
        print('__init__({})'.format(handle_error))
        self.handle_error = handle_error

    def __enter__(self):
        print('__enter__()')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('__exit__()')
        print('  exc_type =', exc_type)
        print('  exc_val  =', exc_val)
        print('  exc_tb   =', exc_tb)
        return self.handle_error


with Context(True):
    raise RuntimeError('error message handled')

print()

with Context(False):
    raise RuntimeError('error message propagated')
    
# output
# __init__(True)
# __enter__()
# __exit__()
#   exc_type = <class 'RuntimeError'>
#   exc_val  = error message handled
#   exc_tb   = <traceback object at 0x101c94948>
# 
# __init__(False)
# __enter__()
# __exit__()
#   exc_type = <class 'RuntimeError'>
#   exc_val  = error message propagated
#   exc_tb   = <traceback object at 0x101c94948>
# Traceback (most recent call last):
#   File "contextlib_api_error.py", line 34, in <module>
#     raise RuntimeError('error message propagated')
# RuntimeError: error message propagated
```

如果上下文管理器可以处理异常，`__exit__()` 则应返回 true 值以指示不需要传播该异常，返回 false 会导致在 `__exit__()` 返回后重新引发异常。

## 作为函数装饰器的上下文管理器

类 `ContextDecorator` 增加了对常规上下文管理器类的支持，使它们可以像用上下文管理器一样用函数装饰器。

```python
import contextlib


class Context(contextlib.ContextDecorator):

    def __init__(self, how_used):
        self.how_used = how_used
        print('__init__({})'.format(how_used))

    def __enter__(self):
        print('__enter__({})'.format(self.how_used))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('__exit__({})'.format(self.how_used))


@Context('as decorator')
def func(message):
    print(message)


print()
with Context('as context manager'):
    print('Doing work in the context')

print()
func('Doing work in the wrapped function')

# output
# __init__(as decorator)
# 
# __init__(as context manager)
# __enter__(as context manager)
# Doing work in the context
# __exit__(as context manager)
# 
# __enter__(as decorator)
# Doing work in the wrapped function
# __exit__(as decorator)
```

使用上下文管理器作为装饰器的一个区别是，`__enter__()` 返回的值在被装饰的函数内部不可用，这与使用 `with` 和 `as` 时不同，传递给装饰函数的参数以通常方式提供。

## 从生成器到上下文管理器

通过用 `__enter__()` 和 `__exit__()` 方法编写类来创建上下文管理器的传统方式并不困难。但是，有时候完全写出所有内容对于一些微不足道的上下文来说是没有必要的。在这些情况下，使用 `contextmanager()` 装饰器将生成器函数转换为上下文管理器。

```python
import contextlib


@contextlib.contextmanager
def make_context():
    print('  entering')
    try:
        yield {}
    except RuntimeError as err:
        print('  ERROR:', err)
    finally:
        print('  exiting')


print('Normal:')
with make_context() as value:
    print('  inside with statement:', value)

print('\nHandled error:')
with make_context() as value:
    raise RuntimeError('showing example of handling an error')

print('\nUnhandled error:')
with make_context() as value:
    raise ValueError('this exception is not handled')
    
# output
# Normal:
#   entering
#   inside with statement: {}
#   exiting
# 
# Handled error:
#   entering
#   ERROR: showing example of handling an error
#   exiting
# 
# Unhandled error:
#   entering
#   exiting
# Traceback (most recent call last):
#   File "contextlib_contextmanager.py", line 33, in <module>
#     raise ValueError('this exception is not handled')
# ValueError: this exception is not handled
```

生成器应该初始化上下文，只产生一次，然后清理上下文。如果有的话，产生的值绑定到 `as` 子句中的变量。`with` 块内的异常在生成器内重新引发，因此可以在那里处理它们。

`contextmanager()` 返回的上下文管理器派生自 `ContextDecorator`，因此它也可以作为函数装饰器使用。

```python
@contextlib.contextmanager
def make_context():
    print('  entering')
    try:
        # Yield control, but not a value, because any value
        # yielded is not available when the context manager
        # is used as a decorator.
        yield
    except RuntimeError as err:
        print('  ERROR:', err)
    finally:
        print('  exiting')


@make_context()
def normal():
    print('  inside with statement')


@make_context()
def throw_error(err):
    raise err


print('Normal:')
normal()

print('\nHandled error:')
throw_error(RuntimeError('showing example of handling an error'))

print('\nUnhandled error:')
throw_error(ValueError('this exception is not handled'))

# output
# Normal:
#   entering
#   inside with statement
#   exiting
# 
# Handled error:
#   entering
#   ERROR: showing example of handling an error
#   exiting
# 
# Unhandled error:
#   entering
#   exiting
# Traceback (most recent call last):
#   File "contextlib_contextmanager_decorator.py", line 43, in
# <module>
#     throw_error(ValueError('this exception is not handled'))
#   File ".../lib/python3.7/contextlib.py", line 74, in inner
#     return func(*args, **kwds)
#   File "contextlib_contextmanager_decorator.py", line 33, in
# throw_error
#     raise err
# ValueError: this exception is not handled
```

如上例所示，当上下文管理器用作装饰器时，生成器产生的值在被装饰的函数内不可用，传递给装饰函数的参数仍然可用，如 `throw_error()` 中所示。

## 关闭打开句柄

`file` 类支持上下文管理器 API，但代表打开句柄的一些其他对象并不支持。标准库文档中给出的 `contextlib` 示例是 `urllib.urlopen()` 返回的对象。还有其他遗留类使用 `close()` 方法，但不支持上下文管理器 API。要确保句柄已关闭，请使用 `closing() ` 为其创建上下文管理器。

```python
import contextlib


class Door:

    def __init__(self):
        print('  __init__()')
        self.status = 'open'

    def close(self):
        print('  close()')
        self.status = 'closed'


print('Normal Example:')
with contextlib.closing(Door()) as door:
    print('  inside with statement: {}'.format(door.status))
print('  outside with statement: {}'.format(door.status))

print('\nError handling example:')
try:
    with contextlib.closing(Door()) as door:
        print('  raising from inside with statement')
        raise RuntimeError('error message')
except Exception as err:
    print('  Had an error:', err)
    
# output
# Normal Example:
#   __init__()
#   inside with statement: open
#   close()
#   outside with statement: closed
# 
# Error handling example:
#   __init__()
#   raising from inside with statement
#   close()
#   Had an error: error message
```

无论 `with` 块中是否有错误，句柄都会关闭。

## 忽略异常

忽略异常的最常见方法是使用语句块 `try:except`，然后在语句 `except` 中只有 `pass`。

```python
import contextlib


class NonFatalError(Exception):
    pass


def non_idempotent_operation():
    raise NonFatalError(
        'The operation failed because of existing state'
    )


try:
    print('trying non-idempotent operation')
    non_idempotent_operation()
    print('succeeded!')
except NonFatalError:
    pass

print('done')

# output
# trying non-idempotent operation
# done
```

在这种情况下，操作失败并忽略错误。

`try:except` 可以被替换为 `contextlib.suppress()`，更明确地抑制类异常在 `with` 块的任何地方发生。

```python
import contextlib


class NonFatalError(Exception):
    pass


def non_idempotent_operation():
    raise NonFatalError(
        'The operation failed because of existing state'
    )


with contextlib.suppress(NonFatalError):
    print('trying non-idempotent operation')
    non_idempotent_operation()
    print('succeeded!')

print('done')

# output
# trying non-idempotent operation
# done
```

在此更新版本中，异常将完全丢弃。

## 重定向输出流

设计不良的库代码可能直接写入 `sys.stdout` 或 `sys.stderr`，不提供参数来配置不同的输出目的地。如果源不能被改变接受新的输出参数时，可以使用 `redirect_stdout()` 和 `redirect_stderr()` 上下文管理器捕获输出。

```python
from contextlib import redirect_stdout, redirect_stderr
import io
import sys


def misbehaving_function(a):
    sys.stdout.write('(stdout) A: {!r}\n'.format(a))
    sys.stderr.write('(stderr) A: {!r}\n'.format(a))


capture = io.StringIO()
with redirect_stdout(capture), redirect_stderr(capture):
    misbehaving_function(5)

print(capture.getvalue())

# output
# (stdout) A: 5
# (stderr) A: 5
```

在此示例中，`misbehaving_function()` 写入 `stdout` 和 `stderr`，但两个上下文管理器将该输出发送到同一 `io.StringIO`，保存它以便稍后使用。

**注意：**`redirect_stdout()` 和 `redirect_stderr()` 通过替换 [`sys`](https://pymotw.com/3/sys/index.html#module-sys) 模块中的对象来修改全局状态，应小心使用。这些函数不是线程安全的，并且可能会干扰期望将标准输出流附加到终端设备的其他操作。

## 动态上下文管理器堆栈

大多数上下文管理器一次操作一个对象，例如单个文件或数据库句柄。在这些情况下，对象是事先已知的，并且使用上下文管理器的代码可以围绕该对象构建。在其他情况下，程序可能需要在上下文中创建未知数量的对象，同时希望在控制流退出上下文时清除所有对象。`ExitStack` 函数就是为了处理这些更动态的情况。

`ExitStack` 实例维护清理回调的堆栈数据结构。回调在上下文中显式填充，并且当控制流退出上下文时，以相反的顺序调用已注册的回调。就像有多个嵌套 `with` 语句，只是它们是动态建立的。

### 堆叠上下文管理器

有几种方法可以填充 `ExitStack`。此示例用于 `enter_context()` 向堆栈添加新的上下文管理器。

```python
import contextlib


@contextlib.contextmanager
def make_context(i):
    print('{} entering'.format(i))
    yield {}
    print('{} exiting'.format(i))


def variable_stack(n, msg):
    with contextlib.ExitStack() as stack:
        for i in range(n):
            stack.enter_context(make_context(i))
        print(msg)


variable_stack(2, 'inside context')

# output
# 0 entering
# 1 entering
# inside context
# 1 exiting
# 0 exiting
```

`enter_context()` 首先调用 `__enter__()` 上下文管理器，然后将 `__exit__()` 方法注册为在栈撤消时调用的回调。

上下文管理器 `ExitStack` 被视为处于一系列嵌套 `with` 语句中。在上下文中的任何位置发生的错误都会通过上下文管理器的正常错误处理进行传播。这些上下文管理器类说明了错误传播的方式。

```python
# contextlib_context_managers.py 
import contextlib


class Tracker:
    "Base class for noisy context managers."

    def __init__(self, i):
        self.i = i

    def msg(self, s):
        print('  {}({}): {}'.format(
            self.__class__.__name__, self.i, s))

    def __enter__(self):
        self.msg('entering')


class HandleError(Tracker):
    "If an exception is received, treat it as handled."

    def __exit__(self, *exc_details):
        received_exc = exc_details[1] is not None
        if received_exc:
            self.msg('handling exception {!r}'.format(
                exc_details[1]))
        self.msg('exiting {}'.format(received_exc))
        # Return Boolean value indicating whether the exception
        # was handled.
        return received_exc


class PassError(Tracker):
    "If an exception is received, propagate it."

    def __exit__(self, *exc_details):
        received_exc = exc_details[1] is not None
        if received_exc:
            self.msg('passing exception {!r}'.format(
                exc_details[1]))
        self.msg('exiting')
        # Return False, indicating any exception was not handled.
        return False


class ErrorOnExit(Tracker):
    "Cause an exception."

    def __exit__(self, *exc_details):
        self.msg('throwing error')
        raise RuntimeError('from {}'.format(self.i))


class ErrorOnEnter(Tracker):
    "Cause an exception."

    def __enter__(self):
        self.msg('throwing error on enter')
        raise RuntimeError('from {}'.format(self.i))

    def __exit__(self, *exc_info):
        self.msg('exiting')
```

这些类的示例基于 `variable_stack()`，它使用上下文管理器来构造  `ExitStack`，逐个构建整体上下文。下面的示例通过不同的上下文管理器来探索错误处理行为。首先，正常情况下没有例外。

```python
print('No errors:')
variable_stack([
    HandleError(1),
    PassError(2),
])
```

然后，在堆栈末尾的上下文管理器中处理异常示例，其中所有打开的上下文在堆栈展开时关闭。

```python
print('\nError at the end of the context stack:')
variable_stack([
    HandleError(1),
    HandleError(2),
    ErrorOnExit(3),
])
```

接下来，处理堆栈中间的上下文管理器中的异常示例，其中在某些上下文已经关闭之前不会发生错误，因此这些上下文不会看到错误。

```
print('\nError in the middle of the context stack:')
variable_stack([
    HandleError(1),
    PassError(2),
    ErrorOnExit(3),
    HandleError(4),
])
```

最后，一个仍未处理的异常并传播到调用代码。

```
try:
    print('\nError ignored:')
    variable_stack([
        PassError(1),
        ErrorOnExit(2),
    ])
except RuntimeError:
    print('error handled outside of context')
```

如果堆栈中的任何上下文管理器收到异常并返回 `True`，则会阻止该异常传播到其他上下文管理器。

```python
$ python3 contextlib_exitstack_enter_context_errors.py

No errors:
  HandleError(1): entering
  PassError(2): entering
  PassError(2): exiting
  HandleError(1): exiting False
  outside of stack, any errors were handled

Error at the end of the context stack:
  HandleError(1): entering
  HandleError(2): entering
  ErrorOnExit(3): entering
  ErrorOnExit(3): throwing error
  HandleError(2): handling exception RuntimeError('from 3')
  HandleError(2): exiting True
  HandleError(1): exiting False
  outside of stack, any errors were handled

Error in the middle of the context stack:
  HandleError(1): entering
  PassError(2): entering
  ErrorOnExit(3): entering
  HandleError(4): entering
  HandleError(4): exiting False
  ErrorOnExit(3): throwing error
  PassError(2): passing exception RuntimeError('from 3')
  PassError(2): exiting
  HandleError(1): handling exception RuntimeError('from 3')
  HandleError(1): exiting True
  outside of stack, any errors were handled

Error ignored:
  PassError(1): entering
  ErrorOnExit(2): entering
  ErrorOnExit(2): throwing error
  PassError(1): passing exception RuntimeError('from 2')
  PassError(1): exiting
error handled outside of context
```

### 任意上下文回调

`ExitStack` 还支持关闭上下文的任意回调，从而可以轻松清理不通过上下文管理器控制的资源。

```python
import contextlib


def callback(*args, **kwds):
    print('closing callback({}, {})'.format(args, kwds))


with contextlib.ExitStack() as stack:
    stack.callback(callback, 'arg1', 'arg2')
    stack.callback(callback, arg3='val3')
    
# output
# closing callback((), {'arg3': 'val3'})
# closing callback(('arg1', 'arg2'), {})
```

与 `__exit__()` 完整上下文管理器的方法一样，回调的调用顺序与它们的注册顺序相反。

无论是否发生错误，都会调用回调，并且不会给出有关是否发生错误的任何信息。它们的返回值被忽略。

```python
import contextlib


def callback(*args, **kwds):
    print('closing callback({}, {})'.format(args, kwds))


try:
    with contextlib.ExitStack() as stack:
        stack.callback(callback, 'arg1', 'arg2')
        stack.callback(callback, arg3='val3')
        raise RuntimeError('thrown error')
except RuntimeError as err:
    print('ERROR: {}'.format(err))
    
# output
# closing callback((), {'arg3': 'val3'})
# closing callback(('arg1', 'arg2'), {})
# ERROR: thrown error
```

因为它们无法访问错误，所以回调无法通过其余的上下文管理器堆栈阻止异常传播。

回调可以方便清楚地定义清理逻辑，而无需创建新的上下文管理器类。为了提高代码可读性，该逻辑可以封装在内联函数中，`callback()` 可以用作装饰器。

```python
import contextlib


with contextlib.ExitStack() as stack:

    @stack.callback
    def inline_cleanup():
        print('inline_cleanup()')
        print('local_resource = {!r}'.format(local_resource))

    local_resource = 'resource created in context'
    print('within the context')
    
# output
# within the context
# inline_cleanup()
# local_resource = 'resource created in context'
```

无法为使用装饰器形式注册的 `callback()` 函数指定参数。但是，如果清理回调是内联定义的，则范围规则允许它访问调用代码中定义的变量。

### 部分堆栈

有时，在构建复杂的上下文时，如果上下文无法完全构建，可以中止操作，但是如果延迟清除所有资源，则能够正确设置所有资源。例如，如果操作需要多个长期网络连接，则最好不要在一个连接失败时启动操作。但是，如果可以打开所有连接，则需要保持打开的时间长于单个上下文管理器的持续时间。可以在此方案中使用 `ExitStack` 的 `pop_all()` 方法。

`pop_all()` 从调用它的堆栈中清除所有上下文管理器和回调，并返回一个预先填充了相同上下文管理器和回调的新堆栈。 在原始堆栈消失之后，可以稍后调用新堆栈的 `close()` 方法来清理资源。

```python
import contextlib

from contextlib_context_managers import *


def variable_stack(contexts):
    with contextlib.ExitStack() as stack:
        for c in contexts:
            stack.enter_context(c)
        # Return the close() method of a new stack as a clean-up
        # function.
        return stack.pop_all().close
    # Explicitly return None, indicating that the ExitStack could
    # not be initialized cleanly but that cleanup has already
    # occurred.
    return None


print('No errors:')
cleaner = variable_stack([
    HandleError(1),
    HandleError(2),
])
cleaner()

print('\nHandled error building context manager stack:')
try:
    cleaner = variable_stack([
        HandleError(1),
        ErrorOnEnter(2),
    ])
except RuntimeError as err:
    print('caught error {}'.format(err))
else:
    if cleaner is not None:
        cleaner()
    else:
        print('no cleaner returned')

print('\nUnhandled error building context manager stack:')
try:
    cleaner = variable_stack([
        PassError(1),
        ErrorOnEnter(2),
    ])
except RuntimeError as err:
    print('caught error {}'.format(err))
else:
    if cleaner is not None:
        cleaner()
    else:
        print('no cleaner returned')
        
# output
# No errors:
#   HandleError(1): entering
#   HandleError(2): entering
#   HandleError(2): exiting False
#   HandleError(1): exiting False
# 
# Handled error building context manager stack:
#   HandleError(1): entering
#   ErrorOnEnter(2): throwing error on enter
#   HandleError(1): handling exception RuntimeError('from 2')
#   HandleError(1): exiting True
# no cleaner returned
# 
# Unhandled error building context manager stack:
#   PassError(1): entering
#   ErrorOnEnter(2): throwing error on enter
#   PassError(1): passing exception RuntimeError('from 2')
#   PassError(1): exiting
# caught error from 2
```

此示例使用前面定义的相同上下文管理器类，其差异是 `ErrorOnEnter` 产生的错误是  `__enter__()` 而不是 `__exit__()`。在 `variable_stack()` 内，如果输入的所有上下文都没有错误，则返回一个  `ExitStack` 的 `close()` 方法。如果发生处理错误，则 `variable_stack()` 返回  `None` 来表示已完成清理工作。如果发生未处理的错误，则清除部分堆栈并传播错误。

相关文档：

https://pymotw.com/3/contextlib/index.html