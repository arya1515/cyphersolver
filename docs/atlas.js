// The Cipher Atlas: atlas.json (places, letters) + pages.json (labels, outcomes) drawn on Natural Earth land with d3.
(async()=>{
  const root=document.getElementById('atlas'); if(!root || !window.d3) return;
  const still=matchMedia('(prefers-reduced-motion: reduce)').matches;
  const [atlas,pages,world]=await Promise.all([
    fetch('atlas.json').then(r=>r.json()), fetch('pages.json').then(r=>r.json()).catch(()=>[]),
    fetch('https://cdn.jsdelivr.net/npm/world-atlas@2/land-50m.json').then(r=>r.json())]);
  const page=Object.fromEntries(pages.map(p=>[p.slug,p]));
  const ST={solved:'read',found:'explained / found read',partial:'read in part',stuck:'attempted'};
  const esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const W=1200,H=700;
  const land=topojson.feature(world,world.objects.land);
  const proj=d3.geoConicConformal().rotate([-14,0]).parallels([38,58])
    .fitExtent([[10,40],[W-10,H-10]],{type:'MultiPoint',coordinates:[[-10,35.5],[36,36],[30,61],[-8,58]]});
  const path=d3.geoPath(proj);
  const svg=d3.select(root).insert('svg',':first-child').attr('viewBox',`0 0 ${W} ${H}`).attr('role','img')
    .attr('aria-label','Map of Europe with the routes of the ciphered letters');
  svg.append('rect').attr('class','sea').attr('width',W).attr('height',H);
  const g=svg.append('g');
  g.append('path').attr('class','grat').attr('d',path(d3.geoGraticule10()));
  g.append('path').attr('class','land').attr('d',path(land));
  const gArcs=g.append('g'), gHits=g.append('g'), gCities=g.append('g'), gPulse=g.append('g');

  const P=name=>{ const c=atlas.places[name]; return c?proj([c[1],c[0]]):null; };
  const letters=atlas.letters.map((l,i)=>({...l,i,a:P(l.from),b:P(l.to),pg:page[l.slug]})).filter(l=>l.a && l.b)
    .sort((x,y)=>x.year-y.year);
  const curve=l=>{ const [x0,y0]=l.a,[x1,y1]=l.b, dx=x1-x0, dy=y1-y0, d=Math.hypot(dx,dy)||1;
    if(d<2) return `M${x0},${y0}m-4,0a4,4 0 1,0 8,0a4,4 0 1,0 -8,0`;
    const k=Math.min(.32,40/d+.12), mx=(x0+x1)/2-dy*k, my=(y0+y1)/2+dx*k; return `M${x0},${y0}Q${mx},${my} ${x1},${y1}`; };
  const arcs=gArcs.selectAll('path').data(letters).join('path').attr('class',l=>'arc '+l.st).attr('d',curve)
    .attr('stroke-width',1.6).attr('opacity',0).attr('vector-effect','non-scaling-stroke');
  arcs.each(function(l){ l.len=this.getTotalLength(); l.el=this; });
  const hits=gHits.selectAll('path').data(letters).join('path').attr('class','arc hit').attr('d',curve).attr('vector-effect','non-scaling-stroke');
  hits.each(function(l){ l.hit=this; });

  // cities, sized by traffic
  const cnt={}; letters.forEach(l=>{ cnt[l.from]=(cnt[l.from]||0)+1; cnt[l.to]=(cnt[l.to]||0)+1; });
  const cities=Object.keys(cnt).map(n=>({n,p:P(n),c:cnt[n]})).sort((a,b)=>b.c-a.c);
  const cg=gCities.selectAll('g').data(cities).join('g').attr('class','city').attr('transform',d=>`translate(${d.p})`);
  cg.append('circle').attr('r',d=>1.6+Math.sqrt(d.c)*1.1);
  cg.filter(d=>d.c>=5).append('text').attr('x',d=>4+Math.sqrt(d.c)*1.1).attr('dy','.35em').text(d=>d.n);

  // zoom and pan
  const zoom=d3.zoom().scaleExtent([.6,10]).on('zoom',e=>{ g.attr('transform',e.transform);
    cg.attr('transform',d=>`translate(${d.p}) scale(${1/Math.sqrt(e.transform.k)})`); });
  svg.call(zoom).on('dblclick.zoom',null);

  // legend filters
  const on=new Set(Object.keys(ST));
  const legend=d3.select('#alegend').selectAll('button').data(Object.keys(ST)).join('button').attr('type','button')
    .attr('aria-pressed','true').html(s=>`<i style="background:var(--${{solved:'green',found:'blue',partial:'amber',stuck:'red'}[s]})"></i>${ST[s]}`)
    .on('click',function(e,s){ on.has(s)?on.delete(s):on.add(s); this.setAttribute('aria-pressed',on.has(s)); draw(T,false); });

  // histogram by decade
  const hist=d3.select('#ahist').attr('viewBox','0 0 525 38'), bins=d3.range(1420,1950,10).map(y=>({y,n:letters.filter(l=>l.year>=y&&l.year<y+10).length}));
  const hy=d3.scaleLinear().domain([0,d3.max(bins,b=>b.n)]).range([0,36]);
  const bars=hist.selectAll('rect').data(bins).join('rect').attr('x',b=>b.y-1420+.5).attr('width',9).attr('y',b=>38-hy(b.n)).attr('height',b=>hy(b.n));

  const tip=document.getElementById('atip'), yearEl=document.getElementById('ayear'), countEl=document.getElementById('acount'),
        feed=document.getElementById('afeed'), slider=document.getElementById('aslider');
  let T=1945, shown=new Set();
  function pulse(l){ if(still) return; gPulse.append('circle').attr('class','pulse').attr('cx',l.b[0]).attr('cy',l.b[1]).attr('r',2)
    .attr('vector-effect','non-scaling-stroke').transition().duration(900).attr('r',18).style('opacity',0).remove(); }
  function draw(t,animate){
    T=t; yearEl.textContent=Math.floor(t); slider.value=Math.floor(t);
    let n=0, newest=null;
    for(const l of letters){
      const vis=l.year<=t && on.has(l.st), age=t-l.year;
      if(vis){ n++;
        const op=Math.max(.22,1-age/70); l.el.style.opacity=op; l.el.classList.toggle('fresh',age<4);
        if(!shown.has(l.i)){ shown.add(l.i);
          if(animate && !still){ l.el.style.strokeDasharray=l.len; l.el.style.strokeDashoffset=l.len;
            d3.select(l.el).transition().duration(1100).ease(d3.easeCubicOut).style('stroke-dashoffset',0).on('end',()=>{ l.el.style.strokeDasharray=''; pulse(l); });
            newest=l; } }
      } else { l.el.style.opacity=0; shown.delete(l.i); }
      l.hit.style.display=vis?'':'none';
    }
    bars.attr('class',b=>b.y<=t?'on':null);
    countEl.textContent=`${n} letter${n===1?'':'s'} on the map`;
    if(newest) feed.innerHTML=`<b>${esc(newest.date||Math.floor(newest.year))}</b> &middot; ${esc(newest.from)} &rarr; ${esc(newest.to)} &middot; <a href="${newest.slug}.html">${esc(newest.pg?newest.pg.label:newest.label)}</a>`;
  }
  // tooltip + neighbourhood
  hits.on('pointerenter',(e,l)=>{
      svg.classed('dim',true); arcs.classed('hot',d=>d.slug===l.slug);
      tip.innerHTML=`<b>${esc(l.pg?l.pg.label:l.label)}</b>${esc(l.from)} &rarr; ${esc(l.to)}<br><span>${esc(l.date||Math.floor(l.year))} &middot; ${esc(l.pg?l.pg.stt:ST[l.st])}</span>`;
      tip.style.opacity=1; })
    .on('pointermove',e=>{ const r=root.getBoundingClientRect(); let x=e.clientX-r.left+14, y=e.clientY-r.top+14;
      if(x>r.width-290) x-=300; tip.style.left=x+'px'; tip.style.top=y+'px'; })
    .on('pointerleave',()=>{ svg.classed('dim',false); arcs.classed('hot',false); tip.style.opacity=0; })
    .on('click',(e,l)=>{ location.href=l.slug+'.html'; });

  // play
  const btn=document.getElementById('aplay'); let raf=0, last=0;
  function stop(){ cancelAnimationFrame(raf); raf=0; btn.innerHTML='&#9654; Play'; btn.setAttribute('aria-label','Play through time'); }
  function step(now){ const dt=Math.min(.1,(now-last)/1000); last=now;
    const busy=letters.some(l=>l.year>T && l.year<T+6);            // slow down where the letters are, hurry through empty years
    const t=T+dt*(busy?14:60); draw(Math.min(t,1945),true); if(t>=1945){ stop(); return; } raf=requestAnimationFrame(step); }
  btn.addEventListener('click',()=>{ if(raf){ stop(); return; } if(T>=1944) { shown.clear(); draw(1420,false); }
    btn.innerHTML='&#10074;&#10074; Pause'; btn.setAttribute('aria-label','Pause'); last=performance.now(); raf=requestAnimationFrame(step); });
  slider.addEventListener('input',()=>{ stop(); draw(+slider.value,true); });
  document.getElementById('aall').addEventListener('click',()=>{ stop(); draw(1945,false); });

  // busiest routes
  const routes=d3.rollups(letters,v=>({n:v.length,slugs:new Set(v.map(l=>l.slug)).size,y0:d3.min(v,l=>l.year),y1:d3.max(v,l=>l.year)}),l=>l.from+' → '+l.to)
    .sort((a,b)=>b[1].n-a[1].n).slice(0,9);
  document.getElementById('atop').innerHTML=routes.map(([r,v])=>`<div><b>${esc(r)}</b><span>${v.n} letters &middot; ${v.slugs} write-up${v.slugs>1?'s':''} &middot; ${Math.floor(v.y0)}${v.y1-v.y0>=1?'&ndash;'+Math.floor(v.y1):''}</span></div>`).join('');

  // open on the whole map, then play once the map is in view
  draw(1945,false);
  if(!still && 'IntersectionObserver' in window){
    const io=new IntersectionObserver(es=>{ if(es[0].isIntersecting){ io.disconnect(); shown.clear(); draw(1420,false); btn.click(); } },{threshold:.5});
    io.observe(root);
  }
})();
