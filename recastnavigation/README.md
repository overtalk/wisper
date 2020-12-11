# recastnavigation notes

> 源码 [github](https://github.com/recastnavigation/recastnavigation)

## 簡介
- 第一部分是Recast，主要功能是将场景网格模型生成用于寻路的网格模型NavMesh。所生成的网格模型比原模型简单的多，这也使得利用网格实时寻路可以满足性能要求。

- 第二部分是Detour，主要功能是利用上一步所生成的NavMesh进行寻路，其包含了多种查询接口和寻路算法，甚至包括一套完整的支持动态避让的多人寻路解决方案。



