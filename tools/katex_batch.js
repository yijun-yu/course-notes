// 批量渲染公式：从 stdin 读入 [{t: "TeX", d: 是否独立公式}]，向 stdout 输出 [{html, err}]
// KaTeX 优先从 node_modules 加载，找不到时用 KATEX_PATH 或环境里预装的那一份。
let katex;
try {
  katex = require('katex');
} catch (e) {
  katex = require(process.env.KATEX_PATH || '/opt/npm-tools/node_modules/katex');
}

const chunks = [];
process.stdin.on('data', (c) => chunks.push(c));
process.stdin.on('end', () => {
  const items = JSON.parse(Buffer.concat(chunks).toString('utf8'));
  const out = items.map(({ t, d }) => {
    const html = katex.renderToString(t, {
      displayMode: d,
      throwOnError: false,
      strict: 'ignore',
      trust: false,
      output: 'html',
      errorColor: '#e07a7a',
    });
    return { html, err: html.includes('katex-error') };
  });
  process.stdout.write(JSON.stringify(out));
});
