import sys
from PIL import Image
im=Image.open('img/c234.jpg')
rows={2:2499,3:2713,4:2807,5:2900,6:2992,7:3078,8:3163,9:3249,10:3314,11:3485,12:3570,13:3663,14:3756,15:3907,16:4380,17:4464,18:4564,19:4649,20:4742,21:4842,22:4927,23:5014,24:5107,25:5192,26:5292,27:5384,28:5592,29:5685,30:5799}
segs=[(1480,2500),(2400,3420),(3320,4400)]
for r in map(int,sys.argv[1:]):
    y=rows[r]
    for i,(a,b) in enumerate(segs):
        c=im.crop((a,y-190,b,y+90)); c=c.resize((1900,int(c.height*1900/c.width)),Image.LANCZOS)
        c.save(f'cal/crops/113_R{r}_{i}.jpg',quality=90)
