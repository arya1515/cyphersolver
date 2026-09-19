# Transcription brief (Kauderbach 1754-58, KHA inv. 201)

Images: kauderbach1754/img/IMG_R<rec>_I<img>_P<n>.png (5472x3648). The pages are photographed ROTATED: text runs
vertically. Rotate the crop so text reads left-to-right (try rotate(-90) i.e. clockwise; check it's not upside down).
Downscaled previews in kauderbach1754/sm/.

Each page mixes clear French with cipher: continuous runs of digits (no reliable spaces), with clear abbreviations
inside the runs such as `E.M.`, `C./.`, `Q./.`, `M./.`, `S./.`, `J./.`.

Output: kauderbach1754/trans/R<rec>.txt, format as DECODE:
  #IMAGE NAME: <file>
  <CLEARTEXT FR ...clear words...>
  digits one manuscript line per line, NO spaces inside a digit run (write 14241932254) ...
  clear markers inline as <CLEARTEXT FR M./.>
Mark an uncertain digit with ? after it (e.g. 7?). Watch 1/7, 4/9, 0/6, 3/5 and loops of 8.
Method: use PIL to crop each manuscript line (about 1/20 of page height, full width) at native resolution,
rotate, save to kauderbach1754/sm/crop_<rec>_<p>_<line>.jpg, then Read it. Transcribe every digit.
Append to the output file after EACH page (do not hold everything until the end).
Final report: pages done, digit count per page, any unreadable spots.
