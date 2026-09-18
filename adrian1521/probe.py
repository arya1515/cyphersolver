import pares,re,sys
from concurrent.futures import ThreadPoolExecutor
def one(nid):
    try: h=pares.get(f'{pares.BASE}/catalogo/description/{nid}').decode('utf-8','replace')
    except Exception: return None
    t=re.sub(r'\s+',' ',re.sub(r'<[^>]*>',' ',h))
    s=re.search(r'Signatura: (\S+)',t)
    if not s: return None
    ti=re.search(r'Nombre Atribuido: (.*?) Signatura',t); f=re.search(r'Fecha Creación: (.*?) Nivel',t)
    a=re.search(r'Alcance y Contenido: (.*?) (?:Índices|Condiciones)',t)
    return nid,s.group(1),f and f.group(1),ti and ti.group(1)[:150],a and a.group(1)[:200]
lo,hi=int(sys.argv[1]),int(sys.argv[2]); pref=sys.argv[3]
with ThreadPoolExecutor(12) as ex:
    for r in ex.map(one,range(lo,hi)):
        if r and r[1].startswith(pref): print(*r,sep=' | ',flush=True)
