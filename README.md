# 课程题型讲义 · Course Notes

各门课程题型讲义的总入口页。

在线访问：https://yijun-yu.github.io/course-notes/

## 文件

- `index.html`：入口页，单文件、无外部依赖（字体已截取子集内嵌）
- `build_fonts.py`：字体打包脚本

## 新增课程

1. 在 `index.html` 里复制一张卡片，改课程名、链接和颜色变量（`--c1` / `--c2`）。
2. 重新内嵌字体（新课程名里可能有新的汉字）：

   ```bash
   pip install fonttools
   python3 build_fonts.py index.html \
     --serif-sc NotoSerifSC-Medium.otf \
     --sans Inter-Regular.otf \
     --italic texgyrepagella-italic.otf
   ```

   字体均为免费开源：Noto Serif SC、Inter（Google Fonts），TeX Gyre Pagella（CTAN）。

## 子页面

卡片默认链接到 `./<课程目录>/index.html`，例如 `./complex-analysis/index.html`。
在仓库里建同名文件夹放入各课程页面即可。
