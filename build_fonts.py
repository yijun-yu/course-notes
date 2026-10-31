#!/usr/bin/env python3
"""
把页面用到的字体「自带」进 index.html（截取子集 + base64 内嵌），国内网络也能正确显示。

用法：
    pip install fonttools
    python3 build_fonts.py index.html \
        --serif-sc  NotoSerifSC-Medium.otf      # 思源宋体 / Noto Serif SC（Medium）
        --sans      Inter-Regular.otf           # Inter
        --italic    texgyrepagella-italic.otf   # TeX Gyre Pagella Italic

新增课程（改了页面里的汉字）后重新运行一次即可。
脚本只改写 index.html 中 /* FONTS:BEGIN */ 与 /* FONTS:END */ 之间的内容。
--serif-sc 也可以传 .ttc 字体集合，用 --serif-sc-index 指定其中的简体中文字体序号。
"""
import argparse, base64, io, re, sys
from fontTools.ttLib import TTFont
from fontTools.subset import Subsetter, Options

LATIN = ''.join(chr(c) for c in range(0x20, 0x7F)) + '—–·∞’“”…'


def subset(path, text, index=0):
    font = TTFont(path, fontNumber=index)
    opts = Options()
    opts.flavor = 'woff'
    opts.layout_features = ['kern', 'liga', 'tnum', 'calt']
    opts.name_IDs = []
    opts.notdef_outline = True
    s = Subsetter(opts)
    s.populate(text=text)
    s.subset(font)
    buf = io.BytesIO()
    font.flavor = 'woff'
    font.save(buf)
    return base64.b64encode(buf.getvalue()).decode()


def face(family, b64, weight='400', style='normal'):
    return (f'  @font-face{{font-family:"{family}";font-style:{style};font-weight:{weight};font-display:swap;'
            f'src:url(data:font/woff;base64,{b64}) format("woff")}}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('html')
    ap.add_argument('--serif-sc', required=True)
    ap.add_argument('--serif-sc-index', type=int, default=0)
    ap.add_argument('--sans', required=True)
    ap.add_argument('--italic', required=True)
    a = ap.parse_args()

    html = open(a.html, encoding='utf-8').read()
    body = re.sub(r'<(script|style)\b.*?</\1>', '', html, flags=re.S)
    cjk = sorted(set(ch for ch in body if ord(ch) > 0x2E7F))
    cjk_text = ''.join(cjk) + '·'
    italic_text = ''.join(set(''.join(re.findall(r'class="en-title">([^<]*)<', html)))) or 'Course Notes'

    css = '\n'.join([
        face('Portal Serif SC', subset(a.serif_sc, cjk_text + LATIN, a.serif_sc_index), '400 600'),
        face('Portal Sans', subset(a.sans, LATIN)),
        face('Portal Italic', subset(a.italic, italic_text), '400', 'italic'),
    ])
    new, n = re.subn(r'/\* FONTS:BEGIN \*/.*?/\* FONTS:END \*/',
                     lambda m: '/* FONTS:BEGIN */\n' + css + '\n  /* FONTS:END */', html, flags=re.S)
    if not n:
        sys.exit('没找到 /* FONTS:BEGIN */ … /* FONTS:END */ 标记')
    open(a.html, 'w', encoding='utf-8').write(new)
    print(f'已嵌入 {len(cjk)} 个汉字；index.html 现在 {len(new.encode()) / 1024:.0f} KB')


if __name__ == '__main__':
    main()
