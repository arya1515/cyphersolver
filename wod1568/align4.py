from align3 import MAIN,TAIL,solve
import sys
for P in ["andsayshemustneidishaifitbeonmeinisoruthir","andsayishemustneidishaifitbeonmeinisoruthir"]:
  for C in (MAIN,MAIN+TAIL):
    r=solve(C,P,int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]))
    print(P,len(C),len(r)); [print(x) for x in r[:5]]
