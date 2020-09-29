# -*- coding: utf-8 -*-

class Person(object):
	def __init__(self):
		self._name = 'name'

	@property
	def name(self):
		return self._name

	@name.setter
	def name(self, name):
		self._name = name

if __name__ == '__main__':
	p = Person()
	p.name = 'test'
	print p.name