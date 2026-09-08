const http = require('http');
const fs = require('fs');
const { execSync } = require('child_process');

(async () => {
  const port = 9333;
  execSync(`start msedge --headless --disable-gpu --remote-debugging-port=${port} about:blank`, {shell: true});
  await new Promise(r => setTimeout(r, 2500));
  const list = await fetch(`http://127.0.0.1:${port}/json`);
  const pages = await list.json();
  const wsUrl = pages[0].webSocketDebuggerUrl;
  const ws = new WebSocket(wsUrl);
  let id = 0; const pend = {};
  const send = (method, params={}) => new Promise(res => { const i = ++id; pend[i] = res; ws.send(JSON.stringify({id:i, method, params})); });
  const wait = (ms) => new Promise(r => setTimeout(r, ms));
  await new Promise(r => ws.onopen = r);
  ws.onmessage = (ev) => { const m = JSON.parse(ev.data); if (m.id && pend[m.id]) { pend[m.id](m.result); delete pend[m.id]; } };
  await send('Page.enable');
  const url = 'http://127.0.0.1:3210/?token=mYipnb8JCS_RyT8tsGgMRMa5fmC9XyyM';
  await send('Page.navigate', {url});
  await wait(4000);
  const shot = async (name) => { const r = await send('Page.captureScreenshot', {format:'png'}); fs.writeFileSync(`C:\\Users\\ptmou\\Desktop\\WX-chatbot\\_v_${name}.png`, Buffer.from(r.data, 'base64')); };
  await shot('1_main');
  // 导航滚到底（030017 色差）
  await send('Runtime.evaluate', {expression:`document.querySelector('.side').scrollTop = 99999;`});
  await wait(600); await shot('2_nav_bottom');
  // 代码检测（速度）
  await send('Runtime.evaluate', {expression:`document.getElementById('selfCheck')?0:0; document.getElementById('codeCheck') && document.getElementById('codeCheck').click();`});
  await wait(2500); await shot('3_codecheck');
  // 切鲸语：select 设 whale → 保存（自动刷新）
  await send('Runtime.evaluate', {expression:`(()=>{ const sel = document.querySelector('[data-cfg="ui.text_style"]'); if(sel){ sel.value='whale'; sel.dispatchEvent(new Event('change')); } const b = document.querySelector('[data-save]'); if(b) b.click(); })()`});
  await wait(3500); await shot('4_whale');
  console.log('DONE');
  process.exit(0);
})().catch(e => { console.error('ERR', e.message); process.exit(1); });