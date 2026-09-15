from solver5 import LM
lm = LM()
for s in ['che', 'della', 'nuntio', 'iiiii', 'iii', 'i', 'sia', 'santita', 'xqzk', 'aaaaa', 'eeee', 'il', 'di', 'et', 'non', 'per', 'sua', 'maesta', 'cesarea']:
    print(f'{s:10} {lm.score(s):7.2f}  per char {lm.score(s)/(len(s)+1):6.2f}')
