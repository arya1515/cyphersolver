"""Build a record-to-edition concordance, keeping source matches separate from decryption."""
import pathlib, json, re
root=pathlib.Path(__file__).resolve().parent
rows=[
('9220','110','7–8 March 1560','Cecil','march6',2,837,'Forbes I, pp.352–356; control on p.355','Key control verified; shared leaf also contains R9221.'),
('9221','110','9 March 1560','Queen','march6',2,844,'Forbes I, p.356','Date/addressee match; same image as R9220.'),
('9222','111–112','9 March 1560','Cecil','march6',2,845,'Forbes I, p.358','Date/addressee match.'),
('9223','112–116','15 March 1560','Queen','march11',2,859,'Forbes I, p.360','Date/addressee match.'),
('9224','116–118','15 March 1560','Council','march11',2,860,'Forbes I, p.369','Date/addressee match.'),
('9225','118–120','21 March 1560','Queen','march21',2,'footnote 1','Forbes I, p.376','CSP prints this in a footnote because the State Paper Office original could not then be located.'),
('9226','120–122','21 March 1560','Cecil','march21',2,882,'Forbes I, p.384','Date/addressee match.'),
('9227','122–123','21 March 1560','Council','march21',2,881,'Forbes I, p.382','Date/addressee match.'),
('9228','123–129','24 September 1562','Queen','sep1562b',5,690,'Forbes II, p.61','Date/addressee match.'),
('9229','129–133','15 October 1562','Queen','oct1562a',5,848,'Forbes II, p.111','Date/addressee match.'),
('9230','133','5 August 1562','Queen','aug1562',5,425,'Forbes II, p.12 (sampled passage); CSP no.426 is the separate decipher','Orleans/Burges passage matched to CSP paragraph 11 and the corresponding Forbes letter.'),
('9231','134','9 September 1562','Queen','sep1562a',5,596,'CSP V, no.596','Date/addressee match.'),
('9232','134–135','9 September 1562','Cecil','sep1562a',5,597,'CSP V, nos.597–600 (two same-day letters and copies)','Opening refers to dispatching Francisco on the ninth. No.597 is the principal candidate; keep no.599 for comparison.'),
('9233','135–136','30 October 1562','Cecil','oct1562b',5,935,'Forbes II, p.156','Date/addressee match.'),
('9234','136–138','1 November 1563','Queen','nov1563',6,1356,'CSP VI, no.1356','Manuscript date agrees with 1563; do not change to 1562 just because preceding letters are earlier.'),
('9242','149–150','3 January 1563','Queen','jan1563a',6,12,'Forbes II, p.251','DECODE uses old-style 1562.'),
('9243','150–151','6 January 1563','Queen','jan1563b',6,35,'Forbes II, p.270','DECODE uses old-style 1562.'),
('9244','151–153','13 January 1563','Queen','jan1563c',6,83,'Forbes II, p.275','DECODE uses old-style 1562.'),
('9245','153–155','20 September 1563','Cecil','sep1563',6,1233,'CSP VI, no.1233','Date/addressee match; CSP explicitly says cipher deciphered.'),
('9255','169–171','22 November 1562 (Throckmorton portion)','Queen','nov1562c',5,1099,'Forbes II, p.208; CSP no.1100 is the deciphered copy','Composite record: Smith, Throckmorton, Somer and Randolph. Throckmorton is on ff.169–170. The catalogue author Lomer is apparently Somer. Other writers require separate keys.'),
]
out=[]
for rid,folio,date,recipient,file,volume,entry,edition,note in rows:
    raw=(root/'sources'/f'{file}.html').read_text(encoding='utf-8',errors='replace')
    match=re.search(r'https://www.british-history.ac.uk/cal-state-papers/foreign/vol\d+/[a-z0-9-]+',raw)
    url=match.group() if match else 'unknown'
    out.append(dict(record='R'+rid,folio=folio,date=date,recipient=recipient,csp_volume=volume,csp_entry=entry,source_file='sources/'+file+'.txt',url=url,edition=edition,evidence=note,full_token_verification=False))
(root/'concordance.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
md=['# Throckmorton: record-to-edition concordance','',
    'These are published counterparts identified by date and recipient, with direct passage checks where stated. They are **not twenty completed diplomatic decryptions**. CSP often abridges the full letters. Read the shared-leaf and composite-record cautions before treating a DECODE record as a single message.','',
    'Dates below use January-start years; the manuscript and DECODE often retain March-start years.','',
    '| DECODE | Add MS 4136 folios | Date | Recipient | Published counterpart | Evidence / limits |',
    '|---|---|---|---|---|---|']
for r in out:
    md.append(f"| [{r['record']}](https://de-crypt.org/decrypt-web/RecordsView/{r['record'][1:]}) | {r['folio']} | {r['date']} | {r['recipient']} | [CSP {r['csp_volume']}, {r['csp_entry']}]({r['url']}); {r['edition']} | {r['evidence']} |")
(root/'CONCORDANCE.md').write_text('\n'.join(md)+'\n',encoding='utf-8')

# Preserve complete historical Calendar entries as a reference dossier. This is
# copied edition text, deliberately not presented as a fresh decipherment.
md=['# Published reference texts','',
    'Source: Joseph Stevenson (ed.), Calendar of State Papers, Foreign, Elizabeth, historical public-domain editions, digital text from British History Online. These are calendar summaries and transcriptions, not fresh decryptions. Generated from the cached source pages.','']
for r in out:
    text=(root/r['source_file']).read_text(encoding='utf-8')
    entry=r['csp_entry']
    if isinstance(entry,int):
        m=re.search(r'^'+str(entry)+r'\. Throckmorton[^\n]*\n',text,re.M)
        if not m: raise ValueError(f'Missing heading {r["record"]}: {entry}')
        following=re.search(r'^'+str(entry+1)+r'\. ',text[m.end():],re.M)
        excerpt=text[m.start(): m.end()+following.start() if following else len(text)]
        excerpt=excerpt.split('PreviousTable of contentsNext')[0].strip()
    else:
        m=re.search(r'^Throckmorton to the Queen\.\n',text,re.M)
        if not m: raise ValueError('Missing Queen 21 March footnote')
        excerpt=text[m.start():].split('PreviousTable of contentsNext')[0].strip()
    md.extend([f"## {r['record']}: {r['date']} → {r['recipient']}",'',f"[CSP {r['csp_volume']}, {entry}]({r['url']}) — {r['evidence']}",'',excerpt,''])
(root/'PUBLISHED_REFERENCE_TEXTS.md').write_text('\n'.join(md),encoding='utf-8')
print(f'Wrote {len(out)} concordance entries and published reference sections.')
