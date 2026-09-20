import json

pages = {286:"5-6",287:"10-12",288:"35-37",289:"40-42",290:"46-47",291:"55-57",292:"62-64",
         293:"68-70",294:"75-76",295:"80",296:"83-84",297:"97-99",298:"90-91",299:"105",
         300:"109-110",301:"113-114",302:"119-120",303:"124-125",304:"130-131",305:"135-136",
         306:"140-142",307:"146-147",308:"152",309:"155-156",310:"163-165",311:"174-176",
         312:"181-183",313:"192-193"}
meas = {286:3573,287:5053,288:3230,289:6460,290:3059,291:6739,292:6727,293:6719,294:1713,
        295:1051,296:3561,297:9070,298:2197,299:1133,300:2500,301:3742,302:4089,303:2475,
        304:4533,305:3037,306:9332,307:3550,308:854,309:959,310:7870,311:6929,312:6517,313:2259}

ED = ("Kiewning, Nuntiaturberichte aus Deutschland IV/2, Nuntiatur des Pallotto 1628-1630, "
      "Bd. 2: 1629 (Berlin 1897), the despatches headed 'dechiffr.', printed from "
      "ASV Nunz. di Germania 119")

docs = []
for r in sorted(pages):
    d = {
        "id": "R%d" % r,
        "shelfmark": "BAV, Barb.lat. 6960, pp. %s (DigiVatLib pagination); DECODE R%d" % (pages[r], r),
        "year": 1629,
        "country": "Papacy",
        "route": "Vienna -> Rome",
        "language": "Italian",
        "cleartext_in_document": "separate passages",
        "plaintext": {"location": ["printed edition"], "source": ED, "partial": True},
        "length": {"tokens": meas[r], "unit": "symbols", "measured": True,
                   "file": "decode/R%d.txt" % r},
        "transcription": {
            "by": "DECODE",
            "source": "DECODE DOC_R%d_*.txt, transcribed 2019-20 by volunteers" % r,
            "image_quality": "poor",
            "notes": ("Digits only; the transcription records single digits, so the manuscript's "
                      "grouping is lost. Tokens measured are digits, not code groups; the code "
                      "width is undetermined."),
        },
    }
    if r == 286:
        d["date"] = "4 Aug 1629"
        d["pages"] = 2
        d["transcription"]["notes"] += (" Line 1 of p. 5 was re-read here from the image and differs "
                                        "from DECODE's by about six digits in 74, including a "
                                        "two-digit length difference; line 2 matched.")
    docs.append(d)

prof = {
 "schema_version": 1,
 "target": "pallotto1629",
 "title": "Pallotto to Barberini, 1629 - 28 ciphered despatches of the nuncio at Vienna (BAV, Barb.lat. 6960)",
 "documents": docs,
 "system": {
   "types": ["undetermined"],
   "summary": "Numeric cipher written as an unbroken digit stream; the code width could not be established and the key was not recovered.",
   "symbol_kind": "digits",
   "digit_groups": {"width": "unknown", "separation": "contiguous"},
   "distinct_symbols": 10,
   "diacritics": {"used": False,
                  "note": "None recorded by the DECODE transcribers; the images are too coarse to see whether the hand marks any figure."},
   "homophones": {"used": True},
   "nomenclator": {"present": False},
   "nulls": {"present": False},
   "key_order": "unknown",
   "word_division": "none",
   "notes": ("112,805 digits over the 28 ciphertexts. Digit frequencies are uneven (0 = 16.1%, 4 = 4.8%) "
             "and adjacent digits carry ~0.18 bits of mutual information, so the stream is structured. "
             "No phase preference was found for two-digit codes (IC 0.01462 at phase 0 vs 0.01466 at "
             "phase 1; even- and odd-position digit distributions agree to 0.2%) or for three-digit "
             "codes, which is also what frequent one-digit transcription slips would produce. "
             "distinct_symbols is the digit alphabet, not the key's code groups, which are unknown."),
 },
 "conditions": {
   "prior_solution": {
     "exists": "in print",
     "where": ("Hans Kiewning (ed.), Nuntiaturberichte aus Deutschland nebst ergaenzenden "
               "Aktenstuecken IV/2, Nuntiatur des Pallotto 1628-1630, Bd. 2: 1629 (Berlin 1897); "
               "archive.org item 4-2_20200807. Prints the contemporary Roman decipherments, headed "
               "'dechiffr.', from ASV Nunz. di Germania 119."),
     "found": "during attempt",
     "used": True,
   },
   "inputs": ["images", "transcription", "cleartext context", "published reading", "crib"],
   "attack": "crib",
   "human_role": "set the target; nothing else",
   "tools": ["banded DP crib aligner (align2.py, align3.py, align4.py, soft.py, walk.py, syll.py)",
             "fixed-multiset simulated annealing homophonic solver (hill2.py)",
             "space-free Italian 5-gram model built here from lang/corpora it-renaissance + it-gutenberg (12.0M chars, it_clean5.npy)",
             "DigiVatLib IIIF", "DECODE JSON API and filesrv"],
   "models": ["claude-opus-5[1m]"],
   "sessions": 1,
   "first_date": "2026-09-20",
   "last_date": "2026-09-20",
 },
 "solution": [
  {"date": "2026-09-20", "kind": "access",
   "what": "Found the manuscript free on DigiVatLib (Barb.lat. 6960, 194 canvases) and fetched the IIIF manifest; the service maximum is 748x1088 px per page, an old bitonal microfilm scan.",
   "result": "partial"},
  {"date": "2026-09-20", "kind": "access",
   "what": "Mapped DECODE R286-R313 to DigiVatLib page ranges from each record's additional_information; established that the volume interleaves cipher sheets with clear register pages.",
   "result": "worked"},
  {"date": "2026-09-20", "kind": "literature search",
   "what": "Searched for a printed decipherment; found Kiewning 1897 (Nuntiatur des Pallotto, Bd. 2: 1629) in full text on archive.org, which prints some forty of Pallotto's 1629 despatches marked 'dechiffr.'.",
   "result": "worked"},
  {"date": "2026-09-20", "kind": "verification",
   "what": "Matched R286 (pp. 5-6, headed 'Di Vienna 4 di Agosto') to Kiewning Nr. 153, and checked that the clear pages 3-4 and 7-9 run continuously through the cipher sheet with the edition's wording; separately matched p. 13 verbatim to Nr. 153 Beilage II.",
   "result": "worked"},
  {"date": "2026-09-20", "kind": "transcription",
   "what": "Downloaded DECODE's 2019-20 digit transcriptions of all 28 ciphertexts (DOC_R*.txt) with the stored session cookie.",
   "result": "worked"},
  {"date": "2026-09-20", "kind": "crib",
   "what": "Aligned the opening of R286 against the known opening of Nr. 153 as two-digit codes: 27 letters align exactly (HORICEVUTALARISPOSTADATAMII) with two independent repeat confirmations, 38=T and 23=I.",
   "result": "partial"},
  {"date": "2026-09-20", "kind": "solver",
   "what": "Ran banded DP EM aligners over the whole of R286 against a hand-corrected 3,359-letter crib of Nr. 153, with two-digit codes plus one-/three-digit resync operations for transcription slips; best code-to-letter consistency about 55%, against a 20% naive baseline.",
   "result": "partial"},
  {"date": "2026-09-20", "kind": "statistics",
   "what": "Tested for a fixed code width: index of coincidence and positional digit distributions by phase for two- and three-digit codes across all 28 ciphertexts. No phase preference at all.",
   "result": "ruled out"},
  {"date": "2026-09-20", "kind": "solver",
   "what": "Fixed-multiset simulated annealing over the 100 two-digit codes on 5,000 codes, scored by a space-free Italian 5-gram model built here; -3.54 log-prob per character against -1.5 for real Italian.",
   "result": "failed"},
  {"date": "2026-09-20", "kind": "hypothesis",
   "what": "Tested a syllabic two-digit nomenclator by aligning codes to plaintext spans of one to four letters; every well-attested code collapsed to a single letter, so no syllable table.",
   "result": "ruled out"},
  {"date": "2026-09-20", "kind": "control",
   "what": "Re-read line 1 of p. 5 from the image and compared with DECODE's transcription: agreement on the first 22 digits, then about six differences in 74 digits including a two-digit length difference; line 2 matched almost exactly. A dropped or inserted digit flips the code phase for the rest of a line, which accounts for both the missing phase signal and the broken alignments.",
   "result": "worked"},
  {"date": "2026-09-20", "kind": "reading",
   "what": "Content of the despatches recovered from Kiewning's printed contemporary decipherment, not from the cipher: Pallotto's mediation between the Emperor and the French envoy Sabran over the Mantuan succession, Casale, Susa and the Grisons passes, Aug-Nov 1629.",
   "result": "worked"},
 ],
 "outcome": {
   "class": "already solved",
   "verification": ["contemporary decipherment", "independent clear copy", "historical consistency"],
   "notes": ("The catalogue said 'what the cipher hides is not known'; it is known, and has been in print "
             "since 1897, from the Roman office's own decipherments. The cipher itself was not broken "
             "here: the key is not recovered and the code width is undetermined. The block is the source "
             "material - at 748 px per page the figures are about ten pixels wide, and DECODE's digit "
             "transcriptions carry slips often enough to break a letter-level alignment every ~27 letters. "
             "Since the plaintext of every passage is known from Kiewning, a fresh accurate transcription "
             "from better images would very likely give the key."),
 },
}

with open('profile.json', 'w', encoding='utf-8') as f:
    json.dump(prof, f, indent=1, ensure_ascii=False)
print('written', len(docs), 'documents')
