import sys,re
K={'11':'t','12':'w','13':'y','14':'x','15':'l','21':'z','22':'o','23':'k','24':'f','25':'m','31':'d','32':'n','33':'v','34':'h','35':'b','41':'g','42':'u','43':'a','44':'s','45':'p','51':'c','52':'r','53':'y','54':'q','55':'i','65':'e','<theta>':'DE','[sign:circle with dot]':'DE'}
for line in open(sys.argv[1],encoding='utf8'):
  out=[]
  for t in re.findall(r'\[[^\]]*\]|<[^>]*>|\S+',line):
    u=t.rstrip('?')
    if re.fullmatch(r'[1-6]{2}',u): out.append(K.get(u,'('+u+')'))
    elif t in K: out.append(K[t])
    else: out.append(' '+t+' ')
  print(''.join(out))
