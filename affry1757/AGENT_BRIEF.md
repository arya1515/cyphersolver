# Brief: align a d'Affry 1757 code letter with its contemporary decipherment

Folder: C:\Users\dbour\cypher\affry1757 . Intercepted letters of the French ambassador d'Affry (The Hague, 1757)
in a numeric word-and-syllable nomenclator (groups 1-1199, homophones; a group stands for a word, a syllable,
a letter or a name fragment; 13 is often a full stop). The Dutch codebreaker Lyonet's decipherment
("clear copy") of some letters is among the page images.

Files:
- img/IMG_R<rec>_I<img>_P<n>.png : page images (5472x3648, text runs sideways). Make readable crops with
  `python crops.py img/<file>.png -90 <tag> 4` (writes sm/<tag>_0..3.jpg; try 90 if upside down) and view them.
- decode/DOC_R<rec>_*.txt : DECODE transcription (digits of the cipher; its CLEARTEXT lines are rough).
- cipher_U.txt : the parsed groups per record (line after "# R<rec>"). `python view.py U R<rec> a b` prints groups
  with the current shared key (key_U.json) underneath.
- plain/R1066.txt, plain/R1069.txt, plain/R1053.txt : finished examples of clear-copy transcriptions.

Task for record R<rec> (given in your prompt):
1. Identify which image page(s) carry the clear copy (French prose headed "N° ... D'A. à R." with a date, no digits)
   and which carry the cipher groups. Check: the clear copy's opening words should fit the first cipher groups
   (e.g. de=219/1018/1138, la=583/382, que=197, M/Mr=196, vous=569 in the key).
2. Transcribe the clear copy exactly (modern accents not needed; keep spelling), into plain/R<rec>.txt, only the part
   that corresponds to the cipher (a letter may also have clear passages in the original that were never ciphered:
   compare with the CLEARTEXT lines on the cipher pages and exclude those).
3. Align group by group: write align/R<rec>.tsv with one line per cipher group: index, group, plaintext value,
   confidence (H = forced by both neighbours or repeated, M = plausible, ? = unsure). Use the key as a guide but
   trust the plaintext; report conflicts with key_U.json in your final message.
4. Final message: page mapping, how many groups aligned H/M/?, list of conflicts, and the new values (group=value).
Do not edit key_U.json or any other file than plain/R<rec>.txt and align/R<rec>.tsv. Do not commit.
Work text-only after transcription; do not view more than ~12 image crops.
