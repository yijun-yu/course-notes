# 课程题型讲义 · Course Notes

各门课程题型讲义的总入口页。

在线访问：https://yijun-yu.github.io/course-notes/

## 文件

- `index.html`：入口页，单文件、无外部依赖（字体已截取子集内嵌）
- `build_fonts.py`：字体打包脚本

## 新增课程

1. 在 `index.html` 里复制一本书（`<a class="book …">`），改「卷几」、课程名、英文名、链接和书脊尺寸（`--w` / `--h`），再给它一个书布色类（参照 `.c-complex` 等，颜色写在 `--c` 里）。
2. 书脊底部的 `<svg class="glyph">` 是这门课的线描符号，换成和新课程相关的图形。
3. 重新内嵌字体（新课程名里可能有新的汉字）：

   ```bash
   pip install fonttools
   python3 build_fonts.py index.html \
     --serif-sc NotoSerifCJK-Medium.ttc --serif-sc-index 2 \
     --sans Inter-Regular.otf \
     --italic texgyrepagella-italic.otf
   ```

   字体均为免费开源：Noto Serif CJK / Noto Serif SC、Inter（Google Fonts），TeX Gyre Pagella（CTAN）。也可以直接用 `NotoSerifSC-Medium.otf`，不需要 `--serif-sc-index`。

旧版（深色毛玻璃卡片）保存在分支 `v1-glass`：`git checkout v1-glass`。

## 题目页（每门课通用）

```
content/<课程>/course.json   课程名、卷号、颜色、章节列表
content/<课程>/<章>.md       题目原文（Astra 输出的题目块，一章一个文件）
<课程>/index.html            章目录（生成）
<课程>/<章>.html             题目页（生成）
assets/                      通用样式、脚本、KaTeX、字体
tools/build.py               构建脚本
```

- 题目页默认只显示题目；答案、思路点击展开；可按档次筛选、按题型分组、标记已做、一键复制题目（含 LaTeX 源码）、打印。
- 公式在构建时用 KaTeX 预渲染，页面不依赖任何外部网络资源。
- 新增或修改题目：把 Astra 的输出追加到 `content/<课程>/<章>.md`，然后在仓库根目录运行：

  ```bash
  python3 -I tools/build.py .
  ```

  需要 Python 3、`fonttools` 和 Node.js（构建用到 KaTeX，脚本会优先用 `node_modules` 里的，否则用环境变量 `KATEX_PATH` 指向的那一份）。
- 新增一门课：复制 `content/complex-analysis/course.json` 改成新课程，再在入口页 `index.html` 的卡片里确认链接目录名一致即可，页面样式通用，颜色由 `course.json` 里的 `color` 决定。

## 子页面

入口页的卡片链接到 `./<课程目录>/index.html`，这些页面由上面的构建脚本生成。
