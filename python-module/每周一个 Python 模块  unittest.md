# 每周一个 Python 模块 | unittest

unittest 是 Python 自带的单元测试框架，可以用来作自动化测试框架的用例组织执行。

优点：提供用例组织与执行方法；提供比较方法；提供丰富的日志、清晰的报告。

## unittest 核心工作原理

**unittest 中最核心的部分是：TestFixture、TestCase、TestSuite、TestRunner。**

下面我们分别来解释这四个概念的意思，先来看一张 unittest 的静态类图：

![unittest](D:\work\article\unittest.png)

- 一个 TestCase 的实例就是一个测试用例。什么是测试用例呢？就是一个完整的测试流程，包括测试前准备环境的搭建（setUp），执行测试代码（run），以及测试后环境的还原（tearDown）。元测试（unit test）的本质也就在这里，一个测试用例是一个完整的测试单元，通过运行这个测试单元，可以对某一个问题进行验证。
- 而多个测试用例集合在一起，就是 TestSuite，而且 TestSuite 也可以嵌套 TestSuite。
- TestLoader 是用来加载 TestCase 到 TestSuite 中的，其中有几个 loadTestsFrom__() 方法，就是从各个地方寻找 TestCase，创建它们的实例，然后 add 到 TestSuite 中，再返回一个 TestSuite 实例。
- TextTestRunner 是来执行测试用例的，其中的 `run(test)` 会执行 TestSuite/TestCase 中的 `run(result)` 方法。 测试的结果会保存到 TextTestResul t实例中，包括运行了多少测试用例，成功了多少，失败了多少等信息。
- 而对一个测试用例环境的搭建和销毁，是一个 Fixture。

一个 class 继承了 unittest.TestCase，便是一个测试用例，但如果其中有多个以 `test` 开头的方法，那么每有一个这样的方法，在 load 的时候便会生成一个 TestCase 实例，如：一个 class 中有四个 test_xxx 方法，最后在 load 到 suite 中时也有四个测试用例。

到这里整个流程就清楚了：

- 写好 TestCase。
- 由 TestLoader 加载 TestCase 到 TestSuite。
- 然后由 TextTestRunner 来运行 TestSuite，运行的结果保存在 TextTestResult 中。
  通过命令行或者 `unittest.main()` 执行时，`main()` 会调用 TextTestRunner 中的 ` run()` 来执行，或者可以直接通过 TextTestRunner 来执行用例。
- 在 Runner 执行时，默认将执行结果输出到控制台，我们可以设置其输出到文件，在文件中查看结果（你可能听说过 HTMLTestRunner，是的，通过它可以将结果输出到 HTML 中，生成漂亮的报告，它跟TextTestRunner 是一样的，从名字就能看出来，这个我们后面再说）。

## unittest 实例

下面我们通过一些实例来更好地认识一下 unittest。

### 写 TestCase

先准备待测试的方法，如下：

```python
# mathfunc.py

# -*- coding: utf-8 -*-

def add(a, b):
    return a+b

def minus(a, b):
    return a-b

def multi(a, b):
    return a*b

def divide(a, b):
    return a/b
```

写 TestCase，如下：

``` python
# test_mathfunc.py

# -*- coding: utf-8 -*-

import unittest
from mathfunc import *


class TestMathFunc(unittest.TestCase):
    """Test mathfuc.py"""

    def test_add(self):
        """Test method add(a, b)"""
        self.assertEqual(3, add(1, 2))
        self.assertNotEqual(3, add(2, 2))

    def test_minus(self):
        """Test method minus(a, b)"""
        self.assertEqual(1, minus(3, 2))

    def test_multi(self):
        """Test method multi(a, b)"""
        self.assertEqual(6, multi(2, 3))

    def test_divide(self):
        """Test method divide(a, b)"""
        self.assertEqual(2, divide(6, 3))
        self.assertEqual(2.5, divide(5, 2))

if __name__ == '__main__':
    unittest.main()
```

执行结果：

```python
.F..
======================================================================
FAIL: test_divide (__main__.TestMathFunc)
Test method divide(a, b)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:/py/test_mathfunc.py", line 26, in test_divide
    self.assertEqual(2.5, divide(5, 2))
AssertionError: 2.5 != 2

----------------------------------------------------------------------
Ran 4 tests in 0.000s

FAILED (failures=1)
```

能够看到一共运行了 4 个测试，失败了 1 个，并且给出了失败原因，`2.5 != 2` 也就是说我们的 divide 方法是有问题的。

这就是一个简单的测试，有几点需要说明的：

1. 在第一行给出了每一个用例执行的结果的标识，成功是 `.`，失败是 `F`，出错是 `E`，跳过是 `S`。从上面也可以看出，测试的执行跟方法的顺序没有关系，test_divide 写在了第 4 个，但是却是第 2 个执行的。
2. 每个测试方法均以 `test` 开头，否则是不被 unittest 识别的。
3. 在 `unittest.main()` 中加 `verbosity` 参数可以控制输出的错误报告的详细程度，默认是 `1`，如果设为 `0`，则不输出每一用例的执行结果，即没有上面的结果中的第 1 行；如果设为 `2`，则输出详细的执行结果，如下：

```python
test_add (__main__.TestMathFunc)
Test method add(a, b) ... ok
test_divide (__main__.TestMathFunc)
Test method divide(a, b) ... FAIL
test_minus (__main__.TestMathFunc)
Test method minus(a, b) ... ok
test_multi (__main__.TestMathFunc)
Test method multi(a, b) ... ok

======================================================================
FAIL: test_divide (__main__.TestMathFunc)
Test method divide(a, b)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:/py/test_mathfunc.py", line 26, in test_divide
    self.assertEqual(2.5, divide(5, 2))
AssertionError: 2.5 != 2

----------------------------------------------------------------------
Ran 4 tests in 0.002s

FAILED (failures=1)
```

可以看到，每一个用例的详细执行情况以及用例名，用例描述均被输出了出来（在测试方法下加代码示例中的”"”Doc String””“，在用例执行时，会将该字符串作为此用例的描述，**加合适的注释能够使输出的测试报告更加便于阅读**）。

### 组织 TestSuite

上面的代码演示了如何编写一个简单的测试，但有两个问题，我们怎么控制用例执行的顺序呢？（这里的示例中的几个测试方法并没有一定关系，但之后你写的用例可能会有先后关系，需要先执行方法 A，再执行方法 B），我们就要用到 TestSuite 了。我们**添加到 TestSuite 中的 case 是会按照添加的顺序执行的**。

问题二是我们现在只有一个测试文件，我们直接执行该文件即可，但如果有多个测试文件，怎么进行组织，总不能一个个文件执行吧，答案也在 TestSuite 中。

下面来个例子：

在文件夹中我们再新建一个文件，**test_suite.py**：

```python
# -*- coding: utf-8 -*-

import unittest
from test_mathfunc import TestMathFunc

if __name__ == '__main__':
    suite = unittest.TestSuite()

    tests = [TestMathFunc("test_add"), TestMathFunc("test_minus"), TestMathFunc("test_divide")]
    suite.addTests(tests)

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
```

执行结果：

```python
test_add (test_mathfunc.TestMathFunc)
Test method add(a, b) ... ok
test_minus (test_mathfunc.TestMathFunc)
Test method minus(a, b) ... ok
test_divide (test_mathfunc.TestMathFunc)
Test method divide(a, b) ... FAIL

======================================================================
FAIL: test_divide (test_mathfunc.TestMathFunc)
Test method divide(a, b)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\py\test_mathfunc.py", line 26, in test_divide
    self.assertEqual(2.5, divide(5, 2))
AssertionError: 2.5 != 2

----------------------------------------------------------------------
Ran 3 tests in 0.001s

FAILED (failures=1)
```

可以看到，执行情况跟我们预料的一样：执行了三个 case，并且顺序是按照我们添加进 suite 的顺序执行的。

上面用了 TestSuite 的 `addTests()` 方法，并直接传入了 TestCase 列表，我们还可以：

```python
# 直接用addTest方法添加单个TestCase
suite.addTest(TestMathFunc("test_multi"))

# 用addTests + TestLoader
# loadTestsFromName()，传入'模块名.TestCase名'
suite.addTests(unittest.TestLoader().loadTestsFromName('test_mathfunc.TestMathFunc'))
suite.addTests(unittest.TestLoader().loadTestsFromNames(['test_mathfunc.TestMathFunc']))  # loadTestsFromNames()，类似，传入列表

# loadTestsFromTestCase()，传入TestCase
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestMathFunc))
```

注意，用 TestLoader 的方法是无法对 case 进行排序的，同时，suite 中也可以套 suite。

### TestLoader 并输出结果

用例组织好了，但结果只能输出到控制台，这样没有办法查看之前的执行记录，我们想将结果输出到文件。很简单，看示例：

修改 **test_suite.py**：

```python
# -*- coding: utf-8 -*-

import unittest
from test_mathfunc import TestMathFunc

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestMathFunc))

    with open('UnittestTextReport.txt', 'a') as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        runner.run(suite)
```

执行此文件，可以看到，在同目录下生成了 **UnittestTextReport.txt**，所有的执行报告均输出到了此文件中，这下我们便有了 txt 格式的测试报告了。

但是文本报告太过简陋，是不是想要更加高大上的 HTML 报告？但 unittest 自己可没有带 HTML 报告，我们只能求助于外部的库了。

HTMLTestRunner 是一个第三方的 unittest HTML 报告库，我们下载 **HTMLTestRunner.py**，并导入就可以运行了。

官方地址：http://tungwaiyip.info/software/HTMLTestRunner.html

修改我们的 `test_suite.py`：

```
# -*- coding: utf-8 -*-

import unittest
from test_mathfunc import TestMathFunc
from HTMLTestRunner import HTMLTestRunner

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestMathFunc))

    with open('HTMLReport.html', 'w') as f:
        runner = HTMLTestRunner(stream=f,
                                title='MathFunc Test Report',
                                description='generated by HTMLTestRunner.',
                                verbosity=2
                                )
        runner.run(suite)
```

这样，在执行时，在控制台我们能够看到执行情况，如下：

```
ok test_add (test_mathfunc.TestMathFunc)
F  test_divide (test_mathfunc.TestMathFunc)
ok test_minus (test_mathfunc.TestMathFunc)
ok test_multi (test_mathfunc.TestMathFunc)

Time Elapsed: 0:00:00.001000
```

并且输出了 HTML 测试报告，`HTMLReport.html`。

这下漂亮的 HTML 报告也有了。其实你能发现，HTMLTestRunner 的执行方法跟 TextTestRunner 很相似，你可以跟上面的示例对比一下，就是把类图中的 runner 换成了 HTMLTestRunner，并将 TestResult 用 HTML 的形式展现出来，如果你研究够深，可以写自己的 runner，生成更复杂更漂亮的报告。

### TestFixture 准备和清除环境

上面整个测试基本跑了下来，但可能会遇到点特殊的情况：如果我的测试需要在每次执行之前准备环境，或者在每次执行完之后需要进行一些清理怎么办？比如执行前需要连接数据库，执行完成之后需要还原数据、断开连接。总不能每个测试方法中都添加准备环境、清理环境的代码吧。

这就要涉及到我们之前说过的 test fixture 了，修改 **test_mathfunc.py**：

```python
# -*- coding: utf-8 -*-

import unittest
from mathfunc import *


class TestMathFunc(unittest.TestCase):
    """Test mathfuc.py"""

    def setUp(self):
        print "do something before test.Prepare environment."

    def tearDown(self):
        print "do something after test.Clean up."

    def test_add(self):
        """Test method add(a, b)"""
        print "add"
        self.assertEqual(3, add(1, 2))
        self.assertNotEqual(3, add(2, 2))

    def test_minus(self):
        """Test method minus(a, b)"""
        print "minus"
        self.assertEqual(1, minus(3, 2))

    def test_multi(self):
        """Test method multi(a, b)"""
        print "multi"
        self.assertEqual(6, multi(2, 3))

    def test_divide(self):
        """Test method divide(a, b)"""
        print "divide"
        self.assertEqual(2, divide(6, 3))
        self.assertEqual(2.5, divide(5, 2))
```

我们添加了 `setUp()` 和 `tearDown()` 两个方法（其实是重写了 TestCase 的这两个方法），这两个方法在每个测试方法执行前以及执行后执行一次，setUp 用来为测试准备环境，tearDown 用来清理环境，已备之后的测试。

我们再执行一次：

```python
test_add (test_mathfunc.TestMathFunc)
Test method add(a, b) ... ok
test_divide (test_mathfunc.TestMathFunc)
Test method divide(a, b) ... FAIL
test_minus (test_mathfunc.TestMathFunc)
Test method minus(a, b) ... ok
test_multi (test_mathfunc.TestMathFunc)
Test method multi(a, b) ... ok

======================================================================
FAIL: test_divide (test_mathfunc.TestMathFunc)
Test method divide(a, b)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\py\test_mathfunc.py", line 36, in test_divide
    self.assertEqual(2.5, divide(5, 2))
AssertionError: 2.5 != 2

----------------------------------------------------------------------
Ran 4 tests in 0.000s

FAILED (failures=1)
do something before test.Prepare environment.
add
do something after test.Clean up.
do something before test.Prepare environment.
divide
do something after test.Clean up.
do something before test.Prepare environment.
minus
do something after test.Clean up.
do something before test.Prepare environment.
multi
do something after test.Clean up.
```

可以看到 setUp 和 tearDown 在每次执行 case 前后都执行了一次。

如果想要在所有 case 执行之前准备一次环境，并在所有 case 执行结束之后再清理环境，我们可以用 `setUpClass()` 与 `tearDownClass()`:

```python
...

class TestMathFunc(unittest.TestCase):
    """Test mathfuc.py"""

    @classmethod
    def setUpClass(cls):
        print "This setUpClass() method only called once."

    @classmethod
    def tearDownClass(cls):
        print "This tearDownClass() method only called once too."

...
```

执行结果如下：

```python
...
This setUpClass() method only called once.
do something before test.Prepare environment.
add
...
multi
do something after test.Clean up.
This tearDownClass() method only called once too.
```

可以看到 setUpClass 以及 tearDownClass 均只执行了一次。

## 一些有用的方法

### 断言 Assert

大多数测试断言某些条件的真实性。编写真值检查测试有两种不同的方法，具体取决于测试作者的观点以及所测试代码的预期结果。

```python
# unittest_truth.py

import unittest


class TruthTest(unittest.TestCase):

    def testAssertTrue(self):
        self.assertTrue(True)

    def testAssertFalse(self):
        self.assertFalse(False)
```

如果代码生成的值为 true，则应使用`assertTrue()`方法。如果代码产生值为 false，则方法`assertFalse()`更有意义。

```python
$ python3 -m unittest -v unittest_truth.py

testAssertFalse (unittest_truth.TruthTest) ... ok
testAssertTrue (unittest_truth.TruthTest) ... ok

----------------------------------------------------------------
Ran 2 tests in 0.000s

OK
```

### 测试相等

`unittest`包括测试两个值相等的方法如下：

```python
# unittest_equality.py 

import unittest


class EqualityTest(unittest.TestCase):

    def testExpectEqual(self):
        self.assertEqual(1, 3 - 2)

    def testExpectEqualFails(self):
        self.assertEqual(2, 3 - 2)

    def testExpectNotEqual(self):
        self.assertNotEqual(2, 3 - 2)

    def testExpectNotEqualFails(self):
        self.assertNotEqual(1, 3 - 2)
```

当失败时，这些特殊的测试方法会产生错误消息，包括被比较的值。

```python
$ python3 -m unittest -v unittest_equality.py

testExpectEqual (unittest_equality.EqualityTest) ... ok
testExpectEqualFails (unittest_equality.EqualityTest) ... FAIL
testExpectNotEqual (unittest_equality.EqualityTest) ... ok
testExpectNotEqualFails (unittest_equality.EqualityTest) ... FAIL

================================================================
FAIL: testExpectEqualFails (unittest_equality.EqualityTest)
----------------------------------------------------------------
Traceback (most recent call last):
  File ".../unittest_equality.py", line 15, in
testExpectEqualFails
    self.assertEqual(2, 3 - 2)
AssertionError: 2 != 1

================================================================
FAIL: testExpectNotEqualFails (unittest_equality.EqualityTest)
----------------------------------------------------------------
Traceback (most recent call last):
  File ".../unittest_equality.py", line 21, in
testExpectNotEqualFails
    self.assertNotEqual(1, 3 - 2)
AssertionError: 1 == 1

----------------------------------------------------------------
Ran 4 tests in 0.001s

FAILED (failures=2)
```

### 几乎相等

除了严格相等之外，还可以使用`assertAlmostEqual()` 和`assertNotAlmostEqual()`测试浮点数的近似相等。

```python
# unittest_almostequal.py 

import unittest


class AlmostEqualTest(unittest.TestCase):

    def testEqual(self):
        self.assertEqual(1.1, 3.3 - 2.2)

    def testAlmostEqual(self):
        self.assertAlmostEqual(1.1, 3.3 - 2.2, places=1)

    def testNotAlmostEqual(self):
        self.assertNotAlmostEqual(1.1, 3.3 - 2.0, places=1)
```

参数是要比较的值，以及用于测试的小数位数。

```python
$ python3 -m unittest unittest_almostequal.py

.F.
================================================================
FAIL: testEqual (unittest_almostequal.AlmostEqualTest)
----------------------------------------------------------------
Traceback (most recent call last):
  File ".../unittest_almostequal.py", line 12, in testEqual
    self.assertEqual(1.1, 3.3 - 2.2)
AssertionError: 1.1 != 1.0999999999999996

----------------------------------------------------------------
Ran 3 tests in 0.001s

FAILED (failures=1)
```

### 容器

除了通用的`assertEqual()`和 `assertNotEqual()`，也有比较`list`，`dict`和`set` 对象的方法。

```python
# unittest_equality_container.py 

import textwrap
import unittest


class ContainerEqualityTest(unittest.TestCase):

    def testCount(self):
        self.assertCountEqual(
            [1, 2, 3, 2],
            [1, 3, 2, 3],
        )

    def testDict(self):
        self.assertDictEqual(
            {'a': 1, 'b': 2},
            {'a': 1, 'b': 3},
        )

    def testList(self):
        self.assertListEqual(
            [1, 2, 3],
            [1, 3, 2],
        )

    def testMultiLineString(self):
        self.assertMultiLineEqual(
            textwrap.dedent("""
            This string
            has more than one
            line.
            """),
            textwrap.dedent("""
            This string has
            more than two
            lines.
            """),
        )

    def testSequence(self):
        self.assertSequenceEqual(
            [1, 2, 3],
            [1, 3, 2],
        )

    def testSet(self):
        self.assertSetEqual(
            set([1, 2, 3]),
            set([1, 3, 2, 4]),
        )

    def testTuple(self):
        self.assertTupleEqual(
            (1, 'a'),
            (1, 'b'),
        )
```

每种方法都使用对输入类型有意义的格式定义函数，使测试失败更容易理解和纠正。

```python
$ python3 -m unittest unittest_equality_container.py

FFFFFFF
================================================================
FAIL: testCount
(unittest_equality_container.ContainerEqualityTest)
----------------------------------------------------------------
Traceback (most recent call last):
  File ".../unittest_equality_container.py", line 15, in
testCount
    [1, 3, 2, 3],
AssertionError: Element counts were not equal:
First has 2, Second has 1:  2
First has 1, Second has 2:  3

================================================================
FAIL: testDict
(unittest_equality_container.ContainerEqualityTest)
----------------------------------------------------------------
Traceback (most recent call last):
  File ".../unittest_equality_container.py", line 21, in
testDict
    {'a': 1, 'b': 3},
AssertionError: {'a': 1, 'b': 2} != {'a': 1, 'b': 3}
- {'a': 1, 'b': 2}
?               ^

+ {'a': 1, 'b': 3}
?               ^


================================================================
FAIL: testList
(unittest_equality_container.ContainerEqualityTest)
----------------------------------------------------------------
Traceback (most recent call last):
  File ".../unittest_equality_container.py", line 27, in
testList
    [1, 3, 2],
AssertionError: Lists differ: [1, 2, 3] != [1, 3, 2]

First differing element 1:
2
3

- [1, 2, 3]
+ [1, 3, 2]

================================================================
FAIL: testMultiLineString
(unittest_equality_container.ContainerEqualityTest)
----------------------------------------------------------------
Traceback (most recent call last):
  File ".../unittest_equality_container.py", line 41, in
testMultiLineString
    """),
AssertionError: '\nThis string\nhas more than one\nline.\n' !=
'\nThis string has\nmore than two\nlines.\n'

- This string
+ This string has
?            ++++
- has more than one
? ----           --
+ more than two
?           ++
- line.
+ lines.
?     +


================================================================
FAIL: testSequence
(unittest_equality_container.ContainerEqualityTest)
----------------------------------------------------------------
Traceback (most recent call last):
  File ".../unittest_equality_container.py", line 47, in
testSequence
    [1, 3, 2],
AssertionError: Sequences differ: [1, 2, 3] != [1, 3, 2]

First differing element 1:
2
3

- [1, 2, 3]
+ [1, 3, 2]

================================================================
FAIL: testSet
(unittest_equality_container.ContainerEqualityTest)
----------------------------------------------------------------
Traceback (most recent call last):
  File ".../unittest_equality_container.py", line 53, in testSet
    set([1, 3, 2, 4]),
AssertionError: Items in the second set but not the first:
4

================================================================
FAIL: testTuple
(unittest_equality_container.ContainerEqualityTest)
----------------------------------------------------------------
Traceback (most recent call last):
  File ".../unittest_equality_container.py", line 59, in
testTuple
    (1, 'b'),
AssertionError: Tuples differ: (1, 'a') != (1, 'b')

First differing element 1:
'a'
'b'

- (1, 'a')
?      ^

+ (1, 'b')
?      ^


----------------------------------------------------------------
Ran 7 tests in 0.005s

FAILED (failures=7)
```

使用`assertIn()`测试容器关系。

```python
# unittest_in.py 

import unittest


class ContainerMembershipTest(unittest.TestCase):

    def testDict(self):
        self.assertIn(4, {1: 'a', 2: 'b', 3: 'c'})

    def testList(self):
        self.assertIn(4, [1, 2, 3])

    def testSet(self):
        self.assertIn(4, set([1, 2, 3]))
```

任何对象都支持`in`运算符或容器 API `assertIn()`。

```python
$ python3 -m unittest unittest_in.py

FFF
================================================================
FAIL: testDict (unittest_in.ContainerMembershipTest)
----------------------------------------------------------------
Traceback (most recent call last):
  File ".../unittest_in.py", line 12, in testDict
    self.assertIn(4, {1: 'a', 2: 'b', 3: 'c'})
AssertionError: 4 not found in {1: 'a', 2: 'b', 3: 'c'}

================================================================
FAIL: testList (unittest_in.ContainerMembershipTest)
----------------------------------------------------------------
Traceback (most recent call last):
  File ".../unittest_in.py", line 15, in testList
    self.assertIn(4, [1, 2, 3])
AssertionError: 4 not found in [1, 2, 3]

================================================================
FAIL: testSet (unittest_in.ContainerMembershipTest)
----------------------------------------------------------------
Traceback (most recent call last):
  File ".../unittest_in.py", line 18, in testSet
    self.assertIn(4, set([1, 2, 3]))
AssertionError: 4 not found in {1, 2, 3}

----------------------------------------------------------------
Ran 3 tests in 0.001s

FAILED (failures=3)
```

### 测试异常

如前所述，如果测试引发异常，则将 `AssertionError`视为错误。这对于修改具有现有测试覆盖率的代码时发现错误非常有用。但是，在某些情况下，测试应验证某些代码是否确实产生异常。

例如，如果给对象的属性赋予无效值。在这种情况下， `assertRaises()`使代码比在测试中捕获异常更清晰。比较这两个测试：

```python
# unittest_exception.py 

import unittest


def raises_error(*args, **kwds):
    raise ValueError('Invalid value: ' + str(args) + str(kwds))


class ExceptionTest(unittest.TestCase):

    def testTrapLocally(self):
        try:
            raises_error('a', b='c')
        except ValueError:
            pass
        else:
            self.fail('Did not see ValueError')

    def testAssertRaises(self):
        self.assertRaises(
            ValueError,
            raises_error,
            'a',
            b='c',
        )
```

两者的结果是相同的，但第二次使用的 `assertRaises()`更简洁。

```python
$ python3 -m unittest -v unittest_exception.py

testAssertRaises (unittest_exception.ExceptionTest) ... ok
testTrapLocally (unittest_exception.ExceptionTest) ... ok

----------------------------------------------------------------
Ran 2 tests in 0.000s

OK
```

### 用不同的输入重复测试

使用不同的输入运行相同的测试逻辑通常很有用。不是为每个小案例定义单独的测试方法，而是使用一种包含多个相关断言调用的测试方法。这种方法的问题在于，只要一个断言失败，就会跳过其余的断言。更好的解决方案是使用`subTest()`在测试方法中为测试创建上下文。如果测试失败，则报告失败并继续进行其余测试。

```python
# unittest_subtest.py 

import unittest


class SubTest(unittest.TestCase):

    def test_combined(self):
        self.assertRegex('abc', 'a')
        self.assertRegex('abc', 'B')
        # The next assertions are not verified!
        self.assertRegex('abc', 'c')
        self.assertRegex('abc', 'd')

    def test_with_subtest(self):
        for pat in ['a', 'B', 'c', 'd']:
            with self.subTest(pattern=pat):
                self.assertRegex('abc', pat)
```

在该示例中，`test_combined()`方法从不运行断言`'c'`和`'d'`。`test_with_subtest()`方法可以正确报告其他故障。请注意，即使报告了三个故障，测试运行器仍然认为只有两个测试用例。

```python
$ python3 -m unittest -v unittest_subtest.py

test_combined (unittest_subtest.SubTest) ... FAIL
test_with_subtest (unittest_subtest.SubTest) ...
================================================================
FAIL: test_combined (unittest_subtest.SubTest)
----------------------------------------------------------------
Traceback (most recent call last):
  File ".../unittest_subtest.py", line 13, in test_combined
    self.assertRegex('abc', 'B')
AssertionError: Regex didn't match: 'B' not found in 'abc'

================================================================
FAIL: test_with_subtest (unittest_subtest.SubTest) (pattern='B')
----------------------------------------------------------------
Traceback (most recent call last):
  File ".../unittest_subtest.py", line 21, in test_with_subtest
    self.assertRegex('abc', pat)
AssertionError: Regex didn't match: 'B' not found in 'abc'

================================================================
FAIL: test_with_subtest (unittest_subtest.SubTest) (pattern='d')
----------------------------------------------------------------
Traceback (most recent call last):
  File ".../unittest_subtest.py", line 21, in test_with_subtest
    self.assertRegex('abc', pat)
AssertionError: Regex didn't match: 'd' not found in 'abc'

----------------------------------------------------------------
Ran 2 tests in 0.001s

FAILED (failures=3)
```

### 跳过某个 case

如果我们临时想要跳过某个 case 不执行怎么办？unittest 也提供了几种方法：

#### skip 装饰器

```python
...

class TestMathFunc(unittest.TestCase):
    """Test mathfuc.py"""

    ...

    @unittest.skip("I don't want to run this case.")
    def test_divide(self):
        """Test method divide(a, b)"""
        print "divide"
        self.assertEqual(2, divide(6, 3))
        self.assertEqual(2.5, divide(5, 2))
```

执行：

```python
...
test_add (test_mathfunc.TestMathFunc)
Test method add(a, b) ... ok
test_divide (test_mathfunc.TestMathFunc)
Test method divide(a, b) ... skipped "I don't want to run this case."
test_minus (test_mathfunc.TestMathFunc)
Test method minus(a, b) ... ok
test_multi (test_mathfunc.TestMathFunc)
Test method multi(a, b) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.000s

OK (skipped=1)
```

可以看到总的 test 数量还是 4 个，但 divide() 方法被 skip 了。

skip 装饰器一共有三个 `unittest.skip(reason)`、`unittest.skipIf(condition, reason)`、`unittest.skipUnless(condition, reason)`，skip 无条件跳过，skipIf 当 condition 为 True 时跳过，skipUnless 当 condition 为 False 时跳过。

#### TestCase.skipTest() 方法

```python
...

class TestMathFunc(unittest.TestCase):
    """Test mathfuc.py"""

    ...

    def test_divide(self):
        """Test method divide(a, b)"""
        self.skipTest('Do not run this.')
        print "divide"
        self.assertEqual(2, divide(6, 3))
        self.assertEqual(2.5, divide(5, 2))
```

输出：

```python
...
test_add (test_mathfunc.TestMathFunc)
Test method add(a, b) ... ok
test_divide (test_mathfunc.TestMathFunc)
Test method divide(a, b) ... skipped 'Do not run this.'
test_minus (test_mathfunc.TestMathFunc)
Test method minus(a, b) ... ok
test_multi (test_mathfunc.TestMathFunc)
Test method multi(a, b) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.001s

OK (skipped=1)
```

效果跟上面的装饰器一样，跳过了 divide 方法。

### 忽略失败的测试

可以使用`expectedFailure()`装饰器来忽略失败的测试。

```python
# unittest_expectedfailure.py 

import unittest


class Test(unittest.TestCase):

    @unittest.expectedFailure
    def test_never_passes(self):
        self.assertTrue(False)

    @unittest.expectedFailure
    def test_always_passes(self):
        self.assertTrue(True)
```

如果预期失败的测试通过了，则该条件被视为特殊类型的失败，并报告为“意外成功”。

```python
$ python3 -m unittest -v unittest_expectedfailure.py

test_always_passes (unittest_expectedfailure.Test) ...
unexpected success
test_never_passes (unittest_expectedfailure.Test) ... expected
failure

----------------------------------------------------------------
Ran 2 tests in 0.001s

FAILED (expected failures=1, unexpected successes=1)
```

## 总结

1. unittest 是 Python 自带的单元测试框架，我们可以用其来作为我们自动化测试框架的用例组织执行框架。
2. unittest 的流程：写好 TestCase，然后由 TestLoader 加载 TestCase 到 TestSuite，然后由 TextTestRunner来运行 TestSuite，运行的结果保存在 TextTestResult 中，我们通过命令行或者 unittest.main() 执行时，main 会调用 TextTestRunner 中的 run 来执行，或者我们可以直接通过 TextTestRunner 来执行用例。
3. 一个 class 继承 unittest.TestCase 即是一个 TestCase，其中以 `test` 开头的方法在 load 时被加载为一个真正的 TestCase。
4. verbosity 参数可以控制执行结果的输出，`0` 是简单报告、`1` 是一般报告、`2` 是详细报告。
5. 可以通过 addTest 和 addTests 向 suite 中添加 case 或 suite，可以用 TestLoader 的 loadTestsFrom__() 方法。
6. 用 `setUp()`、`tearDown()`、`setUpClass()`以及 `tearDownClass()`可以在用例执行前布置环境，以及在用例执行后清理环境。
7. 我们可以通过 skip，skipIf，skipUnless 装饰器跳过某个 case，或者用 TestCase.skipTest 方法。
8. 参数中加 stream，可以将报告输出到文件：可以用 TextTestRunner 输出 txt 报告，以及可以用HTMLTestRunner 输出 html 报告。

相关文档：

https://pymotw.com/3/unittest/index.html

https://huilansame.github.io/huilansame.github.io/archivers/python-unittest

https://segmentfault.com/a/1190000016315201#articleHeader0