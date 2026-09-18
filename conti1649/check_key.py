"""Check Lasry's (2023) final key against his own transcription of f.115 (Figure 8) and the ms reading of one name.
Cipher letters: J=the capital-J sign, d=the round-d (r-like) sign; others as printed."""
KEY = {  # cipher sign -> allowed plaintext letters (Lasry 2023, Fig. 9)
 'J':'A','c':'F','s':'H','t':'I','u':'L','v':'L','g':'N','r':'O','d':'R','o':'R','l':'V',
 'a':'TPAB','i':'CZ','n':'MQ','e':'EG','m':'SDX'}
# Figure 8 lines: (cipher, Lasry's plaintext) -- '|' marks clear-text breaks, dropped
F8 = [("mealtmvJveaadenletelrlmemidtltstes","DEPVISLALETTREQVEIEVOVSESCRIVIHIER"),
      ("JmledatdnlrgJmrggeJltrldmslaJddemaJl","ADVERTIRQVONADONNEAVIOVRDHVTARRESTAV"),
      ("aJduenegaanltrdmrgge","PARLEMENTQVIORDONNE"),
      ("meaLaeimemetrtgmde".replace('L','l'),"DEPVTEZDESEIOINDRE"),
      ("Jieuuemmemr gJuaemmeveadtgiemeirgatarldtgmtmaed".replace(' ',''),"ACEVXDESONALTESSELEPRINCESECONTIPOVRINSISTER"),
      ("JmenJgmedveurtegenegamliJdmtgJunJiJdtg","ADEMANDERLELOIGNEMENTDVCARDINALMAZARIN"),
      ("JademieuJmeuadlaalde","APRESCELADELARVPTVRE"),
      ("nleuuemnemldemtutJJadeJmdeuJmemmlm","QVELLESMESVRESILIAAPRENDRELADESSVS"),
      ("geirgiuleidtegarldaJJa","NECONCLVEZRIENPOVRTANT"),
      ("geJJtemuemedgted","NAIESLEDERNIER"),("Jmltm","ADVIS"),
      ("euueJddtleneaaeilrlmegemaJameg","ELLEARRIVEMETTEZVOVSENESTATDEN"),
      ("cJitutaedueemmltaaem","FACILITERLESSVITTES")]
bad=0; n=0
for c,p in F8:
    if len(c)!=len(p): print('LEN',len(c),len(p),c,p); continue
    for x,y in zip(c,p):
        n+=1
        if y not in KEY.get(x,''): bad+=1; print('miss',x,'->',y,'in',p)
print(f'{n-bad}/{n} signs consistent with the key')
# the open name in f.113r: 'Monsieur me | ae gi dJgme' (read from the leaf)
import itertools
w='aegidJgme'
print('name reads as', ['/'.join(KEY[x]) for x in w])
