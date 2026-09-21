"""Align the code runs of transcription.txt with the clear text printed by Parke (1798) i 310-311."""
import re
PH = """endeavours|used to pervert|cousin|Electoral Prince|Saxony|superstitious worship|church of Rome|[91: no word in print]|dishonour the Protestant interest|Prince|reformation first began|abandon the principles|holy religion|a duty incumbent on us to prevent|in us lies|fatal a blow|you to the said Prince whom|his arrival at Rome|your falling-in|him|merely accidental|him on the road or find him at Rome|deliver our letter to him accompanying it with|his prosperity|insinuate yourself into his good opinion|keeping him steady|Protestant religion|your representations|his mind|him the subject of your commission|dispatched you to him on purpose to let him know that|him which we have so often expressed|he persists|he formerly had|religion in which he was educated he|and honourable reception in our Court|his|his|[261: no word in print]|him this way|him|he|himself|abjuring his religion|he|he has|make his escape|him (first group, foot of f.184v)|(him, continued at the head of f.185r)|rescuing him|hands he is in|him safe|our dominions or those of any other Protestant Prince or State|your|given you leave to see the city of Rome|suspicion of the true intent of your going thither|this service in which we now employ you|enjoin you to correspond with either of our Secretaries of State|your return|come back to Turin|your attendance on the Prince of no further use""".split('|')
t = '\n'.join(l for l in open('transcription.txt', encoding='utf8') if not l.startswith('#'))
runs = [r.strip('.') for r in re.findall(r'(?:\d+\??\.)+', t)]
assert len(runs) == len(PH), (len(runs), len(PH))
with open('alignment.tsv', 'w', encoding='utf8') as f:
    f.write('run\tgroups\tn\tprinted text (Parke 1798)\n')
    for i, (r, p) in enumerate(zip(runs, PH), 1):
        f.write(f'{i}\t{r}\t{len(r.split("."))}\t{p}\n')
print(len(runs), 'runs aligned;', sum(len(r.split('.')) for r in runs), 'groups;', sum(len(p.split()) for p in PH if not p.startswith('[')), 'printed words')
