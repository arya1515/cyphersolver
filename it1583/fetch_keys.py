import json,sys,os,time
sys.path.insert(0,'catalogue_harvest/decode'); import dump_list as D
L=json.load(open('../../catalogue_harvest/decode/list.json',encoding='utf8'))
ids=[r['id'] for r in L if 'Sforzesco' in r['c_holder']]+[str(i) for i in range(7899,7916)]
tok=D.jwt(); out=open('it1583/sforza_views.jsonl','a',encoding='utf8')
for i in ids:
    try: v=D.api('view/Records/%s'%i,tok)['records']
    except Exception as e: time.sleep(3); tok=D.jwt(); v=D.api('view/Records/%s'%i,tok)['records']
    out.write(json.dumps(v,ensure_ascii=False)+'\n'); out.flush(); time.sleep(.2)
print('done')
