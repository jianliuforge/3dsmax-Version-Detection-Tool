# 3dsmax-Version-Detection-Tool

一个用于检测 3ds Max 文件的 Python 工具集，可以识别文件版本和几何信息，并判断是否符合目标要求。

## 功能特点

### check_max.py - 版本检测
- 读取 3ds Max 文件（.max）的版本信息
- 智能检测版本号（优先级：另存为版本 > 主版本 > 备用格式）
- 支持中英文版本标识（`另存为版本`/`saved as version`、`3ds max 版本`/`3ds max version`）
- 支持多种编码格式解析（UTF-8、UTF-16-LE、GBK、ASCII）
- 根据配置的目标版本自动判断兼容性
- 返回"通过"或"拒绝"状态

### check_vertices.py - 顶点数检测
- 读取 3ds Max 文件的顶点数信息
- 根据配置的顶点数限制自动判断
- 默认限制：100万顶点
- 返回"通过"或"拒绝"状态

### extract_geometry.py - 几何信息提取
- 提取完整的几何统计信息（顶点数、面数等）
- 仅用于信息查看，不做判断

## 安装依赖

```bash
pip install olefile
```

## 使用方法

### 1. 版本检测 (check_max.py)

修改配置：
- `MAX_FILE_PATH`: 设置要检测的 .max 文件路径
- `TARGET_MAJOR`: 设置目标支持的最高主版本号（例如：23 = 2021, 26 = 2024）

运行：
```bash
python check_max.py
```

### 2. 顶点数检测 (check_vertices.py)

修改配置：
- `MAX_FILE_PATH`: 设置要检测的 .max 文件路径
- `TARGET_VERTICES`: 设置顶点数限制（默认：1000000 = 100万）

运行：
```bash
python check_vertices.py
```

### 3. 几何信息提取 (extract_geometry.py)

修改配置：
- `MAX_FILE_PATH`: 设置要检测的 .max 文件路径

运行：
```bash
python extract_geometry.py
```

## 版本检测逻辑

脚本使用以下优先级顺序检测版本：

1. **另存为版本**（最高优先级）
   - 匹配模式：`另存为版本` 或 `saved as version`
   - 正则表达式：`(?:另存为版本|saved\s*as\s*version)[:\s]*(\d{2})`

2. **主版本**
   - 匹配模式：`3ds max 版本` 或 `3ds max version`
   - 正则表达式：`(?:3ds\s*max\s*版本|3ds\s*max\s*version)[:\s]*(\d{2})`

3. **备用格式**（最低优先级）
   - 匹配模式：`XX.XX` 格式的版本号
   - 正则表达式：`(\d{2})\.\d{2}`

## 版本对照表

| 版本号 | 3ds Max 版本 |
|--------|--------------|
| 23     | 2021         |
| 24     | 2022         |
| 25     | 2023         |
| 26     | 2024         |

## 输出说明

所有检测脚本的输出规则：
- **通过**: 文件符合要求，可以使用（退出码 0）
- **拒绝**: 文件不符合要求，不兼容（退出码 1）

### check_max.py 输出示例
```
检测到版本: 26
通过
```

### check_vertices.py 输出示例
```
检测到顶点数: 46,827
通过
```

### extract_geometry.py 输出示例
```
==================================================
文件: 2.max
==================================================
顶点数 (Vertices): 46827
三角面数 (Triangles): 未检测到
四边形数 (Quads): 未检测到
总面数 (Faces): 50247
==================================================
```

## 许可证

MIT License
