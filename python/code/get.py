# -*- coding: utf-8 -*-

class Kls(object):
	def __init__(self, a):
		super(Kls, self).__init__()
		self.a = a

	def func(self):
		print 'self'

	def __getattribute__(self, name):
		print 'in __getattribute__', name
		return super(Kls, self).__getattribute__(name)

	def __getattr__(self, name):
		print 'in __getattr__', name

k = Kls(1)
print k.a
print k.func
k.b = 'xxx'
print k.b
print k.__dict__