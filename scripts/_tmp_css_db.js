const fs = require('fs');
const wsUrl = fs.readFileSync('C:\\Users\\ptmou\\Desktop\\WX-chatbot\\wx-agent\\_ws_url.txt','utf8').trim();
const ws = new WebSocket(wsUrl);
let id=0; const pend=new Map();
function send(m,p){ return new Promise(res=>{ const i=++id; pend.set(i,res); ws.send(JSON.stringify({id:i,method:m,params:p})); }); }
ws.onmessage = ev=>{ const m=JSON.parse(ev.data); if(m.id&&pend.has(m.id)){ pend.get(m.id)(m.result); pend.delete(m.id); } };
async function evalJS(expr){ const r=await send('Runtime.evaluate',{expression:expr,returnByValue:true}); return r&&r.result?r.result.value:null; }
ws.onopen = async ()=>{
  await send('Runtime.enable',{});
  const st = await evalJS(`(()=>{
    const d = document.documentElement;
    const b = document.body;
    return {
      theme: d.getAttribute('data-theme'),
      bodyClass: b.className,
      bgBody: getComputedStyle(b).backgroundImage.slice(0,120),
      bgRoot: getComputedStyle(b).backgroundColor,
      blue: getComputedStyle(b).color,
    };
  })()`);
  console.log(JSON.stringify(st, null, 2));
  ws.close();
};
