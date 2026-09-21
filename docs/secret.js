// Write a secret letter: encipher a message with one of the site's rebuilt keys (secret-keys.json), draw it as a letter
// on aged paper with a wax seal (canvas, downloadable), or share a link that carries only the ciphertext.
(async()=>{
  const $=id=>document.getElementById(id);
  const K=(await (await fetch('secret-keys.json')).json()).keys, byId=Object.fromEntries(K.map(k=>[k.id,k]));
  const SITE='dbourdeau.github.io/cyphersolver';
  const fold=s=>s.normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase();
  const pick=a=>a[Math.floor(Math.random()*a.length)];

  // ---------------------------------------------------------------- enciphering
  // tokens: {g, p} cipher group and its value; {g:'', p, cls:'plain'} left in clear; {g:'|', p:' ', cls:'null'} word gap (pigpen)
  function encipher(key, text){
    const out=[], t=fold(text).replace(/[’`]/g,"'");
    if(key.kind==='code') return encCode(key,t);
    const phrases=Object.keys(key.enc).filter(p=>p.length>1).sort((a,b)=>b.length-a.length);
    let i=0;
    while(i<t.length){
      const c=t[i];
      if(/\s/.test(c)){ if(key.kind==='pigpen' && out.length && out[out.length-1].g!=='|') out.push({g:'|',p:' ',cls:'null'}); i++; continue; }
      // whole-word codes (de, la, le roi, Monsieur...) only at word boundaries
      const ph=phrases.find(p=>t.startsWith(p,i) && (i===0||/[^a-z]/.test(t[i-1])) && !/[a-z]/.test(t[i+p.length]||''));
      if(ph){ out.push({g:pick(key.enc[ph]),p:ph,cls:ph.length>2?'code':''}); i+=ph.length; continue; }
      const l=key.fold[c]&&!key.enc[c]?key.fold[c]:c;
      if(key.enc[l]) out.push({g:pick(key.enc[l]),p:l});
      else if(/[a-z0-9]/.test(c)) out.push({g:'',p:c,cls:'plain'});
      i++;
    }
    while(out.length && out[out.length-1].g==='|') out.pop();
    return out;
  }
  // a numbered code: whole words first, then the longest syllables that spell the word, else the word in clear
  let codeIdx=null;
  function encCode(key,t){
    if(!codeIdx){ codeIdx=new Map(); for(const [p,gs] of Object.entries(key.enc)) codeIdx.set(p.toLowerCase(),gs); }
    const parts=Object.keys(key.enc).map(p=>p.toLowerCase()).filter(p=>/^[a-z]+$/.test(p)).sort((a,b)=>b.length-a.length);
    const out=[];
    for(const w of t.match(/[a-z]+|[0-9]+/g)||[]){
      if(codeIdx.has(w)){ out.push({g:pick(codeIdx.get(w)),p:w}); continue; }
      // cheapest spelling by dynamic programming over the syllables
      const best=new Array(w.length+1).fill(null); best[0]=[];
      for(let i=0;i<w.length;i++){ if(!best[i]) continue;
        for(const p of parts){ if(w.startsWith(p,i)){ const j=i+p.length, cand=best[i].concat([p]);
          if(!best[j] || cand.length<best[j].length) best[j]=cand; } } }
      if(best[w.length]) best[w.length].forEach((p,k)=>out.push({g:pick(codeIdx.get(p)),p,cls:k?'unc':''}));
      else out.push({g:'',p:w,cls:'plain'});
    }
    return out;
  }

  // ---------------------------------------------------------------- the letter
  const cv=$('letter'), ctx=cv.getContext('2d');
  let fontsReady=document.fonts?Promise.all([document.fonts.load('40px "IM Fell English"'),document.fonts.load('italic 26px "IM Fell English"')]).catch(()=>{}):Promise.resolve();
  const PAPER=(()=>{ // grain drawn once, reused
    const c=document.createElement('canvas'); c.width=550; c.height=700; const x=c.getContext('2d');
    const im=x.createImageData(c.width,c.height);
    for(let i=0;i<im.data.length;i+=4){ const n=Math.random()*38; im.data[i]=120+n; im.data[i+1]=95+n; im.data[i+2]=55+n; im.data[i+3]=Math.random()<.5?10:0; }
    x.putImageData(im,0,0); return c; })();
  function seeded(seed){ let s=seed>>>0||1; return ()=>{ s^=s<<13; s^=s>>>17; s^=s<<5; return ((s>>>0)%10000)/10000; }; }
  function paper(W,H,rand){
    ctx.clearRect(0,0,W,H); ctx.beginPath(); ctx.roundRect(0,0,W,H,Math.round(Math.min(W,H)*.035)); ctx.clip();   // rounded sheet, in the PNG too
    ctx.fillStyle='#ecdcb8'; ctx.fillRect(0,0,W,H);
    const g=ctx.createRadialGradient(W/2,H*.45,Math.min(W,H)*.25,W/2,H/2,Math.max(W,H)*.75);
    g.addColorStop(0,'rgba(255,248,225,.35)'); g.addColorStop(.7,'rgba(150,110,50,.12)'); g.addColorStop(1,'rgba(90,60,20,.45)');
    ctx.fillStyle=g; ctx.fillRect(0,0,W,H);
    for(let i=0;i<5;i++){ const x=rand()*W, y=rand()*H, r=40+rand()*140, s=ctx.createRadialGradient(x,y,r*.2,x,y,r);
      s.addColorStop(0,'rgba(140,95,35,.06)'); s.addColorStop(.85,'rgba(140,95,35,.10)'); s.addColorStop(1,'rgba(140,95,35,0)'); ctx.fillStyle=s; ctx.fillRect(x-r,y-r,2*r,2*r); }
    ctx.save(); ctx.globalAlpha=.9; for(let y=0;y<H;y+=PAPER.height) for(let x=0;x<W;x+=PAPER.width) ctx.drawImage(PAPER,x,y); ctx.restore();
    // the fold
    const f=ctx.createLinearGradient(0,H/2-14,0,H/2+14); f.addColorStop(0,'rgba(90,60,20,0)'); f.addColorStop(.5,'rgba(90,60,20,.14)'); f.addColorStop(.52,'rgba(255,250,235,.25)'); f.addColorStop(1,'rgba(90,60,20,0)');
    ctx.fillStyle=f; ctx.fillRect(0,H/2-14,W,28);
  }
  function pigpen(x,y,s,g){ // box shape by grid position, dot below or inside
    const i=+g[0], dot=g[1], L=x, R=x+s, T=y-s, B=y;
    const sides={0:'rb',1:'lrb',2:'lb',3:'trb',4:'tlrb',5:'tlb',6:'tr',7:'tlr',8:'tl'}[i];
    ctx.beginPath();
    if(sides.includes('t')){ ctx.moveTo(L,T); ctx.lineTo(R,T); }
    if(sides.includes('b')){ ctx.moveTo(L,B); ctx.lineTo(R,B); }
    if(sides.includes('l')){ ctx.moveTo(L,T); ctx.lineTo(L,B); }
    if(sides.includes('r')){ ctx.moveTo(R,T); ctx.lineTo(R,B); }
    ctx.stroke();
    if(dot){ ctx.beginPath(); ctx.arc(x+s/2, dot==='.'?B+s*.32:y-s/2, s*.09,0,7); ctx.fill(); }
  }
  function seal(cx,cy,r,letter,rand){
    ctx.save(); ctx.translate(cx,cy); ctx.rotate(-.2);
    ctx.fillStyle='rgba(60,10,5,.35)'; ctx.beginPath(); ctx.ellipse(6,9,r*1.05,r*1.02,0,0,7); ctx.fill();
    // an irregular blob of wax
    ctx.beginPath(); for(let a=0;a<=Math.PI*2+.01;a+=Math.PI/18){ const rr=r*(1+(rand()-.5)*.1); ctx.lineTo(Math.cos(a)*rr,Math.sin(a)*rr); } ctx.closePath();
    const g=ctx.createRadialGradient(-r*.35,-r*.4,r*.1,0,0,r*1.05); g.addColorStop(0,'#d8574a'); g.addColorStop(.45,'#9b2a22'); g.addColorStop(1,'#5a120d');
    ctx.fillStyle=g; ctx.fill();
    ctx.lineWidth=r*.07; ctx.strokeStyle='rgba(60,8,5,.55)'; ctx.beginPath(); ctx.arc(0,0,r*.72,0,7); ctx.stroke();
    ctx.lineWidth=r*.025; ctx.strokeStyle='rgba(255,190,170,.35)'; ctx.beginPath(); ctx.arc(-1,-1.5,r*.72,0,7); ctx.stroke();
    ctx.setLineDash([r*.05,r*.07]); ctx.lineWidth=r*.03; ctx.strokeStyle='rgba(60,8,5,.5)'; ctx.beginPath(); ctx.arc(0,0,r*.6,0,7); ctx.stroke(); ctx.setLineDash([]);
    ctx.font=`${Math.round(r*.78)}px "IM Fell English", Georgia, serif`; ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.fillStyle='rgba(50,6,4,.75)'; ctx.fillText(letter,1.5,4); ctx.fillStyle='rgba(255,200,185,.28)'; ctx.fillText(letter,-.5,2);
    ctx.restore();
  }
  function draw(key,tokens,sig,seed){
    const rand=seeded(seed), W=1100, M=110, ink='#2b1c0e';
    const fs=key.kind==='pigpen'?0:(key.kind==='code'?40:44), gap=key.kind==='pigpen'?10:18, lh=key.kind==='pigpen'?74:66;
    ctx.font=`${fs||40}px "IM Fell English", Georgia, serif`;
    // lay the groups out first to know the height
    const lines=[[]]; let x=0;
    for(const t of tokens){
      const txt=t.g||t.p, w=key.kind==='pigpen'?(t.g==='|'?26:34):ctx.measureText(txt).width + (t.cls==='plain'?4:0);
      if(t.g==='|' && x===0) continue;
      if(x+w>W-2*M && lines[lines.length-1].length){ lines.push([]); x=0; if(t.g==='|') continue; }
      lines[lines.length-1].push({t,w,x}); x+=w+gap;
    }
    const H=Math.max(1150, 360+lines.length*lh+(sig?120:0)+330);
    cv.height=H; paper(W,H,rand);
    ctx.fillStyle=ink; ctx.strokeStyle=ink; ctx.textBaseline='alphabetic';
    ctx.font='italic 26px "IM Fell English", Georgia, serif'; ctx.globalAlpha=.8;
    ctx.fillText(`In the cipher of ${key.who}, ${key.year}`,M,150);
    ctx.globalAlpha=1; ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(M,172); ctx.lineTo(M+180,172); ctx.stroke();
    let y=270;
    for(const line of lines){
      for(const {t,w,x} of line){
        const jx=(rand()-.5)*2, jy=(rand()-.5)*3;
        ctx.globalAlpha=.78+rand()*.22;
        if(key.kind==='pigpen'){ if(t.g!=='|'){ ctx.lineWidth=2.8; ctx.lineCap='round'; pigpen(M+x+jx,y+jy,30,t.g); } }
        else{ ctx.font=(t.cls==='plain'?'italic ':'')+`${fs}px "IM Fell English", Georgia, serif`; ctx.fillText(t.g||t.p,M+x+jx,y+jy); }
      }
      y+=lh;
    }
    ctx.globalAlpha=1;
    if(sig){ ctx.font='italic 40px "IM Fell English", Georgia, serif'; ctx.textAlign='right'; ctx.fillText(sig,W-M,y+60); ctx.textAlign='left'; }
    seal(M+90,H-230,78,key.seal||key.who[0],rand);
    ctx.font='21px "IM Fell English", Georgia, serif'; ctx.globalAlpha=.72; ctx.textAlign='right';
    ctx.fillText('Can you read it? The key is at',W-M,H-120);
    ctx.font='22px "JetBrains Mono", Consolas, monospace'; ctx.fillText(SITE+'/'+key.slug+'.html',W-M,H-88);
    ctx.textAlign='left'; ctx.globalAlpha=1;
  }

  // ---------------------------------------------------------------- the page
  let key=K[0], tokens=[], seed=Date.now()%100000;
  const msg=$('msg'), sig=$('sig');
  $('keys').innerHTML=K.map(k=>`<button type="button" class="sl-key" data-k="${k.id}" aria-pressed="false"><b>${k.name}</b><span>${k.who}, ${k.year}</span><i></i></button>`).join('');
  const btns=[...document.querySelectorAll('.sl-key')];
  function sample(k){ const t=encipher(k,'burn this letter'); return k.kind==='pigpen'?'☐ ⊔ ┗ ┓ · ☐':t.map(x=>x.g||x.p).filter(g=>g!=='|').join(' '); }
  btns.forEach(b=>{ b.querySelector('i').textContent=sample(byId[b.dataset.k]); b.addEventListener('click',()=>{ key=byId[b.dataset.k]; update(true); }); });
  function update(reroll){
    if(reroll) seed=Math.floor(Math.random()*1e6);
    btns.forEach(b=>b.setAttribute('aria-pressed',b.dataset.k===key.id));
    $('keynote').innerHTML=`${key.note} <a href="${key.slug}.html">The write-up &rarr;</a>`;
    const r=Math.random; Math.random=seeded(seed); tokens=encipher(key,msg.value); Math.random=r;
    const n=tokens.filter(t=>t.g&&t.g!=='|').length, clear=tokens.filter(t=>t.cls==='plain').length;
    $('count').textContent=`${msg.value.length} / 400`;
    $('stats').textContent=`${n} ${key.kind==='code'?'code groups':key.kind==='pigpen'?'signs':'figures'}`+(clear?`, ${clear} left in clear (the key has no sign for them)`:'');
    fontsReady.then(()=>draw(key,tokens,sig.value.trim(),seed));
  }
  let tmr=0; const later=()=>{ clearTimeout(tmr); tmr=setTimeout(()=>update(false),120); };
  msg.addEventListener('input',later); sig.addEventListener('input',later);
  $('reroll').addEventListener('click',()=>update(true));
  const say=t=>{ $('status').textContent=t; setTimeout(()=>{ if($('status').textContent===t) $('status').textContent=''; },4000); };
  $('dl').addEventListener('click',()=>cv.toBlob(b=>{ const a=document.createElement('a'); a.href=URL.createObjectURL(b);
    a.download=`secret-letter-${key.id}.png`; a.click(); setTimeout(()=>URL.revokeObjectURL(a.href),4000); say('Letter saved.'); },'image/png'));
  // the sealed link: key, groups (clear words prefixed with ~), signature; never the plaintext
  const pack=()=>tokens.map(t=>t.g==='|'?'|':t.g||('~'+t.p)).join('.');
  $('link').addEventListener('click',async()=>{
    const url=`${location.origin}${location.pathname}#k=${key.id}&c=${encodeURIComponent(pack())}`+(sig.value.trim()?`&s=${encodeURIComponent(sig.value.trim())}`:'');
    try{ await navigator.clipboard.writeText(url); say('Sealed link copied. Only the ciphertext travels in it.'); }catch(e){ prompt('Copy this link',url); }
  });

  // ---------------------------------------------------------------- receiving a sealed link
  const h=new URLSearchParams(location.hash.slice(1));
  if(h.get('k') && h.get('c') && byId[h.get('k')]){
    const k=byId[h.get('k')], c=h.get('c').split('.'), s=h.get('s')||'';
    const tk=c.map(g=>g==='|'?{g:'|',p:' ',cls:'null'}:g[0]==='~'?{g:'',p:g.slice(1),cls:'plain'}:{g,p:k.dec[g]??'?',cls:k.dec[g]?'':'unk'})
      .filter(t=>!(k.kind==='pigpen' && t.g==='|'));
    key=k; tokens=c.map(g=>g==='|'?{g:'|',p:' ',cls:'null'}:g[0]==='~'?{g:'',p:g.slice(1),cls:'plain'}:{g,p:k.dec[g]||'?'});
    $('recv').hidden=false;
    $('recv-h').textContent=s?`${s} has sent you a letter in cipher`:'Someone has sent you a letter in cipher';
    $('recv-p').innerHTML=`It is written in the cipher of ${k.who}, ${k.year}. Scroll down and it will decipher itself with the key rebuilt on <a href="${k.slug}.html">that write-up</a>; hover a group to see every place it recurs. Then write one back.`;
    const data={title:`A letter in the cipher of ${k.who.split(',')[0]}`,unit:k.kind==='code'?'code groups':k.kind==='pigpen'?'signs':'figures',
      caption:`Sent with a sealed link from ${SITE}/secret.html.`,key_note:k.note,tokens:tk};
    const fig=$('recv-reveal'); fig.dataset.src=URL.createObjectURL(new Blob([JSON.stringify(data)],{type:'application/json'}));
    const s2=document.createElement('script'); s2.src='cipher-reveal.js?again'; document.body.appendChild(s2);
    msg.value=''; sig.value='';
    btns.forEach(b=>b.setAttribute('aria-pressed',b.dataset.k===key.id));
    $('keynote').innerHTML=`${key.note} <a href="${key.slug}.html">The write-up &rarr;</a>`;
    fontsReady.then(()=>draw(key,tokens,s,seed));
    msg.addEventListener('focus',()=>{ if(!msg.value) update(false); },{once:true});
  } else update(true);
})();
