## -*- coding:utf-8 -*-

'''
函数默认参数 尽量不要使用[], {} 应该使用None，然后通过判断是否为None值
默认参数以对象的形式再函数定义的时候被创建，会被重复利用
'''
def func1(cur_param=[]):
	cur_param.append(1)
	print cur_param

def func2(cur_param=None):
	if cur_param is None:
		cur_param = []
	cur_param.append(1)
	print cur_param

if __name__ == '__main__':
	func1()  # [1]
	func1()  # [1, 1]
	func2()  # [1]
	func2()  # [1]


'''
python并没有对变量或者方法做真正的私有化
而是通过name mangling 将私有函数和私有变量进行重命名
在外部可通过_classname__attributename 直接获取私有属性。
'''
class A(object):
	def __init__(self):
		self.__parame1 = 'test'

	def __func1(self):
		print 'this is a private function'

if __name__ == '__main__':
	print '====================='
	a = A()
	print A.__dict__
	print a.__dict__
	# 通过这种方法可以拿到私有变量
	print a._A__parame1
	a._A__func1()

'''
循环语句在遍历对象时会生成一个迭代器，从前往后循环删除列表元素时，每一次删除都会导致列表其他元素往前移，而索引i在不断增大，结果会导致跳过了某些元素或者index out of range。
正确删除可采用从后往前遍历删除或者列表解析、filter等。
'''
def func3():
	a = [10,20,30,40]
	for i in a:
		if i > 10:
			a.remove(i)
	print(a)

def func4():
	a = [10,20,30,40]
	for i in xrange(len(a)-1,-1,-1):
		if a[i] > 10:
			a.remove(a[i])
	print(a)

if __name__ == '__main__':
	print '==================='
	func3()  #[10, 30]
	func4()  #[10]
