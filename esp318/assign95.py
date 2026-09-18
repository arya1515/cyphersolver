# cluster id (fcluster maxclust=110 on f122r_glyphs.pkl) -> letter, read off the montages
# against George Lasry's 2022 alphabet for BnF Espagnol 318 f.122 (published by S. Tomokiyo).
MAP = {
 'C': [5, 3],
 'R': [4, 1, 2, 106],
 'N': [7, 6, 8, 9, 36],
 'E': [47, 43, 73, 72, 42, 48, 75, 56],
 'D': [103, 59, 35, 21],
 'S': [105, 104, 97],
 'U': [30, 28, 33, 29],
 'Q': [54],
 'T': [102, 101, 110],
 'O': [67, 68, 71, 69, 95, 79, 93, 70, 98],
 'A': [77, 82, 86, 81, 84, 88, 80, 83, 100, 89],
 'I': [39, 52, 37, 46],
 'M': [92, 91, 90, 34, 53],
 'Y': [107],
 'P': [61],
 'L': [32],
 'H': [41],
 'G': [44, 45],
 'B': [40, 96],
}
CL2L = {c: L for L, cs in MAP.items() for c in cs}
