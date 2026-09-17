# One-off patch: register the Feuquières write-up in the site sources (run once, then _build_queue.py and _build_site.py).
import re, pathlib
HERE = pathlib.Path(__file__).parent

# 1. _build_site.py: page manifest and image
p = HERE / '_build_site.py'
s = p.read_text(encoding='utf-8')
entry = """    dict(slug='feuquieres', label='Feuqui&egrave;res', year='1691', y=1691, place='Pignerol &rarr; Suze', st='solved', stt='read',
         title='Feuqui&egrave;res to Catinat &mdash; the petit chiffre of the Pignerol governors',
         blurb='The 418-group despatch of 25 January 1691 that the 1819 editor of Catinat&rsquo;s papers could not read and Bazeries read but never printed. The same edition prints a second letter in the same 367-group code, Louvois to d&rsquo;Herleville of 6 September 1690, with its contemporary translation; the two letters share 72 groups, and hand alignment carried between them reads 586 of their 601 tokens. Feuqui&egrave;res&rsquo; plan for the surprise of Veillane: two roads into the town, eighty horse to Saint-Ambroise, an attack at two points, and the dragoons not to be let escape into the castle.',
         quote='&ldquo;j&rsquo;attaqueray [par] deux endrois, et surtout &hellip; prendray garde que les dragons ne puissent m&rsquo;eschaper&rdquo;',
         rights='Page images: Bayerische Staatsbibliothek, CC BY-NC-SA'),
"""
if "slug='feuquieres'" not in s:
    s = s.replace("    dict(slug='hyde',", entry + "    dict(slug='hyde',", 1)
    s = s.replace("IMAGES = {'richelieu': None, ", "IMAGES = {'richelieu': None, 'feuquieres': ('feuquieres_p283.jpg', 'Mémoires de Catinat 1819, vol. II p. 283, the ciphered despatch', 'Bayerische Staatsbibliothek'), ", 1)
p.write_text(s, encoding='utf-8')

# 2. _build_queue.py: the attempted entry becomes a read entry
p = HERE / '_build_queue.py'
s = p.read_text(encoding='utf-8')
new_q = '''    ("Feuqui&egrave;res to Catinat, Pignerol, 25 January 1691", "1691",
     "feuquieres.html", "", "read (586 of 601 tokens)", "hi",
     "<b>Read, September 2026.</b> The 1819 <i>M&eacute;moires de Catinat</i> print the 418 groups; collated with the Munich page images. The code is the "
     "<i>petit chiffre</i> of the Pignerol governors, the 367-group companion of Bazeries&rsquo; Grand Chiffre de 1691 (his table transcribed from Gallica and "
     "verified on four despatches of 1690&ndash;91). A second letter in the same code, Louvois to d&rsquo;Herleville of 6 September 1690, sits in vol. I of the "
     "same edition with its contemporary translation, found by searching the OCR of all three volumes; the two letters share 72 groups. Exact aligners and "
     "annealers all failed (the translation paraphrases; <i>u</i>/<i>v</i>, <i>i</i>/<i>j</i> are one letter); one 31-group stretch where a single segmentation "
     "makes every repeated group agree, carried between the two letters by hand, reads the rest: 167 of 179 groups. Feuqui&egrave;res has Catinat&rsquo;s letter "
     "of the 24th at ten in the morning, is ready, cannot see how to pass the eighty horse to Saint-Ambroise, names the two roads into Avigliana and will keep the "
     "dragoons from escaping. Twelve singleton groups remain. <a href=\\"feuquieres.html\\">Write-up &rarr;</a>"),
'''
s2 = re.sub(r'    \("Feuqui&egrave;res to Catinat, Pignerol, 25 January 1691", "1691",.*?Notes &rarr;</a>"\),\n', new_q, s, count=1, flags=re.S)
assert s2 != s, 'queue entry not found'
p.write_text(s2, encoding='utf-8')

# 3. index.html: recent finding, featured slide, closed row, counts, date
p = HERE / 'index.html'
s = p.read_text(encoding='utf-8')
finding = ('<li><b>Feuqui&egrave;res to Catinat, 1691</b> &mdash; <span class="fnd">read; a Louis XIV war plan, the first reading since Bazeries&rsquo; unpublished one of 1893.</span> '
           'The code is the petit chiffre of the Pignerol governors, and a second letter in it, Louvois to d&rsquo;Herleville of 6 September 1690, is printed with its translation in '
           'vol. I of the same 1819 edition. Every aligner and annealer failed; hand anchoring carried between the two letters reads 586 of 601 tokens. Feuqui&egrave;res is ready, names the '
           'two roads into Avigliana, cannot see how to pass the eighty horse to Saint-Ambroise, and will keep the dragoons from escaping into the castle. <a href="feuquieres.html">Full write-up &rarr;</a></li>\n')
if 'read; a Louis XIV war plan' not in s:
    s = s.replace('<ul class="findings">\n', '<ul class="findings">\n' + finding, 1)
    # the older finding line: note that it is superseded
    s = s.replace('<li><b>Feuqui&egrave;res to Catinat, 1691</b> &mdash; <span class="fnd">Bazeries read it in 1893 and never printed it.</span>',
                  '<li><b>Feuqui&egrave;res to Catinat, 1691</b> (earlier session) &mdash; <span class="fnd">Bazeries read it in 1893 and never printed it; since read, see above.</span>', 1)
slide = '''<div class="bn-panel hasart" role="group" aria-roledescription="slide" hidden>
<div>
  <span class="tag">&#9733; Read &middot; 1691</span>
  <h2 id="feuquieres-to-catinat-the-veillane-plan">Feuqui&egrave;res to Catinat: a Louis XIV war plan read for the first time since 1893</h2>
  <p>The 1819 editor of Catinat&rsquo;s papers printed the despatch in figures and gave up on it; Bazeries read it and never printed the text. The break is a second letter in the same 367-group <em>petit chiffre</em>, Louvois to the previous governor of Pignerol, which the same edition prints with its translation. Hand alignment carried between the two letters reads the plan for the surprise of Veillane: two roads into the town, eighty horse to Saint-Ambroise, an attack at two points, and the dragoons not to be let escape into the castle.</p>
  <div class="stat2"><div><b>586 of 601</b><span>tokens of the two letters read</span></div><div><b>72</b><span>groups shared by the two letters</span></div><div><b>0</b><span>automatic solvers that got anywhere</span></div></div>
  <a class="cta" href="feuquieres.html">Read the write-up &rarr;</a>
</div>
<figure class="art"><img src="feuquieres_p283.jpg" alt="Page of the Feuquières to Catinat cipher despatch, 1691" loading="lazy"></figure>
</div>
'''
if 'feuquieres-to-catinat-the-veillane-plan' not in s:
    s = s.replace('<div class="bn-panel hasart" role="group" aria-roledescription="slide" hidden>\n<div>\n  <span class="tag">&#9733; Solved &middot; 1634&ndash;35</span>',
                  slide + '<div class="bn-panel hasart" role="group" aria-roledescription="slide" hidden>\n<div>\n  <span class="tag">&#9733; Solved &middot; 1634&ndash;35</span>', 1)
row = ('<tr class="done"><td><a href="feuquieres.html">Feuqui&egrave;res to Catinat, Pignerol</a></td><td>1691</td><td><span class="st solved">read</span></td>'
       '<td>Petit chiffre of the Pignerol governors recovered from a second letter in the code printed with its translation in the 1819 edition; 586 of 601 tokens read, the surprise of Veillane planned in the clear for the first time since Bazeries.</td></tr>\n')
if 'feuquieres.html">Feuqui&egrave;res to Catinat, Pignerol</a></td>' not in s:
    s = s.replace('<tr class="done"><td><a href="armstrong.html">Armstrong to Madison, coded postscript</a>', row + '<tr class="done"><td><a href="armstrong.html">Armstrong to Madison, coded postscript</a>', 1)
s = s.replace('19 items closed: 9 solved or read here,', '20 items closed: 10 solved or read here,')
p.write_text(s, encoding='utf-8')
print('patched')
