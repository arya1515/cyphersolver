"""Print large windows of Avenel vol. III around given anchors."""
import re, sys, pathlib
t = (pathlib.Path(__file__).parent / 'avenel3.txt').read_text(encoding='utf-8', errors='ignore')
anchor = sys.argv[1]; before = int(sys.argv[2]) if len(sys.argv) > 2 else 3000; after = int(sys.argv[3]) if len(sys.argv) > 3 else 5000
for m in re.finditer(re.escape(anchor), t):
    print(f'\n########## hit at {m.start()}\n')
    print(t[max(0, m.start()-before): m.start()+after])
    print('\n##########')
