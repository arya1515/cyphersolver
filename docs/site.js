// shared behaviour: nav highlight, scroll-reveal, card glow follow, interlinear tile renderer
(function(){
  const here=location.pathname.split('/').pop()||'index.html';
  document.querySelectorAll('.nav .links a').forEach(a=>{ if(a.getAttribute('href')===here) a.classList.add('active'); });
  document.querySelectorAll('.card').forEach(c=>c.addEventListener('pointermove',e=>{ const r=c.getBoundingClientRect(); c.style.setProperty('--mx',((e.clientX-r.left)/r.width*100)+'%'); }));
  const els=document.querySelectorAll('main > h2, main > p, main > table, main > figure, main > blockquote, main > .callout, main > .cards, main > .stats, main > ol, main > ul, main > #decoder, main > details, main > h3');
  if(!('IntersectionObserver' in window) || matchMedia('(prefers-reduced-motion: reduce)').matches){ return; }
  const io=new IntersectionObserver(es=>es.forEach(e=>{ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target);} }),{threshold:.05,rootMargin:'0px 0px -5% 0px'});
  els.forEach(el=>{ if(el.getBoundingClientRect().top < innerHeight*1.1){ return; } el.classList.add('reveal'); io.observe(el); });
  setTimeout(()=>els.forEach(el=>el.classList.add('in')),2500);   // never leave content hidden
})();
// render [{g:'972', p:'the', cls:''}, ...] as interlinear tiles into a container
function renderTiles(el, items){
  el.innerHTML='';
  for(const it of items){
    const t=document.createElement('span'); t.className='tile '+(it.cls||'');
    const p=document.createElement('span'); p.className='p'; p.textContent=it.p;
    const g=document.createElement('span'); g.className='g'; g.textContent=it.g||'\u00a0';
    t.appendChild(p); t.appendChild(g); el.appendChild(t);
  }
}
