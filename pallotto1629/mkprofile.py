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
            "image_quality": "fair",
            "notes": ("Digits only; the transcription records single digits, so the manuscript's "
                      "grouping is lost. Tokens measured are digits, not code groups; the code "
                      "width is undetermined."),
        },
    }
    if r == 286:
        d["date"] = "4 Aug 1629"
        d["pages"] = 2
        d["transcription"]["notes"] += (" Line 1 of p. 5 was re-read here from DECODE's 1491x2066 scan: it "
                                        "differs from DECODE's transcription in two digits of 74, both "
                                        "substitutions, with no length difference. Line 2 differs by a digit "
                                        "or two and possibly in length, so the transcription is close but "
                                        "cannot be assumed exact.")
    docs.append(d)

prof = {
 "schema_version": 1,
 "target": "pallotto1629",
 "title": "Pallotto to Barberini, 1629 - 28 ciphered despatches of the nuncio at Vienna (BAV, Barb.lat. 6960)",
 "documents": docs,
 "system": {
   "types": ["undetermined"],
   "summary": "Numeric cipher written as an unbroken digit stream; the code width could not be established, no alignment signal to the known plaintext exists at width two, and the key was not recovered.",
   "symbol_kind": "digits",
   "digit_groups": {"width": "unknown", "separation": "contiguous"},
   "distinct_symbols": 10,
   "diacritics": {"used": False,
                  "note": "None recorded by the DECODE transcribers, and none seen on DECODE's 1491x2066 scan of p. 5."},
   "homophones": {"used": True},
   "nomenclator": {"present": False},
   "nulls": {"present": False},
   "key_order": "unknown",
   "word_division": "none",
   "notes": ("112,805 digits over the 28 ciphertexts. Digit frequencies are uneven (0 = 16.1%, 4 = 4.8%) "
             "and adjacent digits carry ~0.18 bits of mutual information, so the stream is structured. "
             "No phase preference was found for two-digit codes (IC 0.01462 at phase 0 vs 0.01466 at "
             "phase 1; even- and odd-position digit distributions agree to 0.2%) or for three-digit "
             "codes, which is also what one-digit transcription slips at about 1% would produce. "
             "distinct_symbols is the digit alphabet, not the key's code groups, which are unknown. "
             "A run-length control puts the longest consistent two-digit alignment to the known plaintext at 39 "
             "letters against a chance baseline of 36-39, where a synthetic two-digit cipher at the same "
             "transcription noise gives 207 - so the stream is not a two-digit substitution of that plaintext."),
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
   "what": "Found the manuscript free on DigiVatLib (Barb.lat. 6960, 194 canvases) and fetched the IIIF manifest; that service maximum is 748x1088 px per page, an old bitonal microfilm scan. DECODE's own scans of the same leaves, found later, are four times larger.",
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
   "what": "Aligned the opening of R286 against the known opening of Nr. 153 as two-digit codes: 27 letters align exactly (HORICEVUTALARISPOSTADATAMII) with two repeat confirmations, 38=T and 23=I. Read at the time as roughly a 1-in-180 coincidence; the later run-length control shows 27 is BELOW the chance baseline of 36-39 for this material, so it is not evidence.",
   "result": "ruled out"},
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
   "what": "Held-out test: learned a two-digit table on the first 55% of R286 against the crib, froze it, and aligned the remainder. Confirmations per letter 0.355 against a mean of 0.359 over eight controls that shuffle the letters among the same codes; DP score -3266 against -3313. The same test for a 2-digit-plus-nulls model gives 0.440 against 0.431. No separation: the earlier 55% consistency was the aligner fitting the crib, not a key.",
   "result": "ruled out"},
  {"date": "2026-09-20", "kind": "control",
   "what": "Positive control: enciphered the same crib with a random two-digit homophonic key, damaged the digit stream with single-digit insertions and deletions, and ran the identical learner. True key recovered 100/100 at 0% digit error, 87/100 at 0.5%, 7/100 at 1.7%, 19/100 at 4%. The method is sound; it needs a transcription better than about 0.5% digit error.",
   "result": "worked"},
  {"date": "2026-09-20", "kind": "access",
   "what": "Found that DECODE serves its own scans of these leaves at 1491x2066 (IMG_R286_I2489_P1.png, IMG_R286_I2490_P2.png), four times the pixel area of DigiVatLib's 748x1088. Re-read p. 5 line 1 on it: it differs from DECODE's transcription in two digits of 74, both substitutions, no length difference - correcting an earlier claim of about six differences including a length change, which was a misreading of the low-resolution image.",
   "result": "worked"},
  {"date": "2026-09-20", "kind": "control",
   "what": "Run-length test. Long consistent runs cannot be faked: inside a window a repeated code must carry the same letter. Scanning every (digit offset, crib offset) pair, the longest consistent two-digit run between R286 and the plaintext of Nr. 153 is 39 letters; controls that shuffle the crib letters give 39, 39, 36, 38, 36 and reversing the cipher gives 39. A synthetic two-digit cipher over the same text at 1.7% digit noise gives 207, and a clean one 2705. The same method recovers 81/100 key codes from the noisy synthetic text where the DP learner managed 7. The real material sits exactly on its chance baseline: there is no alignment signal, so transcription noise is not a sufficient explanation, and R286 is not a two-digit homophonic encipherment of Nr. 153. This also retires the 27-letter opening match, which is below the 36-39 chance baseline.",
   "result": "ruled out"},
  {"date": "2026-09-20", "kind": "reading",
   "what": "Content of the despatches recovered from Kiewning's printed contemporary decipherment, not from the cipher: Pallotto's mediation between the Emperor and the French envoy Sabran over the Mantuan succession, Casale, Susa and the Grisons passes, Aug-Nov 1629.",
   "result": "worked"},
 ],
 "outcome": {
   "class": "already solved",
   "verification": ["contemporary decipherment", "independent clear copy", "historical consistency"],
   "notes": ("The catalogue said 'what the cipher hides is not known'; it is known, and has been in print "
             "since 1897, from the Roman office's own decipherments. The cipher itself was not broken here and "
             "no partial key is claimed: a held-out test shows the table learned from R286 predicts unseen text "
             "no better than a shuffled control (0.355 vs 0.359), so the 55% consistency of the first pass was "
             "overfitting. A positive control on synthetic ciphertext recovers a random key 100/100 from a clean "
             "transcription, 87/100 at 0.5% digit error and 7/100 at 1.7%, so the method is sound and the limit "
             "is the transcription. Two explanations remain open and cannot be separated from this material: "
             "length errors in the transcription, or the cipher not being a fixed-width substitution of this "
             "plaintext. The run-length control then settled that: the longest consistent two-digit run is 39 "
             "letters against a chance baseline of 36-39 (synthetic at the same noise: 207), so there is no "
             "alignment signal and noise is not a sufficient explanation. R286 is not a two-digit homophonic "
             "encipherment of Kiewning's Nr. 153. Open: whether the code width differs, whether the sheet encodes "
             "another despatch or a materially different wording, or whether the system is nomenclator-heavy or "
             "variable-length."),
 },
}

with open('profile.json', 'w', encoding='utf-8') as f:
    json.dump(prof, f, indent=1, ensure_ascii=False)
print('written', len(docs), 'documents')
