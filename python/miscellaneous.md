# day01

## 整型
- Python中可以处理任意大小的整数（Python 2.x中有int和long两种类型的整数，但这种区分对Python来说意义不大，因此在Python 3.x中整数只有int这一种了）
- 而且支持二进制（如0b100，换算成十进制是4）、八进制（如0o100，换算成十进制是64）、十进制（100）和十六进制（0x100，换算成十进制是256）的表示法。

## 类型注解
- python 3.5 之后引入，例：
```python
def printInt(i : int):
	print(i)
```
 
## 常用数据类型
- 列表（list）: []
	1. 列表生成器
- 字典（dict/map）: {'12': 12}
	1. 一个对象能不能作为字典的key，就取决于其有没有__hash__方法。
	2. 所以所有python自带类型中，除了list、dict、set和内部至少带有上述三种类型之一的tuple之外，其余的对象都能当key。
- 元组（tuple）：('physics', 'chemistry', 1997, 2000) 
	1. 元素不可以进行修改
	2. tup1 = (50,) -> 只有一个元素的元组，后面需要加上一个逗号
- 集合 ：{1,2,3,4}
- 总的来说，python中一些基础变量是不可变类型，即不能修改其数值
	- 修改之后，其实是重新申请了一块内存空间
- python中函数参数传递都是引用传递（可以理解成地址传入地址）
- [可变与不可变变量](https://zhuanlan.zhihu.com/p/34395671)

## python 中模块的导入
- 需要说明的是，如果我们导入的模块除了定义函数之外还中有可以执行代码，那么Python解释器在导入这个模块时就会执行这些代码，事实上我们可能并不希望如此，因此如果我们在模块中编写了执行代码，最好是将这些执行代码放入如下所示的条件中，这样的话除非直接运行该模块，if条件下的这些代码是不会执行的，因为只有直接执行的模块的名字才是"__main__"

```python
# __name__是Python中一个隐含的变量它代表了模块的名字
# 只有被Python解释器直接执行的模块的名字才是__main__
if __name__ == '__main__':
	print('call foo()')
	foo()
	print('call bar()')
	bar()
```

## GIL
- python 的全局锁，保证每时每刻只有一个线程在运行
 
--------------------------------------------------------------------
## list
```python
# 如果需要 index
list1 = ['str0', 'str1', 'str2', 'str3', 'str4']
for index, item in enumerate(list1):
	print index, item

for item in list1:
	print item
```

## dict
```python
dict1 = {0: 'str0', 1: 'str1', 2: 'str2', 3: 'str3', 4: 'str4'}
for k, v in dict1.items():
	print k, v

print dict1.keys()
print dict1.values()
print dict1.items()
```

## 变量赋值
变量赋值可以用 a = b if Condition else c


## 根据变量判断是否执行某个函数
```python
def func():
	print 'do something...'

flag = True

flag and func()
```