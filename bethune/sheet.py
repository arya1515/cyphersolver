"""sheet.py <out.jpg> <crop1.jpg> <crop2.jpg> ...  — stack crops vertically with a separator bar.
Keeps each crop's own width (padded to the max) so horizontal resolution is unchanged."""
import sys
from PIL import Image
out, paths = sys.argv[1], sys.argv[2:]
ims = [Image.open(p).convert('L') for p in paths]
W = max(i.width for i in ims); SEP = 6
H = sum(i.height for i in ims) + SEP*(len(ims)-1)
sheet = Image.new('L', (W, H), 255)
y = 0
for n, i in enumerate(ims):
    sheet.paste(i, (0, y)); y += i.height
    if n < len(ims)-1:
        sheet.paste(Image.new('L', (W, SEP), 0), (0, y)); y += SEP
sheet.save(out, quality=94)
print(out, sheet.size, len(paths), 'strips')
