/* 题目页交互：档次筛选、拓展开关、按题型显示、全部答案、已做标记、打印。
   没有 JavaScript 时，答案仍可用 <details> 点开，页面照常可读。 */
(() => {
  'use strict';
  const body = document.body;
  if (!body.classList.contains('chapter')) return;

  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const key = 'cn:' + body.dataset.course + ':' + body.dataset.chapter + ':';
  const load = (k, d) => {
    try { const v = localStorage.getItem(key + k); return v === null ? d : JSON.parse(v); }
    catch (e) { return d; }
  };
  const save = (k, v) => { try { localStorage.setItem(key + k, JSON.stringify(v)); } catch (e) {} };

  const probs = $$('.prob');
  const heads = $$('.type-head');
  const tierBtns = $$('.seg button');
  const optExt = $('#opt-ext');
  const optBy = $('#opt-bytype');
  const optAll = $('#opt-allans');
  const prog = $('#prog');
  const done = new Set(load('done', []));

  const validTiers = tierBtns.map((b) => b.dataset.tier);
  const state = {
    tier: validTiers.includes(load('tier', '')) ? load('tier', '') : '',
    ext: load('ext', true),
    byType: load('bytype', false),
    allAns: load('allans', false),
  };

  /* 过宽的独立公式：右侧渐隐提示可横向滑动，滑到头后取消 */
  function measure(root) {
    $$('.disp', root).forEach((d) => {
      if (!d._wired) {
        d._wired = true;
        d.addEventListener('scroll', () => {
          d.classList.toggle('end', d.scrollLeft + d.clientWidth >= d.scrollWidth - 2);
        }, { passive: true });
      }
      const over = d.scrollWidth > d.clientWidth + 1;
      d.classList.toggle('ov', over);
      d.classList.toggle('end', over && d.scrollLeft + d.clientWidth >= d.scrollWidth - 2);
    });
  }

  function apply() {
    probs.forEach((p) => {
      const okTier = !state.tier || p.dataset.tier === state.tier;
      const okExt = state.ext || p.dataset.ext !== '1';
      p.hidden = !(okTier && okExt);
    });
    heads.forEach((h) => {
      h.hidden = !probs.some((p) => p.dataset.type === h.dataset.type && !p.hidden);
    });
    body.classList.toggle('by-type', state.byType);
    const tf = $('.tgl-f');
    if (tf) tf.classList.toggle('on', !!state.tier || !state.ext);
    tierBtns.forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.tier === state.tier)));
    if (optExt) optExt.checked = state.ext;
    if (optBy) optBy.checked = state.byType;
    if (optAll) optAll.checked = state.allAns;
    measure(document);
  }

  function renderDone() {
    probs.forEach((p) => {
      const on = done.has(p.dataset.id);
      const btn = $('.done', p);
      if (btn) btn.setAttribute('aria-pressed', String(on));
    });
    if (prog) prog.textContent = '已完成 ' + done.size + ' / ' + probs.length;
  }

  function setAllAnswers(open) {
    $$('details.ans').forEach((d) => { d.open = open; });
  }

  tierBtns.forEach((b) => b.addEventListener('click', () => {
    state.tier = b.dataset.tier; save('tier', state.tier); apply();
  }));
  if (optExt) optExt.addEventListener('change', () => { state.ext = optExt.checked; save('ext', state.ext); apply(); });
  if (optBy) optBy.addEventListener('change', () => { state.byType = optBy.checked; save('bytype', state.byType); apply(); });
  if (optAll) optAll.addEventListener('change', () => {
    state.allAns = optAll.checked; save('allans', state.allAns); setAllAnswers(state.allAns);
  });

  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text).then(() => true, () => false);
    }
    const ta = document.createElement('textarea');
    ta.value = text; ta.setAttribute('readonly', '');
    ta.style.cssText = 'position:fixed;top:-1000px;opacity:0';
    document.body.appendChild(ta); ta.select();
    let ok = false;
    try { ok = document.execCommand('copy'); } catch (e) {}
    document.body.removeChild(ta);
    return Promise.resolve(ok);
  }

  const list = $('#list');
  if (list) list.addEventListener('click', (e) => {
    const cp = e.target.closest('.copy');
    if (cp) {
      const src = $('script.src', cp.closest('.prob'));
      const text = src ? src.textContent.replace(/<\\\//g, '</').trim() : '';
      const old = cp.textContent;
      copyText(text).then((ok) => {
        cp.textContent = ok ? '已复制' : '复制失败';
        setTimeout(() => { cp.textContent = old; }, 1400);
      });
      return;
    }
    const btn = e.target.closest('.done');
    if (!btn) return;
    const id = btn.closest('.prob').dataset.id;
    if (done.has(id)) done.delete(id); else done.add(id);
    save('done', Array.from(done));
    renderDone();
  });

  /* 手机上工具条折叠：筛选、更多 */
  const tglBtns = $$('.bar .tgl');
  tglBtns.forEach((t) => t.addEventListener('click', () => {
    const panel = document.getElementById(t.dataset.panel);
    if (!panel) return;
    const willOpen = !panel.classList.contains('open');
    $$('.bar .panel').forEach((p) => p.classList.remove('open'));
    tglBtns.forEach((x) => x.setAttribute('aria-expanded', 'false'));
    if (willOpen) { panel.classList.add('open'); t.setAttribute('aria-expanded', 'true'); }
  }));

  const printBtn = $('#btn-print');
  if (printBtn) printBtn.addEventListener('click', () => window.print());

  apply();
  renderDone();
  if (state.allAns) setAllAnswers(true);
  document.addEventListener('toggle', (e) => measure(e.target), true);
  let rt = 0;
  window.addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(() => measure(document), 150); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => measure(document));
})();

/* 讲义页交互：展开全部证明、只看 ★ 证明、打印时展开全部证明、过宽公式提示。 */
(() => {
  'use strict';
  const body = document.body;
  if (!body.classList.contains('notes')) return;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const key = 'cn:' + body.dataset.course + ':notes:';
  const load = (k, d) => {
    try { const v = localStorage.getItem(key + k); return v === null ? d : JSON.parse(v); }
    catch (e) { return d; }
  };
  const save = (k, v) => { try { localStorage.setItem(key + k, JSON.stringify(v)); } catch (e) {} };

  const proofs = $$('details.proof');
  const optAll = $('#opt-proofs');
  const optMust = $('#opt-only-must');
  const state = { all: load('allproofs', false), must: load('onlymust', false) };

  function measure(root) {
    $$('.disp', root).forEach((d) => {
      if (!d._wired) {
        d._wired = true;
        d.addEventListener('scroll', () => {
          d.classList.toggle('end', d.scrollLeft + d.clientWidth >= d.scrollWidth - 2);
        }, { passive: true });
      }
      const over = d.scrollWidth > d.clientWidth + 1;
      d.classList.toggle('ov', over);
      d.classList.toggle('end', over && d.scrollLeft + d.clientWidth >= d.scrollWidth - 2);
    });
  }
  function apply() {
    if (optAll) optAll.checked = state.all;
    if (optMust) optMust.checked = state.must;
    body.classList.toggle('only-must', state.must);
    proofs.forEach((d) => { d.open = state.all; });
    measure(document);
  }
  if (optAll) optAll.addEventListener('change', () => { state.all = optAll.checked; save('allproofs', state.all); apply(); });
  if (optMust) optMust.addEventListener('change', () => { state.must = optMust.checked; save('onlymust', state.must); apply(); });
  const printBtn = $('#btn-print');
  if (printBtn) printBtn.addEventListener('click', () => window.print());

  let before = [];
  window.addEventListener('beforeprint', () => {
    before = proofs.map((d) => d.open);
    proofs.forEach((d) => { d.open = true; });
  });
  window.addEventListener('afterprint', () => { proofs.forEach((d, i) => { d.open = before[i]; }); });

  apply();
  document.addEventListener('toggle', (e) => measure(e.target), true);
  let rt = 0;
  window.addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(() => measure(document), 150); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => measure(document));
})();
