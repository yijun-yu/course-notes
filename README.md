# 课程讲义 · Course Notes

各门课程讲义的总入口：题型讲义、课程笔记、学习心得。目前已有题型讲义的题目页。

在线访问：https://yijun-yu.github.io/course-notes/

首页是一个按「辑」分层的书架，每门课一本书；点进去是该课程的章目录，再点进去是题目页。旧版入口页（深色毛玻璃卡片）保存在分支 `v1-glass`：`git checkout v1-glass`。

## 目录结构

```
content/site.json              站点标题与「辑」的名称
content/<课程>/course.json     课程信息：所属辑、卷号、名称、颜色、书脊尺寸、书脊图案、章节列表
content/<课程>/<章>.md         题目原文（Astra 输出的题目块，一章一个文件）
index.html                     首页书架（生成）
<课程>/index.html              章目录（生成）
<课程>/<章>.html               题目页（生成）
assets/                        通用样式、脚本、KaTeX、字体
tools/build.py                 构建脚本
tools/index.template.html      首页模板
```

`index.html`、`<课程>/` 下的页面都是生成的，不要手工修改。

## 日常操作

在仓库根目录运行：

```bash
python3 -I tools/build.py .
```

- **追加或修改题目**：把 Astra 的输出追加到 `content/<课程>/<章>.md`，重新构建即可。
- **新增一门课**：复制一份 `content/<课程>/course.json` 到新目录，修改下面这些字段，重新构建，首页书架和课程目录页会自动出现。
  - `order`：全局卷序（决定「卷几」的顺序）
  - `series`：属于第几辑（`content/site.json` 里定义各辑的名称；需要新开一辑就在那里加一项）
  - `volume`、`title`、`en`：卷号、中文名、英文名
  - `color`：书布色 `[r, g, b]`，课程页的强调色也取自这里
  - `spine`：书脊的宽和高（像素）
  - `glyph`：书脊底部的线描图案（40×40 的 SVG 内部代码）
  - `light`：浅色书脊填 `true`，文字会改用深色
  - `chapters`：章节列表，`id` 与 `content/<课程>/<章>.md` 的文件名对应
- 「待续」位置总是放在最后一辑的末尾。

## 构建依赖

Python 3、`fonttools`、Node.js（用于 KaTeX 预渲染；脚本优先使用 `node_modules` 中的 KaTeX，否则读环境变量 `KATEX_PATH`）。字体用 Noto Serif CJK（宋体）、Inter、TeX Gyre Pagella，均为免费开源。

`build_fonts.py` 是早期手动打包首页字体的脚本，现在这一步已由 `tools/build.py` 自动完成，可以忽略。
