"""Record the limited key verification and the existing published counterparts."""
import json, pathlib
root = pathlib.Path(__file__).resolve().parent
profile = json.loads((root/'profile.json').read_text(encoding='utf-8'))
profile['conditions']['prior_solution'] = {
    'exists':'in print',
    'where':'Forbes I (1740), II (1741); CSP Foreign II, V, VI; Tomokiyo describes three reconstructed ciphers and the surviving archive keys.',
    'found':'before attempt', 'used':True}
profile['conditions']['inputs'] = ['images','key from archive','published reading']
profile['conditions']['sessions'] = 'unknown'
profile['conditions']['human_role'] = 'User supplied the twenty-record target and authorized use of the existing DECODE cookie.'
profile['system']['symbol_kind'] = 'digits and symbols'
profile['system']['summary'] = 'The sampled Throckmorton passages use the archived third cipher: graphic and numeric homophones, marked-letter word signs, suffixes and nulls.'
profile['system']['diacritics']['note'] = 'Single dots and paired dots distinguish numeric homophones; position of marks distinguishes word codes.'
profile['documents'] = []
rows = json.loads((root/'concordance.json').read_text(encoding='utf-8'))
for r in rows:
    doc = {'id':r['record'], 'shelfmark':'BL Add MS 4136 ff.'+r['folio'], 'year':int(r['date'].split(' (')[0][-4:]),
        'country':'England','language':'English','cleartext_in_document':'unknown',
        'plaintext':{'location':['printed edition'], 'source':r['edition']+'; '+r['url'], 'partial':True},
        'length':{'tokens':'unknown','unit':'mixed','measured':False},
        'transcription':{'by':'unknown','image_quality':'good','notes':r['evidence']+' No complete token transcription.'}}
    if r['record']=='R9220':
        doc['transcription'].update(by='llm from images', notes='Numbered extract (6) transcribed: 27 tokens, 24 distinct labels, including 2 nulls, measured with _check_profile.py; whole-record length unknown. control.json and control_tokens.txt.')
    if r['record']=='R9230':
        doc['transcription'].update(by='llm from images', notes='Opening of extract (1) sampled: 15 alphabet tokens, 14 distinct labels, measured with _check_profile.py; whole-record length unknown. control_9230.json and control_9230_tokens.txt.')
    profile['documents'].append(doc)
profile['solution'] = profile['solution'][:4] + [
    {'date':'2026-09-20','kind':'literature search','what':'Existing dossier maps all twenty target records to CSP Foreign II, V and VI, with Forbes counterparts for many. Most matches are date/addressee matches, not full cipher alignments. Tomokiyo already cites Forbes and the archived keys.','result':'worked'},
    {'date':'2026-09-20','kind':'verification','what':'Rechecked downloaded image inventory: 54 target references, 39 unique JPEGs; four key records add 17 JPEGs. R9220 and R9221 are byte-identical copies of f.110. SHA-256 inventory preserved.','result':'worked'},
    {'date':'2026-09-20','kind':'control','what':'Visually rechecked 27-token R9220 extract (6) against R9262 P1, P3, P4 and P9: all be it i be revoked or the warr breake. Forbes I p.355 agrees. This is a known-plaintext verification, not a blind break.','result':'worked'},
    {'date':'2026-09-20','kind':'control','what':'Transcribed and replayed 15 alphabet tokens at R9230 extract (1): orleans or burges. R9262 P1 agrees; Forbes II p.12 and CSP V no.425 paragraph 11 identify the passage.','result':'worked'},
    {'date':'2026-09-20','kind':'verification','what':'Identified R9257 as a mixed Percy ciphertext/key leaf and R9261 as Smith cipher, so proximity alone does not establish key applicability. R9255 combines multiple writers.','result':'worked'},
    {'date':'2026-09-20','kind':'verification','what':'Downloaded and viewed Forbes facsimiles: I p.355 confirms the complete R9220 sample. II p.12 confirms Orleans or Burges; corrected inherited erroneous p.31 citation and pp.28–35 range. Pages 31, 32 and 34 were inspected while locating the correct page; they are later August material.','result':'worked'}]
profile['outcome'] = {'class':'already solved','fraction_read':'unknown','verification':['key confirms','independent clear copy'],
    'notes':'Prior published plaintext and archived keys identified; two short samples (42 tokens total) verified. Twenty-record source concordance is not an end-to-end decipherment. Composite-record non-Throckmorton material and complete transcription remain unverified.'}
(root/'profile.json').write_text(json.dumps(profile,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
