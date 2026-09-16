"""Render the manuscript pages once they are in hand (see GET_IMAGES.md).

python render.py ms994_full.pdf          -> img/pNNN.png at 300 dpi, one per PDF page, and a contact sheet
python render.py --decode                -> splits decode/IMG_R2252_*.png openings into img/R2252_PM_left/right.png
python render.py --crop img/p045.png 4   -> cuts the page into 4 horizontal strips at 2x for line-level reading
"""
import sys, os, glob
HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, 'img'); os.makedirs(IMG, exist_ok=True)

def from_pdf(fn, dpi=300):
    import fitz
    d = fitz.open(fn)
    print('pages', d.page_count)
    for i, p in enumerate(d):
        out = os.path.join(IMG, 'p%03d.png' % (i + 1))
        p.get_pixmap(dpi=dpi).save(out)
        print(out)
    sheet(sorted(glob.glob(os.path.join(IMG, 'p*.png'))))

def sheet(files, w=180):
    from PIL import Image, ImageDraw
    cols = 8; rows = (len(files) + cols - 1) // cols
    m = Image.new('RGB', (cols * w, rows * (w + 14)), 'white'); dr = ImageDraw.Draw(m)
    for k, f in enumerate(files):
        im = Image.open(f); im.thumbnail((w - 4, w - 4))
        x, y = (k % cols) * w, (k // cols) * (w + 14)
        m.paste(im, (x + 2, y + 2)); dr.text((x + 4, y + w), os.path.basename(f), fill='black')
    m.save(os.path.join(IMG, 'contact_sheet.png')); print('contact sheet written')

def split_decode():
    from PIL import Image
    for f in sorted(glob.glob(os.path.join(HERE, 'decode', 'IMG_R2252_*.png'))):
        im = Image.open(f); w, h = im.size
        base = os.path.splitext(os.path.basename(f))[0]
        im.crop((0, 0, w // 2, h)).save(os.path.join(IMG, base + '_left.png'))
        im.crop((w // 2, 0, w, h)).save(os.path.join(IMG, base + '_right.png'))
        print(base, im.size)

def crop(fn, n):
    from PIL import Image
    im = Image.open(fn); w, h = im.size
    for k in range(n):
        s = im.crop((0, k * h // n, w, (k + 1) * h // n)).resize((2 * w, 2 * (h // n)), Image.LANCZOS)
        out = fn.replace('.png', '_strip%d.png' % (k + 1)); s.save(out); print(out)

if __name__ == '__main__':
    a = sys.argv[1:]
    if not a:
        print(__doc__)
    elif a[0] == '--decode':
        split_decode()
    elif a[0] == '--crop':
        crop(a[1], int(a[2]) if len(a) > 2 else 4)
    else:
        from_pdf(a[0])
