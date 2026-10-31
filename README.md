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

旧版（深色毛玻璃卡片）保存在标签 `v1-glass`：`git checkout v1-glass`。

## 子页面

卡片默认链接到 `./<课程目录>/index.html`，例如 `./complex-analysis/index.html`。
在仓库里建同名文件夹放入各课程页面即可。
