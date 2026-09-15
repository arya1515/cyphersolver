from PIL import Image
import glob
for f in sorted(glob.glob(r'c:\Users\dbour\cypher\colbert\decode\TH_*.png')):
    im = Image.open(f); print(f.split('\\')[-1], im.size)
