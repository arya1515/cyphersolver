# JACAR B03050089100, frames C: transcriptions and decodes

Frames 01, 02, 05, 06, 07, 09, 10, 11, 15, 22, 23, 24, 27, 28, 29 (JACAR frame = 60 + NN).

## Key finding
Every condenser telegram in this set **between Tokyo and Shanghai** (Tokyo → Junzaburo and Shanghai → Linwailuk, in both directions) reads under **one key**:
`rot12 euioa`, vowel-major. famtest now lists it as `yamada1916 = (12,'euioa',0)`, and the family search reports the same key as `rot12 euioa vow off1 add0`.
The Manila → Tōyama telegram (frame 22 top) uses a **different key**, `rot2 euaoi` vow off1 (not the old `manila1916`).

The same few errors keep coming back, from the clerk or from the hand (see the per-word notes):
- **g↔q** (the most common): gebo→qebo 使, gori→qori 誰, gice→qice 皓, gire→qire 百, gogi→qogi 請, gopo→qopo 謀, quso→guso 漾, goqu→gogu 頭.
- **x↔d**: xidi/xixi 篠, dunu→xunu 東, dosi→dodi 隨, delo→xelo 各, deha→xeha 否.
- Also s↔x/z, b↔f, h↔k, v↔x, r↔h, a↔o.

Two codebook oddities:
- 1307 (孀) appears twice where no reading fits.
- "jede" 1511 崗 appears twice where 崎 (1505) is expected.

The 滬 group appears as "gulu" 3337, which is correct: it is clean in frames 27 and 28. The "guli" (3357 漭) reading in frames 01 and 05 is a misreading or misspelling of it.

Sender conventions:
- Tokyo telegrams to Junzaburo end with the signature **持** (quco) plus a date character: 皓 19, 號 20, 箇 21, 漾 23, 有 25.
- On the Tokyo forms, "Address of sender" is 東京 and "Signature" is 林蔚陸 = "Linwailuk", Shanghai's address for the Tokyo side.

z-scores are from `famtest.py` on the words as transcribed. A correction marked with → is an emendation made from the key.

---

## T1: frames 01–02 (4 sheets: (1), (2) on f01; (3), (4) on f02)
Forwarded. Tokio → **Junzaburo Shanghai**. No. 01125, class P, 58/57 words, 17/5/1916, 8.10 pm. Prefix "Thirtyseventh" is plain text.

Transcription (sheet by sheet):
```
f01(1) veraxesaxu bekeqivoyo qedodedudu pisofamuxo xejeqikotu podogadefo payelezuxo soxigapadi
       tupasotagu l[u]gedunufu teditudeli cevepohode xerarerexu nasuroxidi tupotegudo pogedunufu tukivehipa
f01(2) xigitobeku buziseqixu qexetodoro memudohabe hugeyepaso qirebejico d[b]bofuhefo fi[p]ozojicu
       livu[r]ijoda reramepaye cemo[v]ubepi vetojedove pegegekebi padugur[b]oso(11 letters) dilubovisa
       padumemuxo dinenegive xocagesitu
f02(3) jinucoxezo xehaqebese xodo[s]ixege firapalibu [z]ixosivevo dupipadopa goxeriheri jevey[o]sepa
       n[?]yugigomo(9 letters, doubtful) zuhazocicu xigorase[q]i nufupikitu popaxaxosu vubapanis[u] hamuyebe[g]o
       [q]ebilicede hatesogofe sokis[o]hepa
f02(4) ziquhoxixi
```
Emendations, as written → read:
- guli/lil → gulu 滬
- dibofuhefo: written "difofuhefo", read with b, giving bofu 錫
- fikozojicu → fipo 與
- livuhijoda → vuri 暗
- cemoxubepi → movu 黨
- paduguroxo: 11 letters written, read as padu|guro|xo = 主漸進
- xododixege → dodi 隨
- cixosivevo → buzi 欲
- vubapanizu → zuha 機
- beqo 在
- qebilicexe → qebi 何 and xeha 否

Key: rot12 euioa. **z = 11.3** on the corrected stream, 8.9 as first read.

Decode:
> 午后本庄轉來天津趙瑾卿真日電如下：張運籌[乾?]效赴滬，學生到敝處卅餘名，保校擬篠日分離。學生於北九[芳→州?/省?]，因欲先期召集，急需四[孀=千?]五百圓。閻錫山與金永暗鬥，傾心吾黨；土匪已動。孔庚主漸進，王等主急進，惟[舵?]遵守方略。可否令其隨卽舉事，欲速匯津[亠亢?]。又尾崎還[乎?][梵?]飛機，[重民飢?]先生言日人送有二機，現在何處？否則須購買也。[按?]篠

Gist: forwards Zhao Jinqing's Tianjin telegram of the 11th (真).
- Zhang Yunchou leaves for Shanghai on the 19th (效). Over 30 students are at Zhao's place. The Baoding-school men will disperse on the 17th (篠). The students are to be called up early, and 4,?00 yen is urgently needed.
- Yan Xishan is secretly at odds with Jin Yong and leans toward "our party". Bandits are already moving. Kong Geng wants a gradual advance, Wang and others a rapid one.
- Asks whether they can be told to rise at once, and for money to be wired to Tianjin quickly.
- On Ozaki and the aircraft: "X-sensei says the Japanese sent two planes; where are they now? Otherwise we must buy."

The final pair should be sender and date. 按 (quho) is doubtful, and 篠 = 17th fits the date.

Still unresolved:
- 乾 (padi)
- 芳 (gito; qito = 省)
- 孀 (geye, 1307; 千 is expected)
- 舵 (give)
- 亠亢 (pado pago)
- 乎梵 (word "n?yugigomo", unreadable)
- 重民飢 before 先生 (a name?)
- 按 (quho)

---

## T2: frame 05 top
Forwarded. Tokio → **Junzaburo Shanghai**. No. 01425, class P, 16/15 words, 19/5/1916, 9.30 pm (sent 10.20 pm). Sender: 東京 林蔚陸. Prefix Thirtyseventh.

```
dogamevagi dadere[q]uka votezulece cunejonere padu[q]eboku hu[q]ori[q]ido piceseqinu fuvojibe[q]o
guligajoce vivesulice licepehire doqucoqice
```
Key: rot12 euioa. z = 4.5 as read; the text is clearly correct.

Decode:
> 電悉。英士捐軀，極堪慟悼。主使爲誰？盼(盻)覆。先生[輮?]在滬[鉼墓?]，務處處戒備。持皓

"Telegram received. Yingshi (Chen Qimei) has given his life; deeply mourned. Who was the instigator? Please reply. Sensei … in Shanghai …, be on guard everywhere. —Chi, 19th."

The doubtful groups are voji (輮, maybe 體) and gajo cevi.

## T3: frame 05 bottom
Forwarded. Tokio → **Junzaburo Shanghai**. No. 01325, class P, 12/11 words, 19/5/1916, 1 pm. Sender 林蔚陸. Prefix Thirtyseventh.

```
gidadereni xutenire[q]e veradefoze bigidopice yunapahepa riyejibupi dutapabubu qaqucoqice
```
Key: rot12 euioa. z = 4.5 for the family's best key; the yamada key is not ranked first on this short text, but it reads.

Decode:
> 英士被刺，傷[午→勢?]如何？盼覆。楊[丙?]乘[哀歌?]浦丸歸。持皓

"Yingshi stabbed: how are the wounds? Please reply. Yang … returning on the …-ura Maru. —Chi, 19th."

The "Yang" here links to T6, which is signed Yangsanpang from Sannomiya.

---

## T4: frame 06
Received at Tokio 3.01 pm 19/5/1916, from **Shanghai** No. 051, 12 words, sent 19/5 12.36 pm. To **Linwailuk Tokio** (林蔚陸).

```
gidadere[v]u xepayevera begohefonu [t]igeyonixu sesivojotu xuqumasesi pagepaxaco coqecaciho
turupaxage yetubupuce
```
Key: rot12 euioa. **z = 6.0**.

Decode:
> 英士昨下午在山田家被兇[轟?]斃，捕兇[一?]人，關係者數人。[孀?]文[疸?]

"Yingshi was shot dead by an assassin yesterday afternoon at the Yamada house. One assassin and several accomplices arrested."

Emendations: xuxe→vuxe 昨, bego→beqo 在, tige→nuti 田.

The last three groups (geye tubu puce) are unresolved, probably the signature and date. 1307 turns up here again.

## T5: frame 07
Forwarded. Tokio → **Junzaburo Shanghai**. No. 01525, 9/8 words, 20/5/1916, 9.30 am. Sender 林蔚陸. Prefix Thirtyseventh.

```
dojetumoxo varonuseqi nufujire[q]o gipehiredo mepafuka(8 letters)
```
Key: rot12 euioa. z = 4.1 (short text).

Decode:
> 陳旣遭變，先生萬[請/祈?]戒備。[心溜?]

"Chen has met with disaster; Sensei must take every precaution."

gogi is probably qogi 請. The last word should be 持號 (the 20th) but reads 心溜.

---

## T6: frame 09 top (clear code)
Forwarded. From **Sannomiya** (Kobe), No. 91, class m?, 15 words, 19/5/1916, 7.25 pm. Delivery station Aoyama. To **Nakayama, 109 Harajuku, Aoyama, Tokio** (中山 = Sun Yat-sen). Signed **Yangsanpang** (楊…).

Digits: `5390 1102 0689 6685 7181 4315 0694 0047 6010`
> 英(5391; clerk wrote 5390 = 苫) 士 君 遭 難 確 否 乞 覆

"Is it true Mr Yingshi has met disaster? Please reply." —Yang.

## T7: frames 09 bottom + 10 (3 sheets)
Forwarded. Tokio → **Junzaburo Shanghai**. No. 01635, class P, 28/27 words, 20/5/1916, 1.15 pm. Sender 林蔚陸. Prefix Thirtyseventh.

```
f09  gerojevege depahapije hefoxubegi tidequpiki keyabolije doredayece(written "doreddyece")
     movucuraso kixehavumo picehefodu nubinoyuci(doubtful) xerigidade
f10  refutageji dogadubade peseqinufu vesubelere donerasiga ronumemiru poyutexube cefuvozupa
     revupobego rexo[ab]mavo(not CV; unreadable) poreqasije xehazokepi | (3) cequcolihe
```
Key: rot12 euioa. **z = 6.1**.

Decode:
> 宮崎[子介?]見山本[𦬊夙?]言[廬→手?]鎗已[僦→備]，吾黨決購否？[曷→望?]覆。山[泯→東][罇?]械，又英士[湱→死?]，宜電海外。先生務嚴備，慮禍變恐搖根本。報載丁[曹?][坍→在]…[辛/身?]傷，確否？[醉?]覆。持號

"Miyazaki [?] saw Yamamoto [?], who says the [pistols?] are ready; will our party decide to buy? Reply. Shandong arms [?]. Also Yingshi's [death?] should be telegraphed overseas. Sensei must take strict precautions, fearing an upheaval that would shake the foundations. Papers report Ding … wounded; true? Reply. —Chi, 20th (號)."

The trailing "de" of f09 continues onto f10 as dere 士.

## T8: frame 11
Forwarded. Tokio → **Junzaburo Shanghai**. No. 00125, class P, 20/19 words, 21/5/1916, 5.40 pm. Sender 林蔚陸. Prefix Thirtyseventh.

```
dedudupije mabugobopa kufusuroge bogedunufu xoyidogoyi fazopobubi sexopalime muxofesuzu
bubidujono depaxagopo teyopagebo xaduyupaze gejisejosi sa[q]ogixosi curaxasipi cequcoxife
```
Key: rot12 euioa. **z = 7.7**.

Decode:
> 天津席正銘[爬?]擬[容?]學生，連[雖→電]索鉅款，其事急迫。撥款派[螅→軍?]人[食?]前[世?]辦法，不宜再[祧→緩]，請速決速覆。持箇

"Xi Zhengming in Tianjin plans to [gather?] students and has repeatedly wired demanding a large sum; the matter is urgent. Arrangements for allotting funds and sending men … must not be delayed further; please decide and reply quickly. —Chi, 21st (箇)."

Emendations: sisa→zisa 緩, gogi→qogi 請, xasi→xosi 速.

## T9: frame 15 (2 sheets)
Forwarded. Tokio → **Junzaburo Shanghai**. No. 00425, class P, 38/37 words, 23/5/1916, 1.20 pm. Sender 林蔚陸. Prefix Thirtyseventh.

```
yerefokuje boyosegulu qeviduyunu hifobegomo totulepase rolihe[q]edo tezupaqobe qodebuxoyi
deburequdu fimiya[g]egi sokivepoke zulebebujo zogapave[q]i revefayovi xudipe[y]abo li[q]irexuji
xemoxeqapa | (2) hososelejo selivuzayo sesevejebo pahogegidu fipanivemo seli[x]ubeyo fixezorudi
numugegigo fese[q]iteju ribipagopa [q]ogogidujo paxahefu[r]o [n]eruhudiho qegigegidu fipazerebi
goriteyupa ziquco[g]uso
```
Key: rot12 euioa. **z = 8.2**.

Decode:
> 吳非己還滬，住法界霞飛路廿六號。來函云：在大連大倉洋行定購卅年式步銃三百、卜郎林手鎗百枝，合同交貨後兩月還價；已交定洋二千兩，本部可提用。定須先[刈?]知[亢云?]，請派人就近接洽。[佚→該?]定洋不[偃顇?]出也。持漾

"Wu Feiji is back in Shanghai, at No. 26 Rue Joffre (霞飛路) in the French Concession. His letter says he has ordered, through the Okura trading company (大倉洋行) in Dalian, 300 Type-30 rifles and 100 Browning pistols. Under the contract, payment is due two months after delivery; a deposit of 2,000 taels has been paid, which headquarters can draw on. … Please send someone to deal with it on the spot. … the deposit cannot be … out. —Chi, 23rd (漾)."

Emendations: gedo→qedo 來, qegi→gegi 定, gire→qire 百 (twice), pexa→peya 手, jebo→jedo 已, sube→xube 本, segi→seqi 先, gogi→qogi 請, xose→xore 近, diho→duho 洽, quso→guso 漾.

---

## T10: frame 22 top
Received at Tokio 1.15 am 23/5/1916, from **Manila** No. 50, class P, 8 words. To **Toyama, Reinanzaka, Tokio** (頭山滿). Prefix "Eleventh".

```
qaseqovesa [qi]qefenuhi(written "yogefenuhi") gave[k]etido sacapedotu
```
Key: **rot2 euaoi**, vow off1 add0, a new key; `manila1916` does not read it. z = 4.4–4.5.

The plaintext 聞陳英士死確否請覆 fixes 16 syllable values, and 13 of them match this table exactly. The three that do not (yo, ge, xe) match as qi, qe, ke: q/y, g/q and x/k slips.

Decode:
> 聞陳英士死確否？請覆。[誠?]

"Heard Chen Yingshi is dead; is it true? Please reply." The last group dotu 誠 (61xx) is probably the signature.

## T11: frames 22 bottom + 23 top (2 sheets)
Received at Tokio 6.30 pm 22/5/1916, from **Shanghai** No. 0101, class P, 24 words, sent 22/5 2.24 pm. To **Linwailuk Tokio**.

```
f22  jemasofase lilicegedu nufupalite hubezureji voxabubiqo giyodavevo qebovoxage papalipeya
     bolijedopi yogerojede buqaxopopa luvuricupe padugopoku huhumakeci docegedide pezupijede
f23  qumaparere qavojukode jiqimepiqo gidevageko vipaqiqefe qekufohoki
```
Read row by row, left word then right word. Key: rot12 euioa. **z = 8.2**.

Decode:
> 席趙兩處學生事，切囑停辦；款請酌匯，使辦實事。手鎗已託宮崎(崗)歸。遣之暗殺主謀爲[炸府→政府?]。除官外[槩?]已捕丁[?]，傷輕，[魄→餘]無恙。請妥寄空白委[任]狀。馬

The key points of the message:
- The Xi and Zhao student business is to be stopped.
- Funds should be wired as appropriate, for real work.
- The pistols have been entrusted to Miyazaki (宮崎) to bring back.
- On those sent to assassinate: the instigator is [the government?].
- … Ding … arrested/lightly wounded; the rest are unharmed.
- Please send blank commissions.
- Ends 馬 = 21st.

Emendations: gepa→geja 實, gopo→qopo 謀, cupe→cuce 殺, huma→suma 政?, jiqi→juqi 無, kode→hode 餘, kufo→kufa 狀.

"jede" 崗 twice where 崎 is expected. The 丁 group (pare) is the same one as in T7 "報載丁…傷".

## T12: frame 23 bottom + frame 24 (clear English)
Received at Tokio 7.15 pm 22/5/1916, from **Melbourne** No. 190, class LC, 33 words, sent 22/5 10.10 am. To **LCO Dr Sunyatsen, 109 Harajuku, Tokio**.

> League received no acknowledgement onesixnaught pounds drafted you by wonglew on its behalf march last future address communications undersigned reply wongyonkwoong Chinese nationalist league russell | (2) street Melbourne

## T13: frame 27 top
Forwarded. Tokio → **Junzaburo Shanghai**. No. 00825, class P, 18/17 words, 25/5/1916, 5 pm. Sender 林蔚陸. Prefix Thirtyseventh.

```
[ge]dunufupa(written 8 letters "dunufupa"; a syllable is missing) liteyotupo jeboxocasi jidogadupi rejibufopa
gapaqovuzi sutovuzede haxezibose teyogebexo sipicecuta tupobucoxo qesetilecu lejosegebu qaqucovuba
```
As written, the stream is misaligned by one syllable and nothing in the family reads it (the best is z 4.1, noise). Restoring "ge" gives rot12 euioa, **z = 6.8**.

Decode:
> 學生事前日已遵示電津停止，今云暫擱是否？取[銷]前[孌?]，速覆。[沁?]日歡迎克強後[儉?]歸。持有

"The students affair: the day before yesterday, as instructed, we wired Tianjin to stop it. Now you say shelve it: is that so? Cancel the earlier …; reply quickly. … after welcoming Keqiang (Huang Xing) on the … th, [will] return. —Chi, 25th (有)."

## T14: frame 27 bottom
Forwarded. Tokio → **Junzaburo Shanghai**. No. 01125, class P, 8/7 words, 26/5/1916, 10.25 am. Sender 林蔚陸. Prefix Thirtyseventh.

```
cefuvozuse qi[nufu]vu[x]e(written "qinifuvuse") tupodopogu lusijexeha
```
Key: rot12 euioa. z = 4.6 (short text).

Decode:
> 報載先生昨日離滬，確否？

"Papers report Sensei left Shanghai yesterday; true?"

## T15: frame 28 top (clear English)
Received at Tokio 6.30 pm 23/5/1916, from **Johannesburg** No. 471, class LC, 19 words, sent 22/5 11.55 am. To **LCO Linwailok, 1 [?]chome Kidomachi Aoyama Tokyo**.

> Laiky cabled you seven hundred twenty five pounds why not reply Gamman

## T16: frame 28 bottom
Received at Tokio 7.30 pm 24/5/1916, from **Shanghai** No. 065, class P, 16 words, sent 24/5 12.40 pm. To **Linwailuk Tokio**.

```
gedunufupa livuzisuto xegebuqade vayehaxube yofi[x]elopa xavuzinuxo xunufu[l]umu ceyofipali
vevotububu bigejipiyo go[g]uhefore repixasufa lejovoyogu lufiyopize
```
Key: rot12 euioa. **z = 6.5**.

Decode:
> 學生事暫擱，卽歸妥商。本部各人暫留東，清理部事。匯文款，宜託頭山保証，收後轉滬，至要。

"Shelve the students affair; return at once to discuss it. HQ staff stay in Tokyo (東) for now to wind up party business. For the remittance of Wen's (Sun's) money, it is best to ask Tōyama to guarantee it; once received, forward it to Shanghai. Most important."

This is the telegram that T13 answers ("now you say shelve it").

## T17: frame 29
Received at Tokio 3.45 pm 24/5/1916, from **Shanghai** No. 064, class P, 11 words, sent 24/5 12.40 pm. To **Linwailuk Tokio**. Signed in clear **"Junzaburo"**.

```
hoyotedase pubopavevo xunu[x]elobu bidoceyoda nuxopaqevu zayofisoke depe[q]iyido gavevogulu  Junzaburo
```
Key: rot12 euioa. **z = 5.3**.

Decode:
> [駒?]劉兆銘匯東各款，除酌留一月部費外，盡電匯滬。—Junzaburo

"[?] Of the various sums Liu Zhaoming remitted to Tokyo, apart from a month's HQ expenses to be kept back, wire all of it to Shanghai."
