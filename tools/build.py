#!/usr/bin/env python3
"""题目页构建脚本。

输入：content/<课程>/course.json，以及同目录下的 <章>.md（Astra 输出的题目块）
输出：index.html（首页书架）、<课程>/index.html（章目录）、<课程>/<章>.html（题目页）、assets/fonts 下的字体子集
公式在构建时用 KaTeX 预渲染，页面不依赖任何外部资源。

用法：python3 -I tools/build.py <仓库根目录>
"""
import base64
import datetime
import html
import io
import json
import pathlib
import re
import subprocess
import sys
import urllib.parse
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


def render_inline(s):
    """行内文字（如题型名）：把 e^{iax} 这类写法当作公式，其余只做转义。"""
    # 先登记已经写在 $...$ 里的公式，再把剩下的 e^{iax} 之类裸写当作公式，避免二次包裹
    s = re.sub(r'\$([^$\n]+?)\$', lambda m: '\u0001%d\u0002' % M.add(m.group(1).strip(), False), s)
    s = re.sub(r'([A-Za-z]\^\{[^}]*\})', lambda m: '\u0001%d\u0002' % M.add(m.group(1), False), s)
    return html.escape(s, quote=False)


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
<link rel="stylesheet" href="../assets/site.css?v=${vcss}">
<style>:root{--c:${c};--ca:${ca}}</style>
<script defer src="../assets/site.js?v=${vjs}"></script>
<link rel="stylesheet" href="../assets/rail.css?v=${vrcss}">
<script defer src="../assets/search-index.js?v=${vidx}"></script>
<script defer src="../assets/rail.js?v=${vrjs}"></script>
</head>
<body class="${bodyclass}" data-course="${course}" data-chapter="${chapter}" data-root="../">
${rail}
<div class="wrap">
${inner}
</div>
\u0003FOOT\u0004
</body>
</html>
''')


def rail_html(root, path=''):
    """全站页眉：站名、所在位置、搜索。内页多一条阅读进度线。"""
    return ('<header class="rail"><div class="rail-in"><a class="rail-mark" href="%s">课程讲义</a>%s'
            '<button class="rail-find" type="button" aria-label="搜索（快捷键 /）"><span>搜索</span><kbd>/</kbd></button>'
            '%s</div></header>' % (root, '<nav class="rail-path" aria-label="当前位置">%s</nav>' % path if path else '',
                             '<div class="rail-line" aria-hidden="true"></div>' if path else ''))


def page_assets():
    return dict(vcss=asset_version('site.css'), vjs=asset_version('site.js'), vrcss=asset_version('rail.css'),
                vrjs=asset_version('rail.js'), vidx='\u0003IDX\u0004')


def asset_version(name):
    """静态文件内容的短哈希，加在链接后面，样式更新后浏览器不会继续用旧缓存。"""
    import hashlib
    return hashlib.sha1((ROOT / 'assets' / name).read_bytes()).hexdigest()[:8]


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
        '<div class="reveal">\n{idea}\n<details class="ans"><summary>答案</summary>\n'
        '<div class="ans-body">{ans}</div>\n</details>\n</div>\n'
        '</div>\n</article>'
    ).format(n=n, id=esc(p['id']), type=esc(p['type']), tier=esc(p['tier']), ext=ext, flag=flag,
             stmt=render_text(p['stmt']), src=p['stmt'].replace('</', '<\\/'), ans=render_text(p['ans']), idea=idea)


def toolbar_html(probs):
    tiers = [t for t in ('基础', '典型', '进阶') if any(p['tier'] == t for p in probs)]
    seg = ('<div class="seg" role="group" aria-label="档次">'
           '<button type="button" data-tier="" aria-pressed="true">全部</button>'
           + ''.join('<button type="button" data-tier="%s" aria-pressed="false">%s</button>' % (t, t) for t in tiers)
           + '</div>')
    ext = ('<label class="chk c-ext"><input type="checkbox" id="opt-ext" checked><span>含拓展</span></label>'
           if any(p['ext'] for p in probs) else '')
    return ''.join([
        '<div class="bar" role="toolbar" aria-label="显示选项">',
        '<button type="button" class="tgl tgl-f" data-panel="p-filter" aria-expanded="false" aria-controls="p-filter">筛选</button>',
        '<div class="panel" id="p-filter">%s%s</div>' % (seg, ext),
        '<label class="chk c-by"><input type="checkbox" id="opt-bytype"><span>按题型</span></label>',
        '<span class="sp"></span><span class="prog" id="prog" aria-live="polite"></span>',
        '<button type="button" class="tgl tgl-m" data-panel="p-more" aria-expanded="false" aria-controls="p-more">更多</button>',
        '<div class="panel" id="p-more"><label class="chk c-all"><input type="checkbox" id="opt-allans"><span>全部答案</span></label>'
        '<button type="button" class="btn" id="btn-print">打印</button></div>',
        '</div>'])


def chapter_path(course, ch):
    return ('<a href="./">%s</a><span class="sep">/</span><span class="now">%s %s</span>'
            % (esc(course['title']), esc(ch['no']), esc(ch['title'])))


def chapter_page(course, ch, probs, prev_ch, next_ch):
    items, last_type = [], None
    for n, p in enumerate(probs, 1):
        if p['type'] != last_type:
            items.append('<h2 class="type-head" data-type="%s"><span class="tid">%s</span><span>%s</span>'
                         '<span class="tier">%s</span></h2>'
                         % (esc(p['type']), esc(p['type']), render_inline(p['type_name']), esc(p['tier'])))
            last_type = p['type']
        items.append(problem_html(p, n))
    left = '<a href="./">← 目录</a>'
    right = ('<a href="%s.html">%s %s →</a>' % (next_ch['id'], esc(next_ch['no']), esc(next_ch['title']))
             if next_ch else '<span></span>')
    inner = (
        '<header class="head"><p class="kicker">%s</p><h1>%s</h1><p class="count">%d 题</p></header>\n'
        '%s\n<main class="list" id="list">\n%s\n</main>\n<footer class="pager">%s%s</footer>'
        % (esc(ch['no']), esc(ch['title']), len(probs), toolbar_html(probs),
           '\n'.join(items), left, right))
    return PAGE.substitute(
        **page_assets(), rail=rail_html('../', chapter_path(course, ch)),
        title='%s %s · %s' % (ch['no'], ch['title'], course['title']),
        desc='%s %s %s，共 %d 题。' % (course['title'], ch['no'], ch['title'], len(probs)),
        c=' '.join(map(str, course['color'])), ca=' '.join(map(str, lighten(course['color']))),
        bodyclass='chapter', course=course['id'], chapter=ch['id'], inner=inner)


# ------------------------------------------------------------------ 讲义（知识点）页
# 课程 course.json 里写 "kind": "notes" 时，章节文件按讲义格式解析：
#   ## 1.1 中文标题 | English Title        一个知识点
#   :::quick / :::proof ★ 标题 / :::example 标题 / :::problem 真题标题 / :::pitfall / :::exam / :::note 标题   …   :::
#   不带编号的 ## 标题（如「## 真题精解 | Past Exam Problems」）进目录但不计入知识点数
#   #### 小标题、- 无序列表、1. 有序列表、| 表格 |、$..$、$$..$$、**粗体**
BOX_NAMES = {'quick': '速查', 'example': '例题', 'problem': '真题', 'pitfall': '易错点', 'exam': '真题考点', 'note': '补充'}
BOX_CLASS = {'problem': 'example exam-q'}


def render_rich(s):
    """讲义用的 Markdown 子集 → HTML（含公式占位符）。"""
    s = re.sub(r'\$\$(.+?)\$\$', lambda m: '\u0001%d\u0002' % M.add(m.group(1).strip(), True), s, flags=re.S)
    s = re.sub(r'\$((?:[^$\n]|\n(?!\s*\n))+?)\$',
               lambda m: '\u0001%d\u0002' % M.add(m.group(1).strip(), False), s)
    s = html.escape(s, quote=False)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'`([^`\n]+)`', r'<code>\1</code>', s)

    out, para, items, kind, rows = [], [], [], None, []

    def flush_para():
        nonlocal para
        if para:
            out.append('<p>' + join_lines(para) + '</p>')
            para = []

    def li(x):
        sub = ''
        if x['sub']:
            sub = '<%s>%s</%s>' % (x['sk'], ''.join('<li>%s</li>' % wrap_disp(join_lines(y)) for y in x['sub']), x['sk'])
        return '<li>%s%s</li>' % (wrap_disp(join_lines(x['l'])), sub)

    def flush_list():
        nonlocal items, kind
        if items:
            out.append('<%s>%s</%s>' % (kind, ''.join(li(x) for x in items), kind))
        items, kind = [], None

    def add_cont(t):
        x = items[-1]
        (x['sub'][-1] if x['sub'] else x['l']).append(t)

    def flush_table():
        nonlocal rows
        if rows:
            cells = [[c.strip() for c in r.strip().strip('|').split('|')] for r in rows]
            body = [r for r in cells if not all(re.fullmatch(r':?-{2,}:?', c or '--') for c in r)]
            head, rest = body[0], body[1:]
            out.append('<div class="tbl"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (
                ''.join('<th>%s</th>' % c for c in head),
                ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % c for c in r) for r in rest)))
            out[-1] = wrap_disp(out[-1])
            rows = []

    def flush_all():
        flush_para()
        flush_list()
        flush_table()

    for line in s.split('\n'):
        t = line.strip()
        if not t:
            flush_all()
            continue
        if t.startswith('|'):
            flush_para()
            flush_list()
            rows.append(t)
            continue
        flush_table()
        mh = re.match(r'^(#{4,5})\s+(.*)$', t)
        if mh:
            flush_all()
            out.append('<h%d>%s</h%d>' % (len(mh.group(1)), mh.group(2), len(mh.group(1))))
            continue
        if any(M.is_display(int(i)) for i in PH.findall(t)) and not re.match(r'^(-|\d+\.)\s', t):
            if items and line.startswith('  '):
                add_cont(t)
                continue
            flush_list()
            for part in re.split('(\u0001\\d+\u0002)', t):
                if not part.strip():
                    continue
                m = re.fullmatch('\u0001(\\d+)\u0002', part)
                if m and M.is_display(int(m.group(1))):
                    flush_para()
                    out.append('<div class="disp">%s</div>' % part)
                else:
                    para.append(part.strip())
            continue
        mul = re.match(r'^-\s+(.*)$', t)
        mol = re.match(r'^\d+\.\s+(.*)$', t)
        if (mul or mol) and items and line.startswith('  '):
            x = items[-1]
            x['sk'] = x['sk'] or ('ul' if mul else 'ol')
            x['sub'].append([(mul or mol).group(1)])
        elif mul or mol:
            flush_para()
            k = 'ul' if mul else 'ol'
            if kind and kind != k:
                flush_list()
            kind = k
            items.append({'l': [(mul or mol).group(1)], 'sub': [], 'sk': None})
        elif items and line.startswith('  '):
            add_cont(t)
        else:
            flush_list()
            para.append(t)
    flush_all()
    return '\n'.join(out)


def wrap_disp(s):
    """列表项、表格里的独立公式：放进可横向滚动的块。"""
    return PH.sub(lambda m: ('<span class="disp">%s</span>' % m.group(0)) if M.is_display(int(m.group(1)))
                  else m.group(0), s)


def parse_notes(path):
    """讲义文件 → {'intro': html, 'kps': [{'no','zh','en','html'}]}"""
    text = path.read_text(encoding='utf8').replace('\r\n', '\n')
    parts = re.split(r'(?m)^##\s+(.+)$', text)
    intro, kps = parts[0], []
    for head, body in zip(parts[1::2], parts[2::2]):
        mh = re.match(r'^(\d+(?:\.\d+)*)\s+(.*)$', head.strip())
        no, rest = (mh.group(1), mh.group(2)) if mh else ('', head.strip())
        zh, _, en = rest.partition('|')
        kps.append({'no': no, 'zh': zh.strip(), 'en': en.strip(), 'html': render_blocks(body, path.name)})
    return {'intro': render_blocks(intro, path.name), 'kps': kps}


def render_blocks(text, fname):
    out, buf, box = [], [], None
    for line in text.split('\n'):
        m = re.match(r'^:::\s*(\w+)?\s*(.*)$', line.strip())
        if m and box is None and m.group(1):
            if buf:
                out.append(render_rich('\n'.join(buf)))
            buf, box = [], (m.group(1), m.group(2).strip())
        elif m and box is not None and not m.group(1):
            out.append(box_html(box[0], box[1], render_rich('\n'.join(buf)), fname))
            buf, box = [], None
        else:
            buf.append(line)
    if box is not None:
        warn('%s：容器 :::%s 没有闭合' % (fname, box[0]))
        out.append(box_html(box[0], box[1], render_rich('\n'.join(buf)), fname))
    elif buf:
        out.append(render_rich('\n'.join(buf)))
    return '\n'.join(x for x in out if x.strip())


def box_html(name, title, inner, fname):
    t = render_inline(title) if title else ''
    if name == 'proof':
        star = 'must' if '★' in title else 'opt'
        return ('<details class="proof %s"><summary><span class="ptag">证明</span>%s</summary>'
                '<div class="proof-body">%s</div></details>' % (star, t, inner))
    if name not in BOX_NAMES:
        warn('%s：未知容器 :::%s' % (fname, name))
    label = BOX_NAMES.get(name, name)
    return ('<div class="box %s"><div class="box-h"><span class="btag">%s</span>%s</div>'
            '<div class="box-b">%s</div></div>' % (esc(BOX_CLASS.get(name, name)), label, ('<span class="bt">%s</span>' % t) if t else '', inner))


def notes_page(course, ch, notes, next_ch):
    kps = notes['kps']
    # 不带编号的 ##（如「真题精解」）照常进目录，但不计入知识点数
    for i, k in enumerate(kps):
        k['slug'] = k['no'].replace('.', '-') if k['no'] else 'x%d' % i
    n_kp = sum(1 for k in kps if k['no'])
    toc = ''.join('<li%s><a href="#kp-%s"><span class="kno">%s</span><span class="kt">%s</span>'
                  '<span class="ken">%s</span></a></li>'
                  % ('' if k['no'] else ' class="extra"', esc(k['slug']), esc(k['no'] or '◆'),
                     render_inline(k['zh']), esc(k['en'])) for k in kps)
    secs = ''.join(
        '<section class="kp%s" id="kp-%s"><h2><span class="kno">%s</span><span class="kt">%s</span>'
        '<span class="ken">%s</span></h2>\n%s\n</section>\n'
        % ('' if k['no'] else ' extra', esc(k['slug']), esc(k['no']), render_inline(k['zh']), esc(k['en']), k['html'])
        for k in kps)
    bar = ('<div class="bar" role="toolbar" aria-label="显示选项">'
           '<label class="chk"><input type="checkbox" id="opt-proofs"><span>展开全部证明</span></label>'
           '<label class="chk"><input type="checkbox" id="opt-only-must"><span>只看 ★ 证明</span></label>'
           '<span class="sp"></span><button type="button" class="btn" id="btn-print">打印</button></div>')
    left = '<a href="./">← 目录</a>'
    right = ('<a href="%s.html">%s %s →</a>' % (next_ch['id'], esc(next_ch['no']), esc(next_ch['title']))
             if next_ch else '<span></span>')
    en = '<p class="en">%s</p>' % esc(ch['en']) if ch.get('en') else ''
    inner = (
        '<header class="head"><p class="kicker">%s</p><h1>%s</h1>%s<p class="count">%d 个知识点</p></header>\n'
        '%s\n<nav class="kp-toc" aria-label="本讲知识点"><ol>%s</ol></nav>\n'
        '<div class="intro">%s</div>\n<main class="notes-body">\n%s</main>\n<footer class="pager">%s%s</footer>'
        % (esc(ch['no']), esc(ch['title']), en, n_kp, bar, toc,
           notes['intro'], secs, left, right))
    return PAGE.substitute(
        **page_assets(), rail=rail_html('../', chapter_path(course, ch)),
        title='%s %s · %s' % (ch['no'], ch['title'], course['title']),
        desc='%s %s %s，共 %d 个知识点。' % (course['title'], ch['no'], ch['title'], n_kp),
        c=' '.join(map(str, course['color'])), ca=' '.join(map(str, lighten(course['color']))),
        bodyclass='notes', course=course['id'], chapter=ch['id'], inner=inner)


def course_page(course, counts):
    notes = course.get('kind') == 'notes'
    unit = '个知识点' if notes else '题'
    avail_rows, soon_rows = [], []
    for ch in course['chapters']:
        n = counts.get(ch['id'])
        head = '<span class="no">%s</span><span class="t">%s</span><span class="dots"></span>' % (
            esc(ch['no']), esc(ch['title']))
        if n:
            avail_rows.append('<li><a href="%s.html">%s<span class="n">%d %s</span></a></li>'
                              % (ch['id'], head, n, unit))
        else:
            soon_rows.append('<li class="soon"><div class="row">%s<span class="n">待续</span></div></li>' % head)
    total = sum(counts.values())
    if notes:
        status = '已收录 %d 讲 · %d 个知识点' % (len(counts), total) if total else '讲义整理中，敬请期待'
    else:
        status = '已收录 %d 题' % total if total else '题目整理中，敬请期待'
    toc = ''
    if avail_rows:
        toc += '\n<ol class="toc">\n%s\n</ol>' % '\n'.join(avail_rows)
    if soon_rows:
        what = '讲' if notes else '章'
        label = '其余 %d %s整理中' % (len(soon_rows), what) if avail_rows else '%s整理中' % ('讲义' if notes else '章节')
        toc += ('\n<details class="soon-group"%s><summary>%s</summary>\n<ol class="toc">\n%s\n</ol>\n</details>'
                % ('' if avail_rows else ' open', label, '\n'.join(soon_rows)))
    inner = (
        '<header class="head"><p class="kicker">%s</p><h1>%s</h1><p class="en">%s</p>'
        '<p class="count">%s</p></header>%s'
        % (esc(course['volume']), esc(course['title']), esc(course['en']), status, toc))
    return PAGE.substitute(
        title='%s · 课程讲义' % course['title'], **page_assets(),
        rail=rail_html('../', '<span class="now">%s %s</span>' % (esc(course['volume']), esc(course['title']))),
        desc='%s 讲义目录。' % course['title'],
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


ASCII = ''.join(chr(c) for c in range(0x20, 0x7F)) + '—·'


def subset_woff(text):
    """用 Noto Serif CJK Medium 截取指定文字，返回 woff 字节；找不到字体时返回 None。"""
    src = next((c for c in ['/usr/share/fonts/opentype/noto/NotoSerifCJK-Medium.ttc']
                if pathlib.Path(c).exists()), None)
    if not src:
        return None
    from fontTools.subset import Options, Subsetter
    from fontTools.ttLib import TTCollection, TTFont
    idx = next(i for i, f in enumerate(TTCollection(src).fonts) if 'SC' in f['name'].getDebugName(1))
    font = TTFont(src, fontNumber=idx)
    opts = Options()
    opts.flavor = 'woff'
    opts.layout_features = ['kern', 'liga', 'tnum']
    opts.name_IDs = []
    sub = Subsetter(opts)
    sub.populate(text=text + ASCII)
    sub.subset(font)
    font.flavor = 'woff'
    buf = io.BytesIO()
    font.save(buf)
    return buf.getvalue()


def build_serif_subset(strings):
    """课程页标题用的宋体：只截取标题里出现的字，体积很小。"""
    data = subset_woff(''.join(sorted(set(''.join(strings)))))
    if data is None:
        warn('找不到 Noto Serif CJK，沿用已有的 serif-sc.woff')
        return
    (ROOT / 'assets' / 'fonts' / 'serif-sc.woff').write_bytes(data)


# ------------------------------------------------------------------ 首页（书架）
CN = '零一二三四五六七八九十'


def cn(n):
    return CN[n] if n <= 10 else '十' + CN[n - 10]


def book_html(c, i):
    light = ' light' if c.get('light') else ''
    n = c.get('_count', 0)
    unit = '个知识点' if c.get('kind') == 'notes' else '题'
    title = ' title="已有 %d %s"' % (n, unit) if n else ''
    sr = '<span class="sr">，已有 %d %s</span>' % (n, unit) if n else ''
    return (
        '<a class="book%s" href="./%s/index.html"%s style="--c:%s;--w:%dpx;--h:%dpx;--d:%d">\n'
        '  <span class="vol">%s</span>\n'
        '  <span class="spine"><h2>%s</h2><span class="en">%s</span></span>\n'
        '  <svg class="glyph" viewBox="0 0 40 40" aria-hidden="true">%s</svg>%s\n</a>'
        % (light, esc(c['id']), title, ' '.join(map(str, c['color'])), c['spine']['w'], c['spine']['h'], i,
           esc(c['volume']), esc(c['title']), esc(c['en']), c['glyph'], sr))


def letter_button(lt, i):
    return ('<button class="letter" type="button" aria-haspopup="dialog" aria-label="拆开这封信：%s" style="--d:%d">'
            '<span class="env" aria-hidden="true"><span class="env-back"></span><span class="env-paper"></span>'
            '<span class="env-front"></span><span class="env-flap"></span><span class="env-seal"></span></span>'
            '<span class="env-label">%s</span></button>' % (esc(lt['title']), i, esc(lt['label'])))


def letter_dialog(lt):
    paras = ''.join('<p>%s</p>' % esc(p) for p in lt['paragraphs'])
    return ('<dialog class="letter-dialog" aria-labelledby="letter-title"><article class="paper">'
            '<form method="dialog" class="x"><button class="xbtn" aria-label="合上这封信">×</button></form>'
            '<h2 id="letter-title">%s</h2>%s<p class="sign">%s<br>%s</p>'
            '<form method="dialog"><button class="close">合上</button></form></article></dialog>'
            % (esc(lt['title']), paras, esc(lt['sign']), esc(lt['date'])))


def cn_n(n):
    """1–99 的中文数字。"""
    if n <= 10:
        return CN[n]
    if n < 20:
        return '十' + CN[n - 10]
    return CN[n // 10] + '十' + (CN[n % 10] if n % 10 else '')


def favicon_svg(courses):
    bw, gap, ggap = 4.6, 2.2, 3.0
    groups = {}
    for c in courses:
        groups.setdefault(c['series'], []).append(c)
    n = len(courses)
    total = n * bw + (n - len(groups)) * gap + (len(groups) - 1) * ggap
    x, rects = (64 - total) / 2, []
    for k, sno in enumerate(sorted(groups)):
        if k:
            x += ggap - gap
        for c in sorted(groups[sno], key=lambda c: c['order']):
            h = 18 + (c['spine']['h'] - 400) * 0.32
            rects.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="1" fill="#%02x%02x%02x"/>'
                         % (x, 52 - h, bw, h, *c['color']))
            x += bw + gap
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#14110f"/>%s</svg>'
            % ''.join(rects))


def favicon_uri(courses):
    svg = favicon_svg(courses)
    (ROOT / 'assets' / 'favicon.svg').write_text(svg + '\n', encoding='utf8')
    return 'data:image/svg+xml,' + urllib.parse.quote(svg)


def git_dates(path):
    """这个文件每次提交的日期（新→旧）；没提交过的返回空。"""
    try:
        out = subprocess.run(['git', '-C', str(ROOT), 'log', '--follow', '--format=%ad', '--date=short', '--', str(path)],
                             capture_output=True, text=True, timeout=20).stdout.split()
    except Exception:
        return []
    return out


def footer_html(courses, root):
    """页脚：最近的更新记录（来自 git 历史）+ 收录量。"""
    today = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).date().isoformat()
    log = []
    for c in courses:
        for k, ch in enumerate(c['chapters']):
            f = c['_dir'] / (ch['id'] + '.md')
            if not f.exists():
                continue
            ds = git_dates(f)
            dirty = subprocess.run(['git', '-C', str(ROOT), 'status', '--porcelain', '--', str(f)],
                                   capture_output=True, text=True).stdout.strip() if ds else 'new'
            latest = today if dirty else ds[0]
            verb = '新增' if (not ds or (len(set(ds)) == 1 and latest == ds[-1])) else '更新'
            log.append((latest, c['order'] * 100 + k, verb, c, ch))
    log.sort(key=lambda x: (x[0], x[1]), reverse=True)
    rows = ''.join(
        '<li><time datetime="%s">%s</time><i style="--c:%s"></i><span class="v">%s</span>'
        '<a href="%s%s/%s.html">%s · %s %s</a></li>'
        % (d, d[5:].replace('-', '/'), ' '.join(map(str, c['color'])), verb, root, esc(c['id']), esc(ch['id']),
           esc(c['title']), esc(ch['no']), esc(ch['title'])) for d, _, verb, c, ch in log[:6])
    probs = sum(c.get('_count', 0) for c in courses if c.get('kind') != 'notes')
    kps = sum(c.get('_count', 0) for c in courses if c.get('kind') == 'notes')
    stat = ['<b>%d</b> 门课' % len(courses)]
    if probs:
        stat.append('<b>%d</b> 道题' % probs)
    if kps:
        stat.append('<b>%d</b> 个知识点' % kps)
    return ('<footer class="foot"><section><h3>更新记录</h3><ol>%s</ol></section>'
            '<p class="stat">%s<br>最近更新 %s</p>'
            '<p class="fine"><span>个人整理，难免有误；遇到觉得不对的地方，请相信自己的判断。</span>'
            '<span>宋体排印 · 公式由 KaTeX 渲染</span></p></footer>'
            % (rows, ' · '.join(stat), log[0][0].replace('-', '/') if log else today.replace('-', '/')))


def build_home(courses, site, idx_version):
    by_series = {}
    for c in courses:
        by_series.setdefault(c['series'], []).append(c)
    last = max(by_series)
    sections, i = [], 0
    for sno in sorted(by_series):
        meta = site['series'][sno - 1]
        cs = sorted(by_series[sno], key=lambda c: c['order'])
        books = []
        for c in cs:
            books.append(book_html(c, i))
            i += 1
        if sno == min(by_series) and site.get('letter'):
            books.append(letter_button(site['letter'], i))
            i += 1
        if sno == last:
            books.append(
                '<div class="slot" aria-label="待续" style="--d:%d"><span class="vol">%02d — ∞</span>'
                '<span class="spine"><h2>待续</h2><span class="en">More volumes to come</span></span>'
                '<span></span></div>' % (i, len(courses) + 1))
        # 辑名不再是浮在书架上方的网页标题，而是插在层板前沿铜框里的一张小卡片
        sections.append(
            '<section class="series" aria-labelledby="s%d">\n<div class="shelf">\n%s\n</div>\n'
            '<div class="plank"><h2 class="tag" id="s%d"><span class="sno">%s</span><span class="sname">%s</span></h2></div>\n'
            '</section>'
            % (sno, '\n'.join(books), sno, esc(meta['no']), esc(meta['name'])))
    ordered = sorted(courses, key=lambda c: c['order'])
    tpl = Template((TOOLS / 'index.template.html').read_text(encoding='utf8'))
    dialog = letter_dialog(site['letter']) if site.get('letter') else ''
    page = tpl.substitute(RAIL=rail_html('./'), SERIES='\n'.join(sections), LETTER_DIALOG=dialog,
                          FOOTER=footer_html(ordered, './'), FAVICON=favicon_uri(ordered),
                          VRCSS=asset_version('rail.css'), VRJS=asset_version('rail.js'), VIDX=idx_version)

    # 首页保持单文件：字体以 base64 内嵌（宋体按首页用到的字截取）
    visible = html.unescape(re.sub(r'<style>.*?</style>|<[^>]+>', '', page, flags=re.S))
    serif = subset_woff(''.join(sorted(set(visible))))
    fonts = ROOT / 'assets' / 'fonts'

    def face(family, data, style='normal', weight='400'):
        return ('  @font-face{font-family:"%s";font-style:%s;font-weight:%s;font-display:swap;'
                'src:url(data:font/woff;base64,%s) format("woff")}'
                % (family, style, weight, base64.b64encode(data).decode()))

    faces = []
    if serif is not None:
        faces.append(face('Portal Serif SC', serif, weight='400 600'))
    else:
        warn('找不到 Noto Serif CJK，首页没有内嵌宋体')
    faces.append(face('Portal Sans', (fonts / 'portal-sans.woff').read_bytes()))
    faces.append(face('Portal Italic', (fonts / 'portal-italic.woff').read_bytes(), style='italic'))
    return re.sub(r'/\* FONTS:BEGIN \*/.*?/\* FONTS:END \*/',
                  lambda m: '/* FONTS:BEGIN */\n' + '\n'.join(faces) + '\n  /* FONTS:END */', page, flags=re.S)


# ------------------------------------------------------------------ 搜索索引
def plain(s):
    """搜索用的纯文本：去掉公式定界符和 Markdown 记号。"""
    return re.sub(r'\s+', ' ', re.sub(r'[$*`\\{}]', '', s)).strip()


def index_course(index, course, avail, data):
    """课程、章节、题型（每类指向第一道题）、知识点，都进搜索索引。链接相对站点根目录。"""
    c = ' '.join(map(str, course['color']))
    cid = course['id']
    index.append({'k': '课程', 't': course['title'], 'en': course['en'], 's': course['volume'], 'u': cid + '/', 'c': c})
    for ch in avail:
        page = '%s/%s.html' % (cid, ch['id'])
        index.append({'k': '章', 't': ch['title'], 'en': ch.get('en', ''), 's': '%s · %s' % (course['title'], ch['no']),
                      'u': page, 'c': c})
        if course.get('kind') == 'notes':
            for i, k in enumerate(data[ch['id']]['kps']):
                if k['no']:
                    index.append({'k': '知识点', 't': plain(k['zh']), 'en': k['en'],
                                  's': '%s · %s' % (course['title'], k['no']),
                                  'u': '%s#kp-%s' % (page, k['no'].replace('.', '-')), 'c': c})
        else:
            seen = set()
            for n, p in enumerate(data[ch['id']], 1):
                if p['type'] not in seen:
                    seen.add(p['type'])
                    index.append({'k': '题型', 't': plain(p['type_name']), 's': '%s · %s' % (course['title'], ch['no']),
                                  'u': '%s#q%d' % (page, n), 'c': c})


# ------------------------------------------------------------------ 主流程
def main():
    site = json.loads((CONTENT / 'site.json').read_text(encoding='utf8'))
    courses = []
    for cfile in sorted(CONTENT.glob('*/course.json')):
        c = json.loads(cfile.read_text(encoding='utf8'))
        c['_dir'] = cfile.parent
        courses.append(c)
    courses.sort(key=lambda c: c.get('order', 99))

    pages = {}
    index = []
    serif_text = [site['title'], '待续', '卷一二三四五六七八九十', '第章综合']
    summary = []
    for course in courses:
        cdir = course['_dir']
        serif_text += [course['title'], course['volume']]
        chapters = course['chapters']
        data = {}
        if course.get('kind') == 'notes':
            for ch in chapters:
                serif_text += [ch['no'], ch['title']]
                f = cdir / (ch['id'] + '.md')
                if f.exists():
                    data[ch['id']] = parse_notes(f)
                    serif_text += [k['zh'] for k in data[ch['id']]['kps']]
            avail = [ch for ch in chapters if ch['id'] in data]
            index_course(index, course, avail, data)
            for i, ch in enumerate(avail):
                nxt = avail[i + 1] if i + 1 < len(avail) else None
                pages[ROOT / course['id'] / (ch['id'] + '.html')] = notes_page(course, ch, data[ch['id']], nxt)
                summary.append('%s %s：%d 个知识点' % (course['id'], ch['id'],
                                                     sum(1 for k in data[ch['id']]['kps'] if k['no'])))
            course['_count'] = sum(sum(1 for x in v['kps'] if x['no']) for v in data.values())
            pages[ROOT / course['id'] / 'index.html'] = course_page(
                course, {k: sum(1 for x in v['kps'] if x['no']) for k, v in data.items()})
            continue
        for ch in chapters:
            serif_text += [ch['no'], ch['title']]
            f = cdir / (ch['id'] + '.md')
            if f.exists():
                data[ch['id']] = parse_chapter(f)
        course['_count'] = sum(len(v) for v in data.values())
        avail = [ch for ch in chapters if ch['id'] in data]
        index_course(index, course, avail, data)
        for i, ch in enumerate(avail):
            nxt = avail[i + 1] if i + 1 < len(avail) else None
            pages[ROOT / course['id'] / (ch['id'] + '.html')] = chapter_page(course, ch, data[ch['id']], None, nxt)
            tiers = {}
            for p in data[ch['id']]:
                tiers[p['tier']] = tiers.get(p['tier'], 0) + 1
            summary.append('%s %s：%d 题 %s' % (course['id'], ch['id'], len(data[ch['id']]), tiers))
        pages[ROOT / course['id'] / 'index.html'] = course_page(course, {k: len(v) for k, v in data.items()})

    idx_js = 'window.SEARCH_INDEX=' + json.dumps(index, ensure_ascii=False, separators=(',', ':')) + ';\n'
    (ROOT / 'assets' / 'search-index.js').write_text(idx_js, encoding='utf8')
    idx_version = asset_version('search-index.js')
    foot = footer_html(courses, '../')
    rendered = render_maths()
    for path, page in pages.items():
        page = PH.sub(lambda m: rendered[int(m.group(1))], page)
        page = page.replace('\u0003FOOT\u0004', foot).replace('\u0003IDX\u0004', idx_version)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(page, encoding='utf8')

    ensure_latin_fonts()
    build_serif_subset(serif_text)
    (ROOT / 'index.html').write_text(build_home(courses, site, idx_version), encoding='utf8')
    print('\n'.join(summary))
    print('搜索索引 %d 条' % len(index))
    print('课程 %d 门，页面 %d 个（另含首页），公式 %d 条，警告 %d 条'
          % (len(courses), len(pages), len(M.items), len(WARNINGS)))


main()
