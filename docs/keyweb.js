// The Key Web: keys.json + pages.json as a force-directed graph, letters pulled towards their year on the x axis.
(async()=>{
  const root=document.getElementById('kw'); if(!root || !window.d3) return;
  const still=matchMedia('(prefers-reduced-motion: reduce)').matches;
  const [K,pages]=await Promise.all([fetch('keys.json').then(r=>r.json()),fetch('pages.json').then(r=>r.json())]);
  const page=Object.fromEntries(pages.map(p=>[p.slug,p]));
  const esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const W=1000,H=820;

  const nodes=[], byId={};
  const add=n=>{ byId[n.id]=n; nodes.push(n); return n; };
  K.keys.forEach(k=>add({...k,type:'key'}));
  (K.sources||[]).forEach(s=>add({...s,type:'src'}));
  const links=[];
  for(const l of K.links){ const p=page[l.target]; if(!p || !byId[l.key]) continue;
    const t=byId['t:'+l.target]||add({id:'t:'+l.target,type:'t',slug:l.target,label:p.label,y:p.y,st:p.st,stt:p.stt});
    links.push({source:l.key,target:t.id,how:l.how||'',note:l.note||''}); }
  for(const l of (K.source_links||[])) if(byId[l.source] && byId[l.key]) links.push({source:l.source,target:l.key,how:'src'});
  // keys sit at the mean year of their letters; sources at the mean of their keys
  const deg={}; links.forEach(l=>{ deg[l.source]=(deg[l.source]||0)+1; deg[l.target]=(deg[l.target]||0)+1; });
  nodes.forEach(n=>{ n.deg=deg[n.id]||0; });
  const years=id=>links.filter(l=>l.source===id && byId[l.target].type==='t').map(l=>byId[l.target].y);
  K.keys.forEach(k=>{ const n=byId[k.id], ys=years(k.id); n.y0=ys.length?d3.mean(ys):(k.year||1600); });
  (K.sources||[]).forEach(s=>{ const ks=links.filter(l=>l.source===s.id).map(l=>byId[l.target].y0); byId[s.id].y0=ks.length?d3.mean(ks):1600; });
  nodes.forEach(n=>{ if(n.type==='t') n.y0=n.y; });
  const yr=d3.extent(nodes,n=>n.y0), x=d3.scaleLinear().domain([Math.floor(yr[0]/50)*50,Math.ceil(yr[1]/50)*50]).range([60,W-60]);
  nodes.forEach(n=>{ n.x=x(n.y0)+(Math.random()-.5)*20; n.y=H/2+(Math.random()-.5)*300; });

  const svg=d3.select(root).insert('svg',':first-child').attr('viewBox',`0 0 ${W} ${H}`).attr('role','img')
    .attr('aria-label','Network of cipher keys and the letters they read');
  const ax=svg.append('g').attr('class','axis');
  x.ticks(8).forEach(t=>{ ax.append('line').attr('x1',x(t)).attr('x2',x(t)).attr('y1',20).attr('y2',H-34);
    ax.append('text').attr('x',x(t)).attr('y',H-18).attr('text-anchor','middle').text(t); });
  const g=svg.append('g');
  const cls=h=>'lk '+(h==='src'?'src':/rebuilt/.test(h)?'rebuilt':/adapt/.test(h)?'adapted':/partial/.test(h)?'partial':'');
  const lk=g.append('g').selectAll('path').data(links).join('path').attr('class',l=>cls(l.how));
  const reads=n=>links.filter(l=>(l.source===n.id||l.target===n.id) && l.how!=='src').length;
  const nd=g.append('g').selectAll('g').data(nodes).join('g').attr('class',n=>'nd '+n.type+(n.st?' '+n.st:'')+(n.type==='key'&&reads(n)<2?' lone':'')+(n.type==='t'&&reads(n)>=2?' multi':''))
    .attr('tabindex',0).attr('role','button').attr('aria-label',n=>n.label);
  const KEYPATH='M-3,-2.5a4.5,4.5 0 1,1 0,5h10l2,-2.5l-2,-2.5z';          // a small key: bow and blade
  nd.filter(n=>n.type==='key').append('path').attr('d',KEYPATH).attr('transform',n=>`scale(${1.15+Math.min(n.deg,6)*.22})`);
  nd.filter(n=>n.type==='src').append('circle').attr('r',n=>8+Math.sqrt(n.deg)*2.2);
  nd.filter(n=>n.type==='t').append('circle').attr('r',n=>4+Math.min(n.deg,4));
  nd.append('text').attr('dy',n=>n.type==='t'?'-.8em':n.type==='src'?'2.2em':'1.9em').attr('text-anchor','middle')
    .text(n=>n.type==='t'?n.label.replace(/\s*\(.*?\)\s*/g,' ').trim():n.label);

  const sim=d3.forceSimulation(nodes)
    .force('link',d3.forceLink(links).id(n=>n.id).distance(l=>l.how==='src'?90:46).strength(l=>l.how==='src'?.15:.7))
    .force('charge',d3.forceManyBody().strength(n=>n.type==='t'?-70:-220))
    .force('x',d3.forceX(n=>x(n.y0)).strength(n=>n.type==='src'?.02:.22))
    .force('y',d3.forceY(H/2).strength(.06))
    .force('collide',d3.forceCollide(n=>n.type==='t'?16:26));
  const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
  function tick(){
    nodes.forEach(n=>{ n.x=clamp(n.x,30,W-30); n.y=clamp(n.y,30,H-50); });
    lk.attr('d',l=>{ const dx=l.target.x-l.source.x, dy=l.target.y-l.source.y, dr=Math.hypot(dx,dy)*1.6;
      return `M${l.source.x},${l.source.y}A${dr},${dr} 0 0,1 ${l.target.x},${l.target.y}`; });
    nd.attr('transform',n=>`translate(${n.x},${n.y})`);
  }
  sim.on('tick',tick);
  if(still){ sim.stop(); for(let i=0;i<300;i++) sim.tick(); tick(); }

  // drag
  nd.call(d3.drag().on('start',(e,n)=>{ if(!e.active) sim.alphaTarget(.2).restart(); n.fx=n.x; n.fy=n.y; })
    .on('drag',(e,n)=>{ n.fx=e.x; n.fy=e.y; }).on('end',(e,n)=>{ if(!e.active) sim.alphaTarget(0); n.fx=null; n.fy=null; }));

  // focus: a node, its links and neighbours
  const side=document.getElementById('kwside'), idle=side.innerHTML;
  const nb=n=>links.filter(l=>l.source===n||l.target===n);
  function focus(n){
    root.classList.toggle('focus',!!n);
    if(!n){ nd.classed('hot',false); lk.classed('hot',false); side.innerHTML=idle; return; }
    const ls=nb(n), set=new Set([n]); ls.forEach(l=>{ set.add(l.source); set.add(l.target); });
    nd.classed('hot',d=>set.has(d)); lk.classed('hot',l=>ls.includes(l));
    const item=(o,l)=>o.type==='t'?`<li><a href="${o.slug}.html">${esc(o.label)}</a><small>${esc(l.how)}${l.note?' &middot; '+esc(l.note):''} &middot; ${esc(o.stt)}</small></li>`
                                   :`<li><b>${esc(o.label)}</b><small>${esc(l.how==='src'?'published or held by':l.how)}${l.note?' &middot; '+esc(l.note):''}</small></li>`;
    const other=l=>l.source===n?l.target:l.source;
    if(n.type==='key') side.innerHTML=`<p class="k">Key &middot; ${esc(n.kind||'')}</p><h3>${esc(n.label)}</h3>${n.by?`<p>${esc(n.by)}${n.year?', '+n.year:''}</p>`:''}<p>${esc(n.note||'')}</p>
      <ul>${ls.filter(l=>l.how!=='src').map(l=>item(other(l),l)).join('')}</ul>`;
    else if(n.type==='src') side.innerHTML=`<p class="k">Source</p><h3>${esc(n.label)}</h3><ul>${ls.map(l=>`<li><b>${esc(other(l).label)}</b><small>${other(l).deg-1} letter${other(l).deg===2?'':'s'}</small></li>`).join('')}</ul>`;
    else side.innerHTML=`<p class="k">Letter &middot; ${esc(n.stt)}</p><h3><a href="${n.slug}.html">${esc(n.label)}</a></h3><p>Read with:</p><ul>${ls.map(l=>item(other(l),l)).join('')}</ul>`;
  }
  let pinned=null;
  nd.on('pointerenter',(e,n)=>{ if(!pinned) focus(n); }).on('pointerleave',()=>{ if(!pinned) focus(null); })
    .on('focus',(e,n)=>focus(n))
    .on('click',(e,n)=>{ if(n.type==='t' && pinned===n){ location.href=n.slug+'.html'; return; } pinned=pinned===n?null:n; focus(pinned||n); })
    .on('keydown',(e,n)=>{ if(e.key==='Enter' && n.type==='t') location.href=n.slug+'.html'; });
  svg.on('click',e=>{ if(e.target===svg.node()){ pinned=null; focus(null); } });

  const multi=K.keys.filter(k=>links.filter(l=>l.source===byId[k.id] && l.how!=='src').length>=2).length, tset=nodes.filter(n=>n.type==='t').length;
  document.getElementById('kwstats').innerHTML=`<span><b>${K.keys.length}</b>keys</span><span><b>${tset}</b>letters and series read with them</span><span><b>${multi}</b>keys that read more than one</span>`;
})();
