"""Download all page images of a PARES record (ACA register) with the project's minimal client."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'adrian1521'))
import pares
nid, prefix = sys.argv[1], sys.argv[2]
files = pares.images(nid, os.path.join('img', prefix), prefix)
print(len(files), 'files')
