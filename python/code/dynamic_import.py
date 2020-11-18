# -*- coding: utf-8 -*-

# 动态加载一个模块

import sys

def loadModule(module_name):
	try:
		module = sys.modules.get(module_name)
		if not module:
			__import__(module_name)
			module = sys.modules[module_name]
		return module
	except Exception as e:
		print '[BT] load ai fail, ai_module(%s), error(%s)' % (module_name, e)

if __name__ == '__main__':
	m = loadModule('test.test_module')
	m.test()