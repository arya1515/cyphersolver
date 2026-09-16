# Evaluate a control run: letter accuracy of the rendered plaintext against the true plaintext.
import sys, re
run, plainf = sys.argv[1], sys.argv[2]
plain = open(plainf).read().strip()
lines = open(run, encoding='utf-8').read().splitlines()
i = [k for k, l in enumerate(lines) if l.startswith('BEST')][-1]
out = lines[i + 1].strip()
n = min(len(out), len(plain))
acc = sum(1 for a, b in zip(out, plain) if a == b) / n
print(run, lines[i], 'accuracy %.1f%%' % (100 * acc))
print(' got :', out[:120]); print(' true:', plain[:120])
