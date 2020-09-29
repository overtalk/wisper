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