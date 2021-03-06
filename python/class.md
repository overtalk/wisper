## 类
- __init__ 是一个特殊方法用于在创建对象时进行初始化操作

### __slots__魔法
- 可以通过在类中定义 __slots__ 变量来进行限定。需要注意的是 __slots__ 的限定只对当前类的对象生效，对子类并不起任何作用。

```python
class Person(object):

	# 限定Person对象只能绑定_name, _age和_gender属性
	__slots__ = ('_name', '_age', '_gender')
```

### 静态方法
- 某个class的静态方法，不属于特定的实例
```python
class demo(object):
	@staticmethod
	def valid(name, age):
		''' class 的静态方法，用于判断参数是否正确
		'''
		import types
		if (type(age) is not types.IntType) or (type(name) is not types.StringType):
			return False
		return age < 100
```

### 类方法
- 和静态方法比较类似，Python还可以在类中定义类方法，类方法的第一个参数约定名为cls，它代表的是当前类相关的信息的对象（类本身也是一个对象，有的地方也称之为类的元数据对象），通过这个参数我们可以获取和类相关的信息并且可以创建出类的对象。
```python
class demo(object):
	@classmethod
	def now(cls):
		ctime = localtime(time())
		return cls(ctime.tm_hour, ctime.tm_min, ctime.tm_sec)
```

## 抽象 class
- 有抽象方法的类不可以被实例化

```python
from abc import ABCMeta, abstractmethod

class pet(object):
	@abstractmethod
	def make_voice(self):
		pass
```

## Python中如何动态设置和获取对象属性？
- setattr(object, name, value)和getattr(object, name[, default])内置函数
- 其中object是对象，name是对象的属性名，value是属性值。
- 这两个函数会调用对象的`__getattr__`和`__setattr__`魔术方法。


-----------------------

## Python 在运行时创建新的类
- 其实 type() 函数不仅可以返回一个对象的类型，也可以创建出新的类型
```python
type(类名, 父类的元组（针对继承的情况，可以为空），包含属性的字典（名称和值）)
```
- Python 解释器遇到 class 定义时，仅仅是扫描一下 class 定义的语法，然后调用 type() 函数创建出 class 的。

```python
# -*- coding: utf-8 -*-


def __init__(self, name):
	self.name = name

def introduction(self):
	print 'i am ', self.name

if __name__ == '__main__':
	Person = type('Person', (object, ), dict(introduction=introduction, __init__=__init__))
	print Person
	p = Person('python')
	p.introduction()
```