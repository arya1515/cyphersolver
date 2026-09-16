# Shared-key ciphertext: Charost to ? (Calais, 3 July 1673, Mel. Colbert 172 f.23) and abbe de Gravel to Maulevrier (Mainz, 16 Aug 1674, Mel. Colbert 168bis ff.553-554)
C = "484 325 199 466 113 325 382 326 484 417 433 142 205 141 55 365 417 371 165 372 52 365 417 433 466 433 75 371 469 415 306 253 439 325 466 141 469 327 433 372 488 489 166 369 415 466 143 163 481 487 365 417 437 415 483"
G1 = "83 90 67 400"                       # qu'on en veut a [...] et que c'est a quoy sont destinees toutes les troupes
G2 = "433 168 75 282 284 415 75 481 141 481 79 141 112 474 141 287 327 99 481 415 199"   # luy ay propose de [...] de les bien observer
G3 = "284 75 282 284 415 251 247 139 417"  # il est party ce matin pour [...] et il m'a asseure
G4 = "253 302 416 369 415 468 415 352"     # des amis et des connoissances [...] un estat au vray de toutes choses
G5 = "439 481 433 385 253 75 437 415 484"  # fort cognu du marquis de Bade. [...]. Apres cela
PASSAGES = {'C':C,'G1':G1,'G2':G2,'G3':G3,'G4':G4,'G5':G5}
def toks(s): return [int(x) for x in s.split()]
