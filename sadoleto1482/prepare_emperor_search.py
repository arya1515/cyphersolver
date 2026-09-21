from pathlib import Path
root = Path(__file__).resolve().parent
s = (root/'search_u02_r1101.py').read_text()
s = s.replace('U02 search', 'emperor-expression search')
s = s.replace('IMG_R1102_I5657_P2.png', 'IMG_R1101_I5654_P1.png')
s = s.replace('[631:652,157:217]', '[275:290,235:275]')
s = s.replace('round(60*scale),round(21*scale)', 'round(40*scale),round(15*scale)')
s = s.replace('u02_search_', 'emperor_search_')
s = s.replace('u02_r1101_candidates.json', 'emperor_r1101_candidates.json')
s = s.replace("'I5655':('IMG_R1101_I5655_P2.png',[(1090,215,3230,2300)])", "'first':('v/v1284_1_ASMO Ambasciatori Busta 1 (103).JPG',[(1200,180,3330,2850)])")
(root/'search_emperor_r1101.py').write_text(s)
