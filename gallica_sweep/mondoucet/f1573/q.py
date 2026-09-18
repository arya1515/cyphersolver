import sys
from PIL import Image
for c in sys.argv[1:]:
    im=Image.open(f'full16127/c{c}.jpg').convert('L')
    im.resize((1240, im.height*1240//im.width)).save(f'mondoucet/f1573/c{c}_q.png')
