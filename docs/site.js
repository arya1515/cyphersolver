// shared behaviour: theme, menu, active link, contents strip, scroll-reveal, card glow, interlinear tiles, queue filter
(function(){
  // theme: stored choice wins, otherwise follow the OS
  const root=document.documentElement;
  let stored=null; try{ stored=localStorage.getItem('theme'); }catch(e){}
  const prefersLight=matchMedia('(prefers-color-scheme: light)').matches;
  root.dataset.theme = stored || (prefersLight ? 'light' : 'dark');
  document.querySelectorAll('.nav .theme').forEach(b=>b.addEventListener('click',()=>{
    root.dataset.theme = root.dataset.theme==='dark' ? 'light' : 'dark';
    try{ localStorage.setItem('theme', root.dataset.theme); }catch(e){}
  }));
  // mobile menu
  const nav=document.querySelector('.nav'), tog=document.querySelector('.navtoggle');
  if(tog){ tog.addEventListener('click',()=>{ const open=nav.classList.toggle('open'); tog.setAttribute('aria-expanded',open); }); }
  // write-ups dropdown: close on outside click or Escape
  const menu=document.querySelector('.nav details.menu');
  if(menu){
    document.addEventListener('click',e=>{ if(menu.open && !menu.contains(e.target)) menu.open=false; });
    document.addEventListener('keydown',e=>{ if(e.key==='Escape'){ menu.open=false; nav.classList.remove('open'); if(tog) tog.setAttribute('aria-expanded','false'); } });
  }
  // active section links (index) and active page
  const here=location.pathname.split('/').pop()||'index.html';
  document.querySelectorAll('.nav .links > a').forEach(a=>{ const h=a.getAttribute('href').split('#')[0]; if(h===here && !a.getAttribute('href').includes('#')) a.classList.add('active'); });
  document.querySelectorAll('.nav .panel a[aria-current]').forEach(a=>{ const sum=menu&&menu.querySelector('summary'); if(sum) sum.classList.add('active'); });
  // card glow follows the pointer
  document.querySelectorAll('.card').forEach(c=>c.addEventListener('pointermove',e=>{ const r=c.getBoundingClientRect(); c.style.setProperty('--mx',((e.clientX-r.left)/r.width*100)+'%'); }));
  // contents strip: highlight the section in view
  const toc=document.querySelector('.toc');
  if(toc && 'IntersectionObserver' in window){
    const links=[...toc.querySelectorAll('a')]; const map=new Map(links.map(a=>[a.getAttribute('href').slice(1),a]));
    const io=new IntersectionObserver(es=>{ es.forEach(e=>{ if(e.isIntersecting){ links.forEach(l=>l.classList.remove('on')); const l=map.get(e.target.id); if(l) l.classList.add('on'); } }); },{rootMargin:'-20% 0px -70% 0px'});
    map.forEach((a,id)=>{ const h=document.getElementById(id); if(h) io.observe(h); });
  }
  // scroll reveal (kept subtle; never leaves content hidden)
  const els=document.querySelectorAll('main > h2, main > p, main > table, main > figure, main > blockquote, main > .callout, main > .cards, main > .stats, main > ol, main > ul, main > #decoder, main > details, main > h3, main > .tg, main > .item');
  if(!('IntersectionObserver' in window) || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const rio=new IntersectionObserver(es=>es.forEach(e=>{ if(e.isIntersecting){ e.target.classList.add('in'); rio.unobserve(e.target);} }),{threshold:.05,rootMargin:'0px 0px -5% 0px'});
  els.forEach(el=>{ if(el.getBoundingClientRect().top < innerHeight*1.1) return; el.classList.add('reveal'); rio.observe(el); });
  setTimeout(()=>els.forEach(el=>el.classList.add('in')),2000);
})();
// render [{g:'972', p:'the', cls:''}, ...] as interlinear tiles into a container
function renderTiles(el, items){
  el.innerHTML='';
  for(const it of items){
    const t=document.createElement('span'); t.className='tile '+(it.cls||'');
    const p=document.createElement('span'); p.className='p'; p.textContent=it.p;
    const g=document.createElement('span'); g.className='g'; g.textContent=it.g||' ';
    t.appendChild(p); t.appendChild(g); el.appendChild(t);
  }
}
// 'show more' blocks on the home page
document.querySelectorAll('.showmore').forEach(b=>b.addEventListener('click',()=>{ const box=b.previousElementSibling; const open=box.hasAttribute('hidden'); if(open) box.removeAttribute('hidden'); else box.setAttribute('hidden',''); b.textContent = open ? 'Show fewer' : b.dataset.label || b.textContent; }));
document.querySelectorAll('.showmore').forEach(b=>b.dataset.label=b.textContent);
// big-news rotation: one panel at a time, every 9 s; pauses on hover, focus, hidden tab or the pause button; no auto-rotate under reduced motion
(function(){
  const box=document.querySelector('.bignews.bn-rot'); if(!box) return;
  const panels=[...box.querySelectorAll('.bn-panel')]; if(panels.length<2) return;
  const dots=box.querySelector('.bn-dots'), pauseBtn=box.querySelector('.bn-pause');
  let i=0, timer=null, paused=matchMedia('(prefers-reduced-motion: reduce)').matches, hovering=false;
  panels.forEach((p,k)=>{ const b=document.createElement('button'); b.type='button'; b.setAttribute('role','tab'); b.setAttribute('aria-label','Show item '+(k+1)); b.addEventListener('click',()=>{ go(k); restart(); }); dots.appendChild(b); });
  const db=[...dots.children];
  function go(k, instant){
    i=(k+panels.length)%panels.length;
    if(instant){ box.classList.add('instant'); requestAnimationFrame(()=>requestAnimationFrame(()=>box.classList.remove('instant'))); }
    panels.forEach((p,n)=>{ const on=n===i; p.classList.toggle('on',on); if(on) p.removeAttribute('hidden'); else if(instant) p.setAttribute('hidden',''); else setTimeout(()=>{ if(!p.classList.contains('on')) p.setAttribute('hidden',''); },650); });
    db.forEach((b,n)=>b.setAttribute('aria-selected', n===i?'true':'false'));
  }
  function tick(){ if(!paused && !hovering && !document.hidden) go(i+1); }
  function restart(){ clearInterval(timer); timer=setInterval(tick,9000); }
  function setPause(v){ paused=v; pauseBtn.setAttribute('aria-pressed',v); pauseBtn.setAttribute('aria-label',v?'Resume rotation':'Pause rotation'); pauseBtn.innerHTML=v?'&#9654;':'&#10074;&#10074;'; }
  box.querySelector('.bn-prev').addEventListener('click',()=>{ go(i-1); restart(); });
  box.querySelector('.bn-next').addEventListener('click',()=>{ go(i+1); restart(); });
  pauseBtn.addEventListener('click',()=>setPause(!paused));
  box.addEventListener('pointerenter',()=>hovering=true); box.addEventListener('pointerleave',()=>hovering=false);
  box.addEventListener('focusin',()=>hovering=true); box.addEventListener('focusout',e=>{ if(!box.contains(e.relatedTarget)) hovering=false; });
  box.addEventListener('keydown',e=>{ if(e.key==='ArrowLeft'){ go(i-1); restart(); } else if(e.key==='ArrowRight'){ go(i+1); restart(); } });
  if(paused) setPause(true);
  const start=/[?&]bn=(\d+)/.exec(location.search); // ?bn=N opens on panel N (1-based)
  go(start ? +start[1]-1 : 0, true); restart();
})();
// priority-queue filter: show one tier at a time
(function(){
  const btns=document.querySelectorAll('.qf'); if(!btns.length) return;
  const tiers=document.querySelectorAll('h3.tier');
  const cards=document.querySelectorAll('.tg');
  function apply(f, remember){
    cards.forEach(c=>{ c.hidden = !(f==='all' || c.classList.contains(f)); });
    tiers.forEach(t=>{ t.hidden = !(f==='all' || t.dataset.t===f); });
    btns.forEach(b=>b.classList.toggle('on', b.dataset.f===f));
    if(remember){ try{ history.replaceState(null,'',f==='live'?location.pathname:'#q='+f); }catch(e){} }
  }
  btns.forEach(b=>b.addEventListener('click',()=>apply(b.dataset.f, true)));
  const m=/^#q=(\w+)$/.exec(location.hash); apply(m ? m[1] : 'live', false);
  // each queue block shows three lines until clicked
  cards.forEach(c=>{ const p=c.querySelector('.tg-b p'); if(!p) return; const t=document.createElement('div'); t.className='tgmore'; t.textContent='more'; p.after(t);
    const toggle=()=>{ const on=c.classList.toggle('x'); t.textContent=on?'less':'more'; }; p.addEventListener('click',toggle); t.addEventListener('click',toggle); });
})();
// write-ups index: outcome / period / source chips, text search, state in the hash (writeups.html#kind=solved&q=rome)
(function(){
  const items=[...document.querySelectorAll('ul.wl li')]; if(!items.length) return;
  const chips=[...document.querySelectorAll('.wfilters .chip[data-facet]')], q=document.getElementById('wq'),
        count=document.getElementById('wcount'), reset=document.getElementById('wreset');
  const state={f:{}, q:''};
  function parse(){
    state.f={}; state.q='';
    location.hash.slice(1).split('&').forEach(kv=>{ if(!kv) return; const i=kv.indexOf('='); const k=i<0?kv:kv.slice(0,i), v=i<0?'':decodeURIComponent(kv.slice(i+1));
      if(k==='q') state.q=v; else if(k) state.f[k]=v.split(',').filter(Boolean); });
  }
  function apply(remember){
    chips.forEach(c=>c.setAttribute('aria-pressed', (state.f[c.dataset.facet]||[]).includes(c.dataset.val)?'true':'false'));
    if(q.value!==state.q) q.value=state.q;
    const needle=state.q.trim().toLowerCase(); let n=0;
    items.forEach(li=>{ let ok=true;
      for(const k in state.f){ const vs=state.f[k]; if(vs.length && !vs.includes(li.dataset[k])) ok=false; }
      if(ok && needle && !(li.dataset.q||'').includes(needle)) ok=false;
      li.hidden=!ok; if(ok) n++; });
    document.querySelectorAll('.wsec').forEach(s=>{ s.hidden=![...s.querySelectorAll('li')].some(li=>!li.hidden); });
    count.textContent = n===items.length ? 'All '+n+' entries' : n+' of '+items.length+' entries';
    if(remember){ const parts=[]; for(const k in state.f) if(state.f[k].length) parts.push(k+'='+state.f[k].join(','));
      if(needle) parts.push('q='+encodeURIComponent(state.q.trim()));
      try{ history.replaceState(null,'', parts.length ? '#'+parts.join('&') : location.pathname+location.search); }catch(e){} }
  }
  chips.forEach(c=>c.addEventListener('click',()=>{ const a=state.f[c.dataset.facet]=state.f[c.dataset.facet]||[]; const i=a.indexOf(c.dataset.val); if(i<0) a.push(c.dataset.val); else a.splice(i,1); apply(true); }));
  q.addEventListener('input',()=>{ state.q=q.value; apply(true); });
  reset.addEventListener('click',()=>{ state.f={}; state.q=''; apply(true); });
  window.addEventListener('hashchange',()=>{ parse(); apply(false); });
  parse(); apply(false);
})();
