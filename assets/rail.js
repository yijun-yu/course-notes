/* 全站页眉：滚动后出现分隔线、内页阅读进度线、搜索面板（/ 或 Ctrl/⌘+K）。 */
(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const rail = $('.rail');
  if (!rail) return;
  const root = document.body.dataset.root || './';

  // 滚动：页眉下沿出现分隔线；内页的细线表示本页读到哪里
  const line = $('.rail-line');
  const onScroll = () => {
    rail.classList.toggle('scrolled', scrollY > 4);
    if (line) {
      const h = document.documentElement.scrollHeight - innerHeight;
      line.style.setProperty('--s', h > 0 ? Math.min(1, scrollY / h) : 0);
    }
  };
  addEventListener('scroll', onScroll, { passive: true });
  addEventListener('resize', onScroll);
  onScroll();

  // 搜索面板：课程、章节、题型、知识点
  const box = document.createElement('div');
  box.className = 'find';
  box.innerHTML = '<div class="find-box" role="dialog" aria-modal="true" aria-label="搜索">'
    + '<input type="search" placeholder="搜课程、章节、题型、知识点…" autocomplete="off" spellcheck="false" aria-label="搜索">'
    + '<ul role="listbox"></ul><div class="hint"><span>↑↓ 选择</span><span>↵ 打开</span><span>esc 关闭</span></div></div>';
  document.body.appendChild(box);
  const input = $('input', box), list = $('ul', box);
  let hits = [], sel = 0, last = null;

  const esc = (s) => String(s).replace(/[&<>"]/g, (m) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[m]));
  const mark = (t, q) => {
    if (!q) return esc(t);
    const i = t.toLowerCase().indexOf(q.toLowerCase());
    return i < 0 ? esc(t) : esc(t.slice(0, i)) + '<mark>' + esc(t.slice(i, i + q.length)) + '</mark>' + esc(t.slice(i + q.length));
  };
  const score = (it, q) => {
    if (!q) return it.k === '课程' ? 1 : 0;
    const t = it.t.toLowerCase(), rest = (it.s + ' ' + (it.en || '')).toLowerCase();
    q = q.toLowerCase();
    if (t.startsWith(q)) return 5;
    if (t.includes(q)) return 4;
    if (rest.includes(q)) return 2;
    const words = q.split(/\s+/).filter(Boolean);   // 「留数 积分」：每个词都出现即可
    return words.length > 1 && words.every((w) => (t + ' ' + rest).includes(w)) ? 1 : 0;
  };
  const render = () => {
    const q = input.value.trim();
    const all = window.SEARCH_INDEX || [];
    hits = all.map((it, i) => [score(it, q), i, it]).filter((x) => x[0] > 0)
      .sort((a, b) => b[0] - a[0] || a[1] - b[1]).slice(0, 50).map((x) => x[2]);
    sel = 0;
    list.innerHTML = hits.length
      ? hits.map((it, i) => '<li role="option"' + (i ? '' : ' class="sel"') + '><a href="' + esc(root + it.u)
        + '" style="--c:' + it.c + '"><i class="dot"></i><span class="t">' + mark(it.t, q) + '</span><span class="s">'
        + esc(it.s) + (it.k === '课程' ? '' : ' · ' + esc(it.k)) + '</span></a></li>').join('')
      : '<li class="empty">没有找到「' + esc(q) + '」</li>';
  };
  const move = (d) => {
    if (!hits.length) return;
    const li = $$('li', list);
    li[sel].classList.remove('sel');
    sel = (sel + d + hits.length) % hits.length;
    li[sel].classList.add('sel');
    li[sel].scrollIntoView({ block: 'nearest' });
  };
  const open = () => {
    last = document.activeElement;
    box.classList.add('on');
    input.value = '';
    render();
    input.focus();
  };
  const close = () => {
    box.classList.remove('on');
    if (last && last.focus) last.focus();
  };
  input.addEventListener('input', render);
  input.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowDown') { e.preventDefault(); move(1); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); move(-1); }
    else if (e.key === 'Enter' && hits[sel]) { e.preventDefault(); close(); location.href = root + hits[sel].u; }
    else if (e.key === 'Escape') { e.preventDefault(); close(); }
  });
  list.addEventListener('click', (e) => { if (e.target.closest('a')) close(); });
  box.addEventListener('click', (e) => { if (e.target === box) close(); });
  $('.rail-find').addEventListener('click', open);
  addEventListener('keydown', (e) => {
    const el = document.activeElement;
    const typing = el && (/^(INPUT|TEXTAREA|SELECT)$/.test(el.tagName) || el.isContentEditable);
    if ((e.key === '/' && !typing && !e.metaKey && !e.ctrlKey) || ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k')) {
      e.preventDefault();
      box.classList.contains('on') ? input.focus() : open();
    }
  });
})();
