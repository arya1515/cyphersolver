# Contact sheets for a fetched volume: 4 canvases per sheet (2 x 2) at 700 px wide each, autocontrast, labelled.
import os, sys
from glob import glob
from PIL import Image, ImageOps, ImageDraw
ark = sys.argv[1]; per = int(sys.argv[2]) if len(sys.argv) > 2 else 4; W = int(sys.argv[3]) if len(sys.argv) > 3 else 700
files = sorted(glob(f'{ark}/c*.jpg'))
out = f'sheets_{ark}_{W}'; os.makedirs(out, exist_ok=True)
cols = 2 if per == 4 else per
made = 0
for i in range(0, len(files), per):
    grp = files[i:i + per]
    ids = [os.path.basename(f)[1:4] for f in grp]
    fn = f'{out}/s{ids[0]}_{ids[-1]}.png'
    if os.path.exists(fn):
        continue
    ims = []
    for f in grp:
        try:
            im = Image.open(f).convert('L')
        except Exception:
            im = Image.new('L', (W, W), 128)
        im = im.resize((W, int(im.height * W / im.width)), Image.LANCZOS)
        im = ImageOps.autocontrast(im, cutoff=1); ims.append(im)
    rows = (len(ims) + cols - 1) // cols
    h = max(im.height for im in ims)
    sheet = Image.new('L', (W * cols, (h + 28) * rows), 255); d = ImageDraw.Draw(sheet)
    for k, im in enumerate(ims):
        x = W * (k % cols); y = (h + 28) * (k // cols)
        sheet.paste(im, (x, y + 28)); d.text((x + 8, y + 6), 'canvas ' + ids[k], fill=0)
    sheet.save(fn); made += 1
print('sheets made', made, 'files', len(files))
