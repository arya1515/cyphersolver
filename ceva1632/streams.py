"""Pull the ciphertext digit stream out of the DECODE transcriptions.

Lines beginning '#' are headers, '<...>' lines are the clerk's cleartext;
everything else is cipher.  Transcribers marked doubt with '?' and stressed
digits with '_'; both are dropped, and the digits are run together because
the clerk's own spacing is not the code boundary.
"""
import re, sys, os

def stream(path):
    out, clear = [], []
    for line in open(path, encoding='utf-8', errors='replace'):
        s = line.strip()
        if not s or s.startswith('#'):
            continue
        if s.startswith('<'):
            clear.append(s)
            # a cleartext line may still carry cipher after the '>'
            s = re.sub(r'^<[^>]*>', '', s).strip()
            if not s:
                continue
        d = re.sub(r'\D', '', s)
        if d:
            out.append(d)
    return out, clear

if __name__ == '__main__':
    p = sys.argv[1]
    lines, clear = stream(p)
    total = sum(len(l) for l in lines)
    sys.stderr.write('%s: %d cipher lines, %d digits, %d cleartext lines\n'
                     % (os.path.basename(p), len(lines), total, len(clear)))
    print('\n'.join(lines))
