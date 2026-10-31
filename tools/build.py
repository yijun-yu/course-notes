#!/usr/bin/env python3
"""题目页构建脚本。

输入：content/<课程>/course.json，以及同目录下的 <章>.md（Astra 输出的题目块）
输出：<课程>/index.html（章目录）、<课程>/<章>.html（题目页）、assets/fonts 下的字体子集
公式在构建时用 KaTeX 预渲染，页面不依赖任何外部资源。

用法：python3 -I tools/build.py <仓库根目录>
"""
import base64
import html
import io
import json
import pathlib
import re
import subprocess
import sys
from string import Template

ROOT = pathlib.Path(sys.argv[1]).resolve()
TOOLS = pathlib.Path(__file__).resolve().parent
CONTENT = ROOT / 'content'
WARNINGS = []


def warn(msg):
    WARNINGS.append(msg)
    print('警告：' + msg, file=sys.stderr)


def esc(s):
    return html.escape(s, quote=True)


# ------------------------------------------------------------------ 公式登记
class Maths:
    """先把公式登记成占位符，最后统一交给 KaTeX 批量渲染。"""

    def __init__(self):
        self.items = []
        self.index = {}

    def add(self, tex, display):
        k = (tex, display)
        if k not in self.index:
            self.index[k] = len(self.items)
            self.items.append(k)
        return self.index[k]

    def is_display(self, i):
        return self.items[i][1]


M = Maths()
PH = re.compile('\u0001(\\d+)\u0002')


def is_cjk(ch):
    return '一' <= ch <= '鿿' or ch in '，。、；：？！（）「」『』《》…—'


def join_lines(lines):
    out = lines[0]
    for ln in lines[1:]:
        out += ('' if (is_cjk(out[-1]) or is_cjk(ln[0])) else ' ') + ln
    return out


def render_text(s):
    """Markdown 片段 → HTML（含公式占位符）。支持段落、$..$、$$..$$、**粗体**、「1. 」有序列表。"""
    s = re.sub(r'\$\$(.+?)\$\$', lambda m: '\u0001%d\u0002' % M.add(m.group(1).strip(), True), s, flags=re.S)
    s = re.sub(r'\$((?:[^$\n]|\n(?!\s*\n))+?)\$',
               lambda m: '\u0001%d\u0002' % M.add(m.group(1).strip(), False), s)
    s = html.escape(s, quote=False)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)

    out, para, items = [], [], []

    def flush_para():
        nonlocal para
        if para:
            out.append('<p>' + join_lines(para) + '</p>')
            para = []

    def flush_list():
        nonlocal items
        if items:
            out.append('<ol>' + ''.join('<li>%s</li>' % x for x in items) + '</ol>')
            items = []

    for line in s.split('\n'):
        t = line.strip()
        if not t:
            flush_para()
            flush_list()
            continue
        if any(M.is_display(int(i)) for i in PH.findall(t)):
            flush_list()
            for part in re.split('(\u0001\\d+\u0002)', t):
                if not part:
                    continue
                m = re.fullmatch('\u0001(\\d+)\u0002', part)
                if m and M.is_display(int(m.group(1))):
                    flush_para()
                    out.append('<div class="disp">%s</div>' % part)
                else:
                    para.append(part)
            continue
        mol = re.match(r'^\d+\.\s+(.*)$', t)
        if mol:
            flush_para()
            items.append(mol.group(1))
        else:
            flush_list()
            para.append(t)
    flush_para()
    flush_list()
    return '\n'.join(out)


# ------------------------------------------------------------------ 解析题目块
def parse_chapter(path):
    text = path.read_text(encoding='utf8').replace('\r\n', '\n')
    probs = []
    seen = set()
    for raw in re.split(r'(?m)^[ \t]*---[ \t]*$', text):
        raw = raw.strip()
        if not raw:
            continue
        lines = raw.split('\n')
        m = re.match(r'^###\s+(\S+)\s*(.*)$', lines[0].strip())
        if not m:
            warn('%s：块首行不是「### 编号」，已跳过：%s' % (path.name, lines[0][:30]))
            continue
        pid, rest = m.group(1), m.group(2)
        meta, secs, cur, buf = {}, {}, None, []
        for ln in lines[1:]:
            ms = re.match(r'^\*\*(题目|答案|思路|自检)\*\*\s*$', ln.strip())
            if ms:
                if cur:
                    secs[cur] = '\n'.join(buf).strip()
                cur, buf = ms.group(1), []
                continue
            if cur is None:
                mm = re.match(r'^-\s*(.+?)[：:]\s*(.*)$', ln.strip())
                if mm:
                    meta[mm.group(1)] = mm.group(2).strip()
            else:
                buf.append(ln)
        if cur:
            secs[cur] = '\n'.join(buf).strip()
        for need in ('题目', '答案'):
            if not secs.get(need):
                warn('%s：%s 缺少「%s」' % (path.name, pid, need))
        if pid in seen:
            warn('%s：编号重复 %s' % (path.name, pid))
        seen.add(pid)
        tname = meta.get('题型', '')
        mt = re.match(r'^(\d+-\S+)\s+(.*)$', tname)
        probs.append({
            'id': pid,
            'type': pid.rsplit('-', 1)[0],
            'type_name': mt.group(2) if mt else tname,
            'tier': meta.get('档次', ''),
            'ext': meta.get('标记', '') == '拓展',
            'check': '待核验' in rest,
            'stmt': secs.get('题目', ''),
            'ans': secs.get('答案', ''),
            'idea': secs.get('思路', ''),
        })
    return probs


# ------------------------------------------------------------------ 页面
PAGE = Template('''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${title}</title>
<meta name="description" content="${desc}">
<link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="../assets/katex/katex.min.css">
<link rel="stylesheet" href="../assets/site.css">
<style>:root{--c:${c};--ca:${ca}}</style>
<script defer src="../assets/site.js"></script>
</head>
<body class="${bodyclass}" data-course="${course}" data-chapter="${chapter}">
<div class="wrap">
${inner}
</div>
</body>
</html>
''')


def lighten(rgb, k=0.55):
    return [round(v + (255 - v) * k) for v in rgb]


def problem_html(p, n):
    ext = ' data-ext="1"' if p['ext'] else ''
    flag = '<span class="flag">待核验</span>' if p['check'] else ''
    idea = ''
    if p['idea']:
        idea = ('<details class="idea"><summary>思路</summary><div class="idea-body">%s</div></details>'
                % render_text(p['idea']))
    return (
        '<article class="prob" id="q{n}" data-id="{id}" data-type="{type}" data-tier="{tier}"{ext}>\n'
        '<div class="mark"><button class="done" type="button" aria-pressed="false" aria-label="标记第 {n} 题已完成"></button></div>\n'
        '<div class="main">\n'
        '<div class="qhead"><span class="num">{n}</span>{flag}'
        '<button class="copy" type="button" title="复制题目（含 LaTeX 源码），可直接粘贴给 AI">复制</button></div>\n'
        '<div class="stmt">{stmt}</div>\n'
        '<script type="text/plain" class="src">{src}</script>\n'
        '<details class="ans"><summary>答案</summary>\n'
        '<div class="ans-body">{ans}</div>\n{idea}\n</details>\n'
        '</div>\n</article>'
    ).format(n=n, id=esc(p['id']), type=esc(p['type']), tier=esc(p['tier']), ext=ext, flag=flag,
             stmt=render_text(p['stmt']), src=p['stmt'].replace('</', '<\\/'), ans=render_text(p['ans']), idea=idea)


def toolbar_html(probs):
    tiers = [t for t in ('基础', '典型', '进阶') if any(p['tier'] == t for p in probs)]
    b = ['<div class="bar" role="toolbar" aria-label="显示选项">',
         '<div class="seg" role="group" aria-label="档次">'
         '<button type="button" data-tier="" aria-pressed="true">全部</button>'
         + ''.join('<button type="button" data-tier="%s" aria-pressed="false">%s</button>' % (t, t) for t in tiers)
         + '</div>']
    if any(p['ext'] for p in probs):
        b.append('<label class="chk"><input type="checkbox" id="opt-ext" checked><span>拓展</span></label>')
    b.append('<label class="chk"><input type="checkbox" id="opt-bytype"><span>按题型</span></label>')
    b.append('<label class="chk"><input type="checkbox" id="opt-allans"><span>全部答案</span></label>')
    b.append('<span class="sp"></span><span class="prog" id="prog" aria-live="polite"></span>'
             '<button type="button" class="btn" id="btn-print">打印</button></div>')
    return '\n'.join(b)


def chapter_page(course, ch, probs, prev_ch, next_ch):
    items, last_type = [], None
    for n, p in enumerate(probs, 1):
        if p['type'] != last_type:
            items.append('<h2 class="type-head" data-type="%s"><span class="tid">%s</span><span>%s</span>'
                         '<span class="tier">%s</span></h2>'
                         % (esc(p['type']), esc(p['type']), esc(p['type_name']), esc(p['tier'])))
            last_type = p['type']
        items.append(problem_html(p, n))
    left = '<a href="./">← 目录</a>'
    right = ('<a href="%s.html">%s %s →</a>' % (next_ch['id'], esc(next_ch['no']), esc(next_ch['title']))
             if next_ch else '<span></span>')
    inner = (
        '<nav class="crumb"><a href="../">课程题型讲义</a><span>/</span><a href="./">%s</a></nav>\n'
        '<header class="head"><p class="kicker">%s</p><h1>%s</h1><p class="count">%d 题</p></header>\n'
        '%s\n<main class="list" id="list">\n%s\n</main>\n<footer class="pager">%s%s</footer>'
        % (esc(course['title']), esc(ch['no']), esc(ch['title']), len(probs), toolbar_html(probs),
           '\n'.join(items), left, right))
    return PAGE.substitute(
        title='%s %s · %s' % (ch['no'], ch['title'], course['title']),
        desc='%s %s %s，共 %d 题。' % (course['title'], ch['no'], ch['title'], len(probs)),
        c=' '.join(map(str, course['color'])), ca=' '.join(map(str, lighten(course['color']))),
        bodyclass='chapter', course=course['id'], chapter=ch['id'], inner=inner)


def course_page(course, counts):
    rows = []
    for ch in course['chapters']:
        n = counts.get(ch['id'])
        head = '<span class="no">%s</span><span class="t">%s</span><span class="dots"></span>' % (
            esc(ch['no']), esc(ch['title']))
        if n:
            rows.append('<li><a href="%s.html">%s<span class="n">%d 题</span></a></li>' % (ch['id'], head, n))
        else:
            rows.append('<li class="soon"><div class="row">%s<span class="n">待续</span></div></li>' % head)
    total = sum(counts.values())
    inner = (
        '<nav class="crumb"><a href="../">课程题型讲义</a></nav>\n'
        '<header class="head"><p class="kicker">%s</p><h1>%s</h1><p class="en">%s</p>'
        '<p class="count">已收录 %d 题</p></header>\n<ol class="toc">\n%s\n</ol>'
        % (esc(course['volume']), esc(course['title']), esc(course['en']), total, '\n'.join(rows)))
    return PAGE.substitute(
        title='%s · 课程题型讲义' % course['title'],
        desc='%s 题型讲义目录。' % course['title'],
        c=' '.join(map(str, course['color'])), ca=' '.join(map(str, lighten(course['color']))),
        bodyclass='course', course=course['id'], chapter='index', inner=inner)


# ------------------------------------------------------------------ 公式渲染
def render_maths():
    if not M.items:
        return []
    payload = json.dumps([{'t': t, 'd': d} for t, d in M.items], ensure_ascii=False)
    r = subprocess.run(['node', str(TOOLS / 'katex_batch.js')], input=payload,
                       capture_output=True, text=True, encoding='utf8')
    if r.returncode != 0:
        sys.exit('KaTeX 渲染失败：\n' + r.stderr)
    res = json.loads(r.stdout)
    for (t, d), x in zip(M.items, res):
        if x['err']:
            warn('公式渲染出错：' + t[:80])
    return [x['html'] for x in res]


# ------------------------------------------------------------------ 字体
def ensure_latin_fonts():
    fonts = ROOT / 'assets' / 'fonts'
    fonts.mkdir(parents=True, exist_ok=True)
    src = (ROOT / 'index.html').read_text(encoding='utf8')
    for fam, name in (('Portal Sans', 'portal-sans.woff'), ('Portal Italic', 'portal-italic.woff')):
        p = fonts / name
        if p.exists():
            continue
        m = re.search(r'font-family:"%s".*?base64,([A-Za-z0-9+/=]+)\)' % fam, src, re.S)
        if m:
            p.write_bytes(base64.b64decode(m.group(1)))
        else:
            warn('入口页里找不到字体 ' + fam)


def build_serif_subset(strings):
    """标题用的宋体：只截取页面标题里出现的字，体积很小。"""
    candidates = ['/usr/share/fonts/opentype/noto/NotoSerifCJK-Medium.ttc']
    src = next((c for c in candidates if pathlib.Path(c).exists()), None)
    out = ROOT / 'assets' / 'fonts' / 'serif-sc.woff'
    if not src:
        warn('找不到 Noto Serif CJK，沿用已有的 serif-sc.woff')
        return
    from fontTools.subset import Options, Subsetter
    from fontTools.ttLib import TTCollection, TTFont
    idx = next(i for i, f in enumerate(TTCollection(src).fonts) if 'SC' in f['name'].getDebugName(1))
    text = ''.join(sorted(set(''.join(strings)))) + ''.join(chr(c) for c in range(0x20, 0x7F)) + '—·'
    font = TTFont(src, fontNumber=idx)
    opts = Options()
    opts.flavor = 'woff'
    opts.layout_features = ['kern', 'liga', 'tnum']
    opts.name_IDs = []
    sub = Subsetter(opts)
    sub.populate(text=text)
    sub.subset(font)
    font.flavor = 'woff'
    buf = io.BytesIO()
    font.save(buf)
    out.write_bytes(buf.getvalue())


# ------------------------------------------------------------------ 主流程
def main():
    pages = {}
    serif_text = ['课程题型讲义', '待续', '卷一二三四五六七八九十', '第章综合']
    summary = []
    for cfile in sorted(CONTENT.glob('*/course.json')):
        course = json.loads(cfile.read_text(encoding='utf8'))
        cdir = cfile.parent
        serif_text += [course['title'], course['volume']]
        chapters = course['chapters']
        data = {}
        for ch in chapters:
            serif_text += [ch['no'], ch['title']]
            f = cdir / (ch['id'] + '.md')
            if f.exists():
                data[ch['id']] = parse_chapter(f)
        avail = [ch for ch in chapters if ch['id'] in data]
        for i, ch in enumerate(avail):
            nxt = avail[i + 1] if i + 1 < len(avail) else None
            pages[ROOT / course['id'] / (ch['id'] + '.html')] = chapter_page(course, ch, data[ch['id']], None, nxt)
            tiers = {}
            for p in data[ch['id']]:
                tiers[p['tier']] = tiers.get(p['tier'], 0) + 1
            summary.append('%s %s：%d 题 %s' % (course['id'], ch['id'], len(data[ch['id']]), tiers))
        pages[ROOT / course['id'] / 'index.html'] = course_page(course, {k: len(v) for k, v in data.items()})

    rendered = render_maths()
    for path, page in pages.items():
        page = PH.sub(lambda m: rendered[int(m.group(1))], page)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(page, encoding='utf8')

    ensure_latin_fonts()
    build_serif_subset(serif_text)
    print('\n'.join(summary))
    print('页面 %d 个，公式 %d 条，警告 %d 条' % (len(pages), len(M.items), len(WARNINGS)))


main()
