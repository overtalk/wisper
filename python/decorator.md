## property 装饰器
- 建议属性值设置为私有，那么如果想访问属性可以通过属性的getter（访问器）和setter（修改器）方法进行对应的操作
```python
class person(object):
	def __init__(self, name, age):
		print "__init__ is called"
		self.__age = age
		self.__name = name
		pass

	@property
	def age(self):
		return self.__age

	@age.setter
	def age(self, age):
		self.__age = age
```

## 装饰器
- [CSDN](https://blog.csdn.net/u013858731/article/details/54971762?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-1.edu_weight&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-1.edu_weight)


