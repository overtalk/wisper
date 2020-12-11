# -*- coding: utf-8 -*-

# python 中 __init__ 和 __new__ 方法的区别

class A(object):
	def __init__(self):
		print("__init__ ")
		print(self)
		super(A, self).__init__()

	def __new__(cls):
		print("__new__ ")
		self = super(A, cls).__new__(cls)
		print(self)
		return self

a = A()
print callable(a)