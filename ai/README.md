# 游戏中AI的

## 关键技术
1. 寻路 Path Finding
	- A*算法  基于网格tile  基于Navigation Mesh
	- 贪心策略  拟人化寻路
	- 群体寻路

2. 感知
	- Environment Query System (EQS)
	- 视觉 听觉 躲避点

3. 反馈机制
	- 事件

4. Black Board 黑板
	- 共享数据，数据生命期管理，集中式输入管理
	- 增删改查
	- AI的内存数据库

5. Tick激活和分帧

## 主流设计方法-行为树
1. 控制节点
	- 选择节点 Selector Node
	- 顺序节点 Sequence Node
	- 并行节点 Parallel Node

2. 条件节点 Condition Node

3. 动作节点 Action Node

4. 节点返回：Success，Running，Fail
