import re
def load(path='key_raw.txt', check=True):
    K={}
    for line in open(path, encoding='utf8'):
        line=line.strip()
        if not line or line.startswith('#'): continue
        n,rest=line.split(':',1)
        n=int(n)
        for e in rest.strip().split('|'):
            while n%10 in (5,9): n+=1
            e=e.strip().lstrip('*')
            if e:
                if n in K and K[n]!=e: print('CONFLICT',n,K[n],e)
                K[n]=e
            n+=1
    return K
if __name__=='__main__':
    K=load(); print(len(K))
