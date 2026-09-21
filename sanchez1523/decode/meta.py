import re,html,glob,os,sys
def val(s,label):
    m=re.search(r'\n'+label+r'\n(.*?)\n',s)
    return m.group(1).strip() if m else ''
rows=[]
for p in sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)),'rec*.htm')),key=lambda x:int(re.findall(r'\d+',os.path.basename(x))[0])):
    t=open(p,encoding='utf-8',errors='replace').read()
    imgs=sorted(set(re.findall(r'filesrv/\?file=TH_([A-Za-z0-9_.]+)',t)))
    s=re.sub(r'<(script|style).*?</\1>','',t,flags=re.S|re.I)
    s=re.sub(r'<[^>]+>','\n',s); s=html.unescape(s)
    s='\n'+'\n'.join(l.strip() for l in s.split('\n') if l.strip())
    rid=re.findall(r'\d+',os.path.basename(p))[0]
    holder=val(s,'Holder')
    rows.append((rid,val(s,'Status'),val(s,'Start Year'),val(s,'Start Month'),val(s,'Start Day'),
                 val(s,'No. of Pages'),len(imgs),val(s,'Author'),holder,val(s,'Inline Cleartext')))
print('rec\tstatus\ty\tm\td\tpp\timgs\tauthor\tholder\tinlineclear')
for r in rows: print('\t'.join(map(str,r)))
