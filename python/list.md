# list 的相关操作

```python
list1 = [0, 1, 2, 3, 4, 5]

# 添加元素
list1.append(3)
list1.insert(3, 12) # 如果 index 超出了范围，则相当于 append

# 删除元素
del list1[3] # 如果越界，panic

print 3 in list1 # 某个元素是否在list中
```