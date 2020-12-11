# Recast Notes

> 以 solomesh 为例

## 预准备
- `Recast/include/Recast.h` 中的 `struct rcConfig`，即生成navmesh时面板上输入的参数
```c++
/// Specifies a configuration to use when performing Recast builds.
/// @ingroup recast
struct rcConfig
{
	/// The width of the field along the x-axis. [Limit: >= 0] [Units: vx]
	int width;

	/// The height of the field along the z-axis. [Limit: >= 0] [Units: vx]
	int height;

	/// The width/height size of tile's on the xz-plane. [Limit: >= 0] [Units: vx]
	int tileSize;

	/// The size of the non-navigable border around the heightfield. [Limit: >=0] [Units: vx]
	int borderSize;

	/// The xz-plane cell size to use for fields. [Limit: > 0] [Units: wu]
	float cs;

	/// The y-axis cell size to use for fields. [Limit: > 0] [Units: wu]
	float ch;

	/// The minimum bounds of the field's AABB. [(x, y, z)] [Units: wu]
	float bmin[3];

	/// The maximum bounds of the field's AABB. [(x, y, z)] [Units: wu]
	float bmax[3];

	/// The maximum slope that is considered walkable. [Limits: 0 <= value < 90] [Units: Degrees]
	float walkableSlopeAngle;

	/// Minimum floor to 'ceiling' height that will still allow the floor area to
	/// be considered walkable. [Limit: >= 3] [Units: vx]
	int walkableHeight;

	/// Maximum ledge height that is considered to still be traversable. [Limit: >=0] [Units: vx]
	int walkableClimb;

	/// The distance to erode/shrink the walkable area of the heightfield away from
	/// obstructions.  [Limit: >=0] [Units: vx]
	int walkableRadius;

	/// The maximum allowed length for contour edges along the border of the mesh. [Limit: >=0] [Units: vx]
	int maxEdgeLen;

	/// The maximum distance a simplfied contour's border edges should deviate
	/// the original raw contour. [Limit: >=0] [Units: vx]
	float maxSimplificationError;

	/// The minimum number of cells allowed to form isolated island areas. [Limit: >=0] [Units: vx]
	int minRegionArea;

	/// Any regions with a span count smaller than this value will, if possible,
	/// be merged with larger regions. [Limit: >=0] [Units: vx]
	int mergeRegionArea;

	/// The maximum number of vertices allowed for polygons generated during the
	/// contour to polygon conversion process. [Limit: >= 3]
	int maxVertsPerPoly;

	/// Sets the sampling distance to use when generating the detail mesh.
	/// (For height detail only.) [Limits: 0 or >= 0.9] [Units: wu]
	float detailSampleDist;

	/// The maximum distance the detail mesh surface should deviate from heightfield
	/// data. (For height detail only.) [Limit: >=0] [Units: wu]
	float detailSampleMaxError;
};
```

- `RecastDemo/include/Sample.h` 中 `class Sample` 的 `virtual bool handleBuild()` 方法，主要就是生成navmesh的流程

- 如何理解体素？
- 从数据结构上来理解也许非常简单。

- 一般模型存储的是顶点和面等数据，每个顶点在无限空间的任意一个位置。而体素空间是一个有限空间，包含了width*depth*height个体素，每个体素大小是固定的，在Recast中由CellSize和CellHeight决定。可想象一个魔方，每一块大小为cellSize*cellHeight，一共有width*height*depth大小。

- 体素化的过程就是求得模型的包围盒，在xz轴上以CellSize划分，在y轴上以CellHeight划分，得到一个[x][z][y]体素数组，再根据这个体素是否包含原模型的面，决定这个体素是实心还是空心，可行走还是不可行走等属性。

## 生成导航网格
- Recast部分的功能就是生成整个导航网格，其核心方法是 Sample_SoloMesh::handleBuild
- `class Sample_SoloMesh` 是 头文件`Sample.h` 中的 `class Sample` 的实现
- 这个函数注释非常友好地揭露了生成整个NavMesh导航网格的8个步骤，分别是：
	- Step 1. Initialize build config
	- Step 2. Rasterize input polygon soup
	- Step 3. Filter walkables surfaces
	- Step 4. Partition walkable surface to simple regions
	- Step 5. Trace and simplify region contours
	- Step 6. Build polygons mesh from contours
	- Step 7. Create detail mesh which allows to access approximate height on each polygon
	- Step 8. Create Detour data from Recast poly mesh


## 读取obj文件
- `InputGeom.cpp` 中 `InputGeom::load` 方法将读取obj文件中的内容，其实上工作的函数是 `loadMesh` 方法
	- RecastDemo 中 `InputGeom.h` 中的 `class InputGeom` 中包含了 `class rcMeshLoaderObj` 对象（位于 `MeshLoaderObj.h` 中）
	- `class rcMeshLoaderObj` 是真正读取 obj 文件的数据结构，它的成员变量中存储了顶点的坐标索引等信息
	- 最终调用的是 `rcMeshLoaderObj::load(const std::string& filename)` 去读取obj文件
	- 它读取了文件每一行，对v开头的调用了addVertext，对f开头的调用了addTriangle。其他的忽略。即读取了顶点和面数据。

```c++
class Sample
{
	class InputGeom* m_geom; // 用于存放读取的obj文件的内容
	float m_meshBMin[3], m_meshBMax[3]; // 最小x,y,z构成的一个点 & 最大x,y,z构成的一个点
}

class InputGeom
{
	rcMeshLoaderObj* m_mesh;
}

class rcMeshLoaderObj
{
	std::string m_filename; // obj 文件的路径
	float m_scale;
	float* m_verts; // 顶点坐标列表
	int* m_tris;  // 面的顶点索引列表
	float* m_normals;
	int m_vertCount; // 顶点数
	int m_triCount; // 面数
};
```

## 开始build
- 点击gui面板上的build，开始构建navmesh，实际上就是调用 sample->handlebuild()
- 例如 `RecastDemo/src/Sample_SoloMesh.cpp` 的 `handleBuild` 方法
- 首先会调用 `m_geom.getMesh()` 方法，将obj文件读取到 `m_geom`（`class InputGeom*` 结构体）中
- 然后从 `m_geom` 中拿到场景obj文件的相关信息
	```c++
	// 读取场景obj文件信息
	const float* bmin = m_geom->getNavMeshBoundsMin();
	const float* bmax = m_geom->getNavMeshBoundsMax();
	const float* verts = m_geom->getMesh()->getVerts();
	const int nverts = m_geom->getMesh()->getVertCount();
	const int* tris = m_geom->getMesh()->getTris();
	const int ntris = m_geom->getMesh()->getTriCount();
	```
- 读取好场景文件之后，再进行上文说的八个步骤

### step1: 将编辑器中的数据
```c++
m_cfg.cs = m_cellSize; // 体素的长和宽
m_cfg.ch = m_cellHeight; // 体素高度
m_cfg.walkableSlopeAngle = m_agentMaxSlope; // ageng 最大爬坡角度
m_cfg.walkableHeight = (int)ceilf(m_agentHeight / m_cfg.ch); // agent 高度
m_cfg.walkableClimb = (int)floorf(m_agentMaxClimb / m_cfg.ch); //agent 最大爬台阶高度
m_cfg.walkableRadius = (int)ceilf(m_agentRadius / m_cfg.cs); // agent 半径
m_cfg.maxEdgeLen = (int)(m_edgeMaxLen / m_cellSize); // step6: 多边形的最大边长，超过这个边长的会被拆分
m_cfg.maxSimplificationError = m_edgeMaxError; // step6: 将模型外轮廓构建成简单多边形中，点距离边的最大长度，如果该点距离变长度超过这个值，则该点与变的两个顶点分别相连，形成两条新边，替换原边。
m_cfg.minRegionArea = (int)rcSqr(m_regionMinSize);		// Note: area = size*size  step4: 构建area时，area的最小大小，小于这个值将会被合并
m_cfg.mergeRegionArea = (int)rcSqr(m_regionMergeSize);	// Note: area = size*size
m_cfg.maxVertsPerPoly = (int)m_vertsPerPoly; // step6: 构建简单多边形时，多边形最大的顶点数，大于这个值的多边形将会被拆分
m_cfg.detailSampleDist = m_detailSampleDist < 0.9f ? 0 : m_cellSize * m_detailSampleDist; // step7: 简单多边形形成精确模型时，采样点的距离
m_cfg.detailSampleMaxError = m_cellHeight * m_detailSampleMaxError; //  step7: 简单多边形和实际模型在采样点的最大误差，超过这个误差将给多边形增加新的顶点
```

### 光栅化所有的面，生成实心高度场
- 光栅化所有的面，生成实心高度场，主要有4个函数。
- 这一步还分配了一个跟面数相同的单字节数组 `geom.m_triareas = new unsigned char[ntris]`，用于保存每个面的可行走标记。

```c++
// Sample_SoleMesh.cpp->HandleBuild()
// line: 393~406
// Step 2. Rasterize input polygon soup.

// 略：内存分配&初始化
...

[1]   m_solid = rcAllocHeightfield();
[2]   rcCreateHeightfield(m_ctx, *m_solid, m_cfg.width, m_cfg.height, m_cfg.bmin, m_cfg.bmax, m_cfg.cs, m_cfg.ch))
      m_triareas = new unsigned char[ntris];
[3]   rcMarkWalkableTriangles(m_ctx, m_cfg.walkableSlopeAngle, verts, nverts, tris, ntris, m_triareas);
[4]   rcRasterizeTriangles(m_ctx, verts, nverts, tris, m_triareas, ntris, *m_solid, m_cfg.walkableClimb)
```

#### [1]rcAllocHeightfield()
- 分配了solid = rcHeightfield()实心高度场对象，这个对象后来以solid或hf命名出现。
- 前面6项是高度场的空间结构
- 后面两项是实心柱rcSpan对象池，用于构建过程中减少内存分配。中间的spans即前文提到的实心柱链表结构，也是核心数据
- 注释中可以看到，其大小为width*height。每一项包含了该坐标处实心柱rcSpan对象链表。
```c++
struct rcHeightfield
{
	rcHeightfield();
	~rcHeightfield();

	int width;			///< The width of the heightfield. (Along the x-axis in cell units.)
	int height;			///< The height of the heightfield. (Along the z-axis in cell units.)
	float bmin[3];  	///< The minimum bounds in world space. [(x, y, z)]
	float bmax[3];		///< The maximum bounds in world space. [(x, y, z)]
	float cs;			///< The size of each cell. (On the xz-plane.)
	float ch;			///< The height of each cell. (The minimum increment along the y-axis.)
	rcSpan** spans;		///< Heightfield of spans (width*height). 实心柱链表结构(核心数据，其大小为width*height，每一项包含了该坐标处实心柱rcSpan对象链表)
	rcSpanPool* pools;	///< Linked list of span pools.
	rcSpan* freelist;	///< The next free span.
}
```

#### [2]rcCreateHeightfield(m_ctx, width, hegiht, bmin, bmax, cs, ch)
```c++
// m_solid 就是前面申请的用于存储体素空间的数据结构
rcCreateHeightfield(m_ctx, *m_solid, m_cfg.width, m_cfg.height, m_cfg.bmin, m_cfg.bmax, m_cfg.cs, m_cfg.ch))
m_triareas = new unsigned char[ntris];
```

- 为 `geom.solid.spans` 分配了 width*height*sizeof(rcSpan) 的空间，并从geom传入了前6项空间结构的参数，并赋值于rcHeightField geom.solid.

```c++
/// @par
///
/// See the #rcConfig documentation for more information on the configuration parameters.
///
/// @see rcAllocHeightfield, rcHeightfield
bool rcCreateHeightfield(rcContext* ctx, rcHeightfield& hf, int width, int height,
						 const float* bmin, const float* bmax,
						 float cs, float ch)
{
	rcIgnoreUnused(ctx);

	hf.width = width;
	hf.height = height;
	rcVcopy(hf.bmin, bmin);
	rcVcopy(hf.bmax, bmax);
	hf.cs = cs;
	hf.ch = ch;
	hf.spans = (rcSpan**)rcAlloc(sizeof(rcSpan*)*hf.width*hf.height, RC_ALLOC_PERM);
	if (!hf.spans)
		return false;
	memset(hf.spans, 0, sizeof(rcSpan*)*hf.width*hf.height);
	return true;
}
```

#### [3]rcMarkWalkableTriangles()
- 标记出可走的面，其原理为检查面的倾斜角度是否小于 m_cfg.walkableSlopeAngle。
- 其方法是计算m_cfg.walkableSlopeAngle对应的cos值Thr，若这个面的标准化的法线y值大于Thr则标记为可行走。
- PS：area参数即sample.m_triareas。

```c++
/// @par
///
/// Only sets the area id's for the walkable triangles.  Does not alter the
/// area id's for unwalkable triangles.
///
/// See the #rcConfig documentation for more information on the configuration parameters.
///
/// @see rcHeightfield, rcClearUnwalkableTriangles, rcRasterizeTriangles
void rcMarkWalkableTriangles(rcContext* ctx, const float walkableSlopeAngle,
	const float* verts, int nv,
	const int* tris, int nt,
	unsigned char* areas)
{
	rcIgnoreUnused(ctx);
	rcIgnoreUnused(nv);

	// walkableSlopeAngle 计算最大爬坡角度的cos值
	const float walkableThr = cosf(walkableSlopeAngle / 180.0f * RC_PI);

	float norm[3];

	for (int i = 0; i < nt; ++i)
	{
		const int* tri = &tris[i * 3];
		calcTriNormal(&verts[tri[0] * 3], &verts[tri[1] * 3], &verts[tri[2] * 3], norm);
		// Check if the face is walkable.
		if (norm[1] > walkableThr)
			// 法线y值是否大于 walkableThr
			areas[i] = RC_WALKABLE_AREA;
	}
}
```
- 其结果保存在sample.m_triareas中。枚举声明如下：

> static const unsigned char RC_WALKABLE_AREA = 63;

#### [4]!!rcRasterizeTriangles()
- 他将完成体素化，即将顶点和面数据，转化成体素数据。
- 可以看到，遍历了模型的每一个面，对每一个面都构造rasterizeTri()，该函数对每一个三角面进行了光栅化。
- 最后一个参数 `flagMergeThr` 为 `m_cfg.walkableClimb`，即最大爬坡高度，用于判断体素间是否能合并。
```c++
/// @par
///
/// Spans will only be added for triangles that overlap the heightfield grid.
///
/// @see rcHeightfield
bool rcRasterizeTriangles(rcContext* ctx, const float* verts, const int /*nv*/,
						  const int* tris, const unsigned char* areas, const int nt,
						  rcHeightfield& solid, const int flagMergeThr)
{
	rcAssert(ctx);

	rcScopedTimer timer(ctx, RC_TIMER_RASTERIZE_TRIANGLES);

	const float ics = 1.0f/solid.cs;
	const float ich = 1.0f/solid.ch;
	// Rasterize triangles.
	for (int i = 0; i < nt; ++i)
	{
		const float* v0 = &verts[tris[i*3+0]*3];
		const float* v1 = &verts[tris[i*3+1]*3];
		const float* v2 = &verts[tris[i*3+2]*3];
		// Rasterize.
		if (!rasterizeTri(v0, v1, v2, areas[i], solid, solid.bmin, solid.bmax, solid.cs, ics, ich, flagMergeThr))
		{
			ctx->log(RC_LOG_ERROR, "rcRasterizeTriangles: Out of memory.");
			return false;
		}
	}

	return true;
}
```