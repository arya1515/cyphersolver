"""Cut f.74r text into per-line strips following each line's slope (centres from ink projection in 5 bands)."""
from PIL import Image, ImageDraw
import numpy as np
B = {800:[377,524,669,833,980,1134,1308,1501,1663,1842,2037,2166,2336,2471,2678,2913,3068,3375,3646,4018,4230,4353,4547],
1800:[392,563,701,881,977,1172,1380,1556,1729,1880,2076,2211,2379,2589,2796,2973,3206,3422,3718,4016,4249,4427,4617],
2800:[420,575,739,873,1048,1200,1431,1575,1760,1918,2112,2266,2414,2611,2821,3054,3266,3467,3742,4048,4258,4441,4627],
3800:[424,584,715,934,1075,1249,1456,1652,1839,1983,2184,2359,2554,2749,2937,3150,3345,3551,3799,4077,4263,4456,4644],
4800:[430,571,758,923,1132,1304,1496,1672,1855,2027,2224,2424,2600,2751,2996,3179,3379,3609,3829,4079,4312,4498,4701]}
xs = sorted(B)
im = Image.open('img/f74r_text.jpg')
H = 250
SEG = [(200,1650),(1550,3000),(2900,4350),(4250,5500)]
for L in range(23):
    ys = [B[x][L] for x in xs]
    strip = Image.new('RGB', (5500, H))
    for x in range(0, 5500, 50):
        yc = int(np.interp(x + 25, xs, ys))
        strip.paste(im.crop((x, yc - H//2, x + 50, yc + H//2)), (x, 0))
    strip.save(f'view/L{L+1:02d}.jpg', quality=92)
    for j,(a,b) in enumerate(SEG):
        c = strip.crop((a,0,b,H)); d = ImageDraw.Draw(c); d.text((3,3), f'L{L+1} {a}', fill='red')
        c.save(f'view/L{L+1:02d}{"abcd"[j]}.jpg', quality=92)
