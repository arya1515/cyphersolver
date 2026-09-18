from PIL import Image
im=Image.open('soglia-cryptogram.png').convert('L')
bands=[(1133,1150),(1176,1193),(1218,1235),(1259,1276),(1301,1318),(1343,1360),(1384,1402),(1426,1444),(1468,1486),(1509,1527),(1551,1569),(1593,1611),(1636,1654),(1679,1695),(1720,1737),(1762,1779),(1890,1906),(1911,1926)]
for i,(a,b) in enumerate(bands):
    for h,(x0,x1) in enumerate([(110,600),(560,1060)]):
        c=im.crop((x0,a-14,x1,b+12)); c=c.resize((c.width*3,c.height*3),Image.LANCZOS)
        c.save(f'line{i+1:02d}{"ab"[h]}.png')
