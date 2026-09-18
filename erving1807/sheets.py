"""Contact sheets of a reel: python sheets.py imgdir outdir [per_sheet]"""
import sys, os, glob
from PIL import Image, ImageDraw
src, out = sys.argv[1], sys.argv[2]
per = int(sys.argv[3]) if len(sys.argv) > 3 else 30
os.makedirs(out, exist_ok=True)
fs = sorted(glob.glob(os.path.join(src, '*.jpg')))
W, H, cols = 300, 400, 6
for i in range(0, len(fs), per):
    chunk = fs[i:i+per]
    rows = (len(chunk) + cols - 1) // cols
    sheet = Image.new('L', (cols*W, rows*(H+20)), 255)
    d = ImageDraw.Draw(sheet)
    for j, f in enumerate(chunk):
        im = Image.open(f).convert('L'); im.thumbnail((W, H))
        x, y = (j % cols)*W, (j//cols)*(H+20)
        sheet.paste(im, (x, y+20)); d.text((x+5, y+3), os.path.basename(f)[-8:-4], fill=0)
    sheet.save(os.path.join(out, f'sheet_{i:04d}.png'))
    print(out, i)
