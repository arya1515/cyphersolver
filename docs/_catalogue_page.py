"""Build docs/catalogue.html and the tables in ../CATALOGUE.md from ../catalogue.json.

Run from docs/:  python _catalogue_page.py   then   python _build_site.py   (nav, footer, contents strip).

catalogue.json is the single source: entries with 1-5 scores for importance, solvability and difficulty.
The page embeds the JSON and computes a priority score client-side from adjustable weights; it also renders a
static table for readers without JavaScript. CATALOGUE.md gets its table (counted entries, default weights) and
its "Also noted" list rewritten between <!-- table:start --> / <!-- table:end --> and <!-- also:start --> /
<!-- also:end --> markers; the prose around them is hand-written and left alone.
"""
import json, html, pathlib, re

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent
DATA = json.loads((ROOT / 'catalogue.json').read_text(encoding='utf-8'))
W = DATA['weights_default']
GALLICA = 'https://gallica.bnf.fr/ark:/12148/'


def priority(e, w=W):
    """0-10: weighted mean of importance, solvability and ease (6 - difficulty), each 1-5, rescaled."""
    tot = w['importance'] + w['solvability'] + w['ease']
    v = (w['importance'] * e['importance'] + w['solvability'] * e['solvability'] + w['ease'] * (6 - e['difficulty'])) / tot
    return round((v - 1) / 4 * 10, 1)


def esc(t):
    return html.escape(str(t), quote=False)


def ark_links(e):
    out = []
    for k in ('ark', 'ark2'):
        a = e.get(k)
        if a: out.append(f'<a href="{GALLICA}{a}" rel="noopener">{a}</a>')
    return ' · '.join(out)


# ---------- Markdown ----------
def md_table(entries):
    rows = ['| Prio. | # | Date | Item | Shelfmark / access | Status & prior art | Why it matters | Imp. | Solv. | Diff. | Cls | Seen |',
            '|---|---|---|---|---|---|---|---|---|---|---|---|']
    for e in entries:
        arks = '; '.join(f'ark {e[k]}' for k in ('ark', 'ark2') if e.get(k))
        shelf = e['shelfmark'] + (f' ({arks})' if arks else '') + (f'; {e["folio_note"]}' if e.get('folio_note') else '')
        seen = '●' if e['seen'] == 'image' else '◇'
        rows.append(f"| **{priority(e)}** | {e['id']} | {e['date']} | {e['title']}: {e['correspondents']} | {shelf} | {e['status']} | {e['why']} | {e['importance']} | {e['solvability']} | {e['difficulty']} | {e['cls']} | {seen} |")
    return '\n'.join(rows)


def md_also(entries):
    out = []
    for e in entries:
        arks = ', '.join(f'ark {e[k]}' for k in ('ark', 'ark2') if e.get(k))
        out.append(f"- **{e['title']}**, {e['date']}, {e['shelfmark']}{(', ' + arks) if arks else ''}. {e['status']} {e['why']} "
                   f"Imp. {e['importance']}, solv. {e['solvability']}, diff. {e['difficulty']}, class {e['cls']}, priority {priority(e)}.")
    return '\n'.join(out)


def update_md():
    p = ROOT / 'CATALOGUE.md'
    s = p.read_text(encoding='utf-8')
    counted = sorted([e for e in DATA['entries'] if e['counted']], key=lambda e: (-priority(e), e['id']))
    also = sorted([e for e in DATA['entries'] if not e['counted']], key=lambda e: (-priority(e), e['id']))
    s = re.sub(r'<!-- table:start -->.*?<!-- table:end -->', lambda m: '<!-- table:start -->\n' + md_table(counted) + '\n<!-- table:end -->', s, flags=re.S)
    s = re.sub(r'<!-- also:start -->.*?<!-- also:end -->', lambda m: '<!-- also:start -->\n' + md_also(also) + '\n<!-- also:end -->', s, flags=re.S)
    p.write_text(s, encoding='utf-8')


# ---------- HTML ----------
def static_rows(entries):
    out = []
    for e in entries:
        out.append(f"<tr><td>{priority(e)}</td><td>{e['id']}</td><td>{esc(e['date'])}</td><td><b>{esc(e['title'])}</b><br>{esc(e['correspondents'])}</td>"
                   f"<td>{esc(e['shelfmark'])}<br>{ark_links(e)}</td><td>{esc(e['status'])}</td><td>{esc(e['why'])}</td>"
                   f"<td>{e['importance']}</td><td>{e['solvability']}</td><td>{e['difficulty']}</td><td>{e['cls']}</td></tr>")
    return '\n'.join(out)


def facet(name, label, values):
    opts = ''.join(f'<button type="button" class="chip" data-facet="{name}" data-val="{esc(v)}" aria-pressed="false">{esc(v)}</button>' for v in values)
    return f'<div class="facet"><span class="flabel">{label}</span>{opts}</div>'


def build_html():
    E = DATA['entries']
    counted = sorted([e for e in E if e['counted']], key=lambda e: (-priority(e), e['id']))
    also = sorted([e for e in E if not e['counted']], key=lambda e: (-priority(e), e['id']))
    periods = sorted({e['period'] for e in E})
    regions = sorted({e['region'] for e in E})
    sources = sorted({e['source'] for e in E})
    data_js = json.dumps({'weights': W, 'entries': E}, ensure_ascii=False).replace('</', '<\\/')
    n_all, n_img = len(E), sum(1 for e in E if e['seen'] == 'image')
    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Catalogue of unsolved historical ciphers — {len(counted)} new targets, scored</title>
<meta name="description" content="Undeciphered historical cipher letters, 1497–1650, not on the standard unsolved lists, harvested from the BnF catalogue on Gallica and the fine print of the cryptiana articles. Each scored for historical importance, solvability and difficulty; filter, sort and reweight the priority score.">
<link rel="stylesheet" href="style.css">
<style>
.ctl{{background:var(--panel);border:1px solid var(--rule);border-radius:var(--radius);padding:1rem 1.1rem;margin:1.2rem 0}}
.ctl .row{{display:flex;flex-wrap:wrap;gap:.8rem 1.4rem;align-items:center}}
.ctl label{{font-family:var(--mono);font-size:.76rem;letter-spacing:.04em;color:var(--muted)}}
.ctl input[type=range]{{width:130px;vertical-align:middle;accent-color:var(--gold)}}
.ctl input[type=search],.ctl select{{background:var(--bg);color:var(--ink);border:1px solid var(--rule);border-radius:6px;padding:.35rem .6rem;font:inherit;font-size:.9rem}}
.facet{{display:flex;flex-wrap:wrap;gap:.35rem;align-items:center;margin:.45rem 0}}
.flabel{{font-family:var(--mono);font-size:.72rem;letter-spacing:.06em;color:var(--muted);min-width:5.5rem}}
.chip{{padding:.25rem .7rem;border-radius:999px;border:1px solid var(--rule);background:var(--bg);color:var(--ink2);font-family:var(--mono);font-size:.74rem;cursor:pointer}}
.chip[aria-pressed=true]{{background:var(--gold);color:var(--gold-ink);border-color:var(--gold)}}
.chip:hover{{border-color:var(--gold)}}
.count{{font-family:var(--mono);font-size:.78rem;color:var(--muted);margin:.6rem 0}}
.cards2{{display:grid;gap:.9rem;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));margin:1rem 0 2rem}}
.card2{{background:var(--panel);border:1px solid var(--rule);border-radius:var(--radius);padding:.9rem 1rem;display:flex;flex-direction:column;gap:.45rem}}
.card2 .top{{display:flex;justify-content:space-between;align-items:baseline;gap:.6rem}}
.card2 .prio{{font-family:var(--display);font-size:1.7rem;line-height:1;color:var(--gold)}}
.card2 .prio small{{font-family:var(--mono);font-size:.6rem;color:var(--muted);display:block;letter-spacing:.08em}}
.card2 h3{{margin:0;font-size:1.02rem;line-height:1.3}}
.card2 .date{{font-family:var(--mono);font-size:.74rem;color:var(--muted)}}
.card2 .why{{font-size:.9rem;color:var(--ink2);margin:0}}
.bars{{display:grid;grid-template-columns:auto 1fr auto;gap:.15rem .5rem;align-items:center;font-family:var(--mono);font-size:.7rem;color:var(--muted)}}
.bar{{height:6px;background:var(--rule);border-radius:3px;overflow:hidden}}
.bar i{{display:block;height:100%;background:var(--gold)}}
.bar.diff i{{background:var(--red)}}
.tags{{display:flex;flex-wrap:wrap;gap:.3rem}}
.tag{{font-family:var(--mono);font-size:.66rem;letter-spacing:.05em;padding:.12rem .5rem;border-radius:999px;border:1px solid var(--rule);color:var(--muted)}}
.tag.A{{border-color:var(--green);color:var(--green)}}.tag.B{{border-color:var(--amber);color:var(--amber)}}.tag.C{{border-color:var(--red);color:var(--red)}}
.tag.seen{{border-color:var(--blue);color:var(--blue)}}
.card2 details{{font-size:.86rem}}
.card2 summary{{cursor:pointer;color:var(--gold);font-family:var(--mono);font-size:.74rem;letter-spacing:.04em}}
.card2 details p{{margin:.4rem 0}}
.tablewrap{{overflow-x:auto;margin:1.2rem 0}}
table.cat{{border-collapse:collapse;font-size:.82rem;min-width:1000px}}
table.cat th,table.cat td{{border-bottom:1px solid var(--rule);padding:.4rem .5rem;vertical-align:top;text-align:left}}
table.cat th{{position:sticky;top:0;background:var(--bg)}}
.nojs .jsonly{{display:none}}
</style>
</head>
<body id="top" class="nojs">
<!-- site:nav -->

<section class="hero">
  <p class="kicker">Gallica · BnF catalogue harvest · cryptiana fine print · 1497–1650 · {len(counted)} new targets + {len(also)} noted · unvalidated</p>
  <h1>Catalogue of unsolved historical ciphers</h1>
  <p class="sub">What is still in cipher in the digitised French diplomatic volumes, and nobody has put on a list. Each entry is scored 1–5 for <b>historical importance</b> (what the text could add), <b>solvability</b> (odds of a full reading with the material online) and <b>difficulty</b> (the technical work), and the <b>priority</b> below is a weighted blend you can reweight. Class <b>A</b> means siblings with decipherment in the same volume, <b>B</b> a partial key or known family in print, <b>C</b> no key and no sibling.</p>
  <p class="sub">Scores are judgements from catalogue descriptions and the literature, not from the leaves: {n_img} of {n_all} entries have been viewed on the image, and each carries the check that would confirm it is open. Data: <a href="https://github.com/dbourdeau/cyphersolver/blob/main/catalogue.json" rel="noopener">catalogue.json</a> · text: <a href="https://github.com/dbourdeau/cyphersolver/blob/main/CATALOGUE.md" rel="noopener">CATALOGUE.md</a>.</p>
  <p class="meta">Daniel Bourdeau · September 2026</p>
</section>

<main>
<h2>Explore</h2>
<div class="ctl jsonly">
  <div class="row">
    <label>Search <input type="search" id="q" placeholder="name, place, shelfmark…" aria-label="Search the catalogue"></label>
    <label>Sort <select id="sort"><option value="prio">priority</option><option value="importance">importance</option><option value="solvability">solvability</option><option value="difficulty">difficulty (easiest first)</option><option value="year">date</option><option value="id">catalogue number</option></select></label>
    <label>Weights: importance <input type="range" id="w_imp" min="0" max="100" value="{int(W['importance']*100)}"> <span id="v_imp"></span></label>
    <label>solvability <input type="range" id="w_sol" min="0" max="100" value="{int(W['solvability']*100)}"> <span id="v_sol"></span></label>
    <label>ease (inverse difficulty) <input type="range" id="w_eas" min="0" max="100" value="{int(W['ease']*100)}"> <span id="v_eas"></span></label>
    <button type="button" class="chip" id="reset">reset</button>
  </div>
  {facet('cls', 'Class', ['A', 'B', 'C'])}
  {facet('period', 'Period', periods)}
  {facet('region', 'Region', regions)}
  {facet('source', 'Source', sources)}
  {facet('seen', 'Seen', ['image', 'catalogue'])}
  {facet('counted', 'Set', ['counted', 'also noted'])}
  <div class="count" id="count"></div>
</div>

<div class="cards2 jsonly" id="cards"></div>

<h2>Table</h2>
<p>All entries at the default weights (importance {W['importance']}, solvability {W['solvability']}, ease {W['ease']}), highest priority first. Imp. = importance, Solv. = solvability, Diff. = difficulty, 1–5.</p>
<div class="tablewrap"><table class="cat">
<thead><tr><th>Prio.</th><th>#</th><th>Date</th><th>Item</th><th>Shelfmark / ark</th><th>Status &amp; prior art</th><th>Why it matters</th><th>Imp.</th><th>Solv.</th><th>Diff.</th><th>Cls</th></tr></thead>
<tbody>
{static_rows(counted + also)}
</tbody></table></div>

<h2>How the scores were set</h2>
<p><b>Importance</b> asks what a full reading would add: 5 for a first-hand report of a major event by a principal witness (du Bellay in London 1529, Lanssac at the Polish election), 2 for routine business. <b>Solvability</b> asks whether the material online is enough: 5 when deciphered siblings of the same hand and year sit in the same volume, 1 for one short letter in an unknown language. <b>Difficulty</b> is the technical work at the keyboard: 1 for aligning a known sibling, 5 for a statistics-only attack on a large homophonic nomenclator. The default priority weights importance 0.4, solvability 0.35 and ease 0.25, rescaled to 0–10; move the sliders to see the order change. Every score is a judgement made before viewing the leaf, so treat the order as a work plan, not a finding.</p>
<p><b>Checked:</b> catalogue descriptions and item numbering; presence or absence of a decipherment item in each volume; shelfmarks from the IIIF manifests; fr. 16127 and fr. 3484 f. 34 on the image. <b>Not checked:</b> the other leaves; Tomokiyo's François I article; the Scheurer, Savasse and Mousset editions; DECODE. <b>User must verify</b> each entry on the image and in the literature before attacking it.</p>
</main>
<!-- site:footer -->
<script id="catdata" type="application/json">{data_js}</script>
<script>
(function(){{
document.body.classList.remove('nojs');
var D=JSON.parse(document.getElementById('catdata').textContent),E=D.entries,G='{GALLICA}';
var state={{q:'',sort:'prio',w:{{imp:D.weights.importance,sol:D.weights.solvability,eas:D.weights.ease}},f:{{}}}};
function prio(e){{var w=state.w,t=w.imp+w.sol+w.eas||1;var v=(w.imp*e.importance+w.sol*e.solvability+w.eas*(6-e.difficulty))/t;return Math.round((v-1)/4*100)/10;}}
function esc(s){{return String(s).replace(/[&<>"]/g,function(c){{return{{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c];}});}}
function bar(l,v,cls){{return '<span>'+l+'</span><span class="bar '+(cls||'')+'"><i style="width:'+(v*20)+'%"></i></span><span>'+v+'/5</span>';}}
function card(e){{var p=prio(e);var arks=['ark','ark2'].filter(function(k){{return e[k];}}).map(function(k){{return '<a href="'+G+e[k]+'" rel="noopener">'+e[k]+'</a>';}}).join(' · ');
 return '<article class="card2"><div class="top"><h3>'+esc(e.title)+'</h3><div class="prio">'+p.toFixed(1)+'<small>priority</small></div></div>'
 +'<div class="date">#'+e.id+' · '+esc(e.date)+' · '+esc(e.place)+' · '+esc(e.language)+'</div>'
 +'<p class="why">'+esc(e.why)+'</p>'
 +'<div class="bars">'+bar('importance',e.importance)+bar('solvability',e.solvability)+bar('difficulty',e.difficulty,'diff')+'</div>'
 +'<div class="tags"><span class="tag '+e.cls+'">class '+e.cls+'</span><span class="tag'+(e.seen==='image'?' seen':'')+'">'+(e.seen==='image'?'seen on image':'catalogue only')+'</span><span class="tag">'+esc(e.source)+'</span>'+(e.counted?'':'<span class="tag">also noted</span>')+'</div>'
 +'<details><summary>shelfmark, status, verification</summary><p><b>'+esc(e.shelfmark)+'</b>'+(arks?' · '+arks:'')+(e.folio_note?' · '+esc(e.folio_note):'')+'</p><p>'+esc(e.correspondents)+'</p><p>'+esc(e.status)+'</p><p><i>Scores:</i> '+esc(e.score_note)+'</p><p><i>Verify first:</i> '+esc(e.verify)+'</p>'+(e.writeup?'<p><a href="'+e.writeup+'">Write-up &rarr;</a></p>':'')+'</details></article>';}}
function match(e){{var f=state.f;for(var k in f){{if(!f[k].length)continue;var v=k==='counted'?(e.counted?'counted':'also noted'):e[k];if(f[k].indexOf(v)<0)return false;}}
 if(state.q){{var h=(e.title+' '+e.correspondents+' '+e.place+' '+e.shelfmark+' '+e.why+' '+e.status+' '+e.region+' '+e.language+' '+e.date).toLowerCase();if(h.indexOf(state.q)<0)return false;}}return true;}}
function render(){{var L=E.filter(match);var s=state.sort;L.sort(function(a,b){{if(s==='prio')return prio(b)-prio(a)||a.id-b.id;if(s==='difficulty')return a.difficulty-b.difficulty||prio(b)-prio(a);if(s==='year'||s==='id')return a[s]-b[s];return b[s]-a[s]||prio(b)-prio(a);}});
 document.getElementById('cards').innerHTML=L.map(card).join('');document.getElementById('count').textContent=L.length+' of '+E.length+' entries';
 document.getElementById('v_imp').textContent=state.w.imp.toFixed(2);document.getElementById('v_sol').textContent=state.w.sol.toFixed(2);document.getElementById('v_eas').textContent=state.w.eas.toFixed(2);
 var tb=document.querySelector('table.cat tbody');if(tb){{var rows=Array.prototype.slice.call(tb.rows);rows.forEach(function(r){{var id=+r.cells[1].textContent;var e=E.filter(function(x){{return x.id===id;}})[0];if(e)r.cells[0].textContent=prio(e).toFixed(1);}});rows.sort(function(a,b){{return parseFloat(b.cells[0].textContent)-parseFloat(a.cells[0].textContent);}});rows.forEach(function(r){{tb.appendChild(r);}});}}}}
document.querySelectorAll('.chip[data-facet]').forEach(function(b){{b.addEventListener('click',function(){{var k=b.dataset.facet,v=b.dataset.val;state.f[k]=state.f[k]||[];var i=state.f[k].indexOf(v);if(i<0)state.f[k].push(v);else state.f[k].splice(i,1);b.setAttribute('aria-pressed',i<0?'true':'false');render();}});}});
document.getElementById('q').addEventListener('input',function(ev){{state.q=ev.target.value.trim().toLowerCase();render();}});
document.getElementById('sort').addEventListener('change',function(ev){{state.sort=ev.target.value;render();}});
[['w_imp','imp'],['w_sol','sol'],['w_eas','eas']].forEach(function(p){{document.getElementById(p[0]).addEventListener('input',function(ev){{state.w[p[1]]=ev.target.value/100;render();}});}});
document.getElementById('reset').addEventListener('click',function(){{state.q='';state.sort='prio';state.w={{imp:D.weights.importance,sol:D.weights.solvability,eas:D.weights.ease}};state.f={{}};document.getElementById('q').value='';document.getElementById('sort').value='prio';document.getElementById('w_imp').value=state.w.imp*100;document.getElementById('w_sol').value=state.w.sol*100;document.getElementById('w_eas').value=state.w.eas*100;document.querySelectorAll('.chip[data-facet]').forEach(function(b){{b.setAttribute('aria-pressed','false');}});render();}});
render();
}})();
</script>
</body>
</html>
'''
    (HERE / 'catalogue.html').write_text(page, encoding='utf-8')
    print('wrote catalogue.html', len(page), 'entries', len(E))


if __name__ == '__main__':
    update_md()
    build_html()
