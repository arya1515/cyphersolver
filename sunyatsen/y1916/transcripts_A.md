# JACAR B03050088300: transcripts, batch A

Frames 088300_04, 05, 18–27 (JACAR frames 445, 446, 459–468). Keys are given as famtest names or as
`rotN/revN : vowel order : fill : offset`, which `family.py` / `famtest.table()` can use directly.
"z" is famtest's z-score for the transcription as read. "robust z" comes from a variant that caps each
code's log-probability at −12, so a few misread codes do not sink a true key. Corrections are single
letters, suggested by the decode and checked against the image where possible. `[?]` marks a code
still unexplained.

Keys found in this batch:

| Circuit | Key | Evidence |
|---|---|---|
| Tokyo ↔ Manila (Konglipo) | manila1916 = rot4 oeuai vow off1 | z 4.7–5.9 on four telegrams |
| Shanghai → Tokyo (Rosamonde), Tokyo → Junzaburo Shanghai | shanghai1916 = rev0 ioaeu vow off1 | z 4.9–9.2 |
| **Seitō (Tsingtao) → Tokyo** | **rot9 uieoa vow off1** (new) | z 7.1, robust z 11.0 on No. 56. rot8 uieoa vow off0 is almost the same table and nearly as good. |
| **Honolulu → Tokyo** | **rev10 eaoui cons off0** (new, tentative) | z 4.9, robust z 6.5. Reads 議和萬勿以□代袁. |

Clerk confusions seen repeatedly: g↔q, and x written like d or s (d→x, s→x, z→x) on the
Shanghai forms. The two Seitō telegrams both give `mezo` = 4171 盻 before 覆, where 盼 is 4162 = `meno`.
So 盼覆 ("hoping for your reply") was probably meant, with the same n→z slip each time.

---

## Frame 04 (JACAR 445), upper form: Sun → Manila
- Forwarded. Original office Tokio, class P, No. 07425, 10 words, date 27/3 1916, time 11.50 am, sent 6.35 pm. Remarks: via Sh[anghai], Comm. Address **Konglipo Manila**. Signature 中山.
- Cipher: `tudasaviku parakusoke saxigegugu vumuvilola medelanave befibogavu lananonoco belebikege`
- Key **manila1916**, z 5.0 as read.
- Corrections: `saxigegugu` → `saxiqequga`. The image shows q-like loops, so qequ 款, and ga|vu = 請 (u/a). `belebikege` → `…keqe` (文).
- Decode: **舅電稱閩[夠?]需款，請籌匯東，轉滬；並請轉告怡朗。文**
  ("Uncle wires that Fujian [?] needs funds. Please raise them and remit to Tokyo, to be passed on to Shanghai. Please also inform Iloilo. — Wen")
  Code 4 `soke` = 1124 夠 is unexplained.

## Frame 04, lower form: clear text
- Forwarded, Tokio, No. 07525, 12 words, 27/3 1916, 11.50 am, sent 6.30 pm. To Ozawayoshitaro, Taiyokan, Japanese Concession, Tientsin. Signed 林 (with Japanese notes 孫逸仙…).
- Text: "Return with your friend settle mother here".

## Frame 05 (JACAR 446): Sun → Junzaburo Shanghai
- Forwarded, Tokio, class P, No. 07825, 12 words, 28/3 1916, 5 pm, sent 5.20 pm. Address **Junzaburo Shanghai**. Signature 中山.
- Cipher: `papamezuvi kodagopoje lojitixomo foxigatibu vogakopozi ninozehayi xigakofofi c?fihovise paparonala zenoguvopo`
- Key **shanghai1916**, z 4.9.
- Correction: w1 is probably `popamezuvi`, giving popa 款 rather than papa 繼. The capital P/o is ambiguous.
- Decode: **款難分[螮?]。此時務注全力於滇，以求萬全。滬[彐彊?]刻繼械自[沗?]。文**
  ("Funds are hard to divide. Now all effort must go to Yunnan, to make it secure. Shanghai … arms … — Wen")
  Codes 3 (`dago`), 17–18 (`fico fiho`) and 23 (`nogu`) are unexplained. w8's second letter is an unclear loop.

## Frame 18 (JACAR 459), upper form: Honolulu → Rosamonde Tokyo
- Received Tokio 8 am 28/3 1916. Paper 23, class P, original office **Honolulu**, No. 53, 10 words.
- Text: `Aloha` (clear, or a code-name), then `xofalodeye molecumake tikomaluyi kuvukodibe musafateme rahofibaji hurunozo`. The last word has 8 letters, perhaps `huru?ozo`.
- Key **rev10 eaoui cons off0**, new and tentative: z 4.9, robust z 6.5. None of the known keys reads it.
- Decode: **議和萬勿以[黎?]代袁，[?]由[?][?][?]接管[?][?]**
  ("In the peace talks on no account let [Li Yuanhong] replace Yuan; … must take over …")
  - `tiko` = 7412 餛. 黎 would be `suko`, so t→s is a guess.
  - Codes 8, 10–12 and 15–16 are unexplained. `vuko` may be `tuko` 須.

## Frames 18–19 (JACAR 459–460): Seitō No. 71 → Rosamonde Tokio
- Received 1.26 am 28-3-1916. Papers 21–22, class M, original office **Seitō** (Tsingtao), No. 71, 12 words, dated 28-3 1916, 9.40 pm.
- Cipher: `huhacukepu hegocamezo leyuxidoyo fizoqekiji kivijujilu husopepefe nesetubuxi xiquzejumu | musuzocaru rodicoruni`
- Key **rot9 uieoa vow off1** (Seitō key): z 4.1 raw, robust z 6.0. rot8 uieoa off0 gives robust z 6.3 but differs by one code.
- Corrections:
  - `hegocamezo` → `hezoca…`: zoca 電 (g/z).
  - `kivijuyilu` → `kivijujilu`: juji 急.
  - `mezo` is read as 盼 (see note above).
  - `musu` → `muyu` 以.
  - `dico` → `xico` 正 (d→x).
- Decode: **[徼宥?]兩電盼覆。此間[需?]用甚急，懇速示[砬呂櫟?]；到必以電匯。正[勘?]**
  ("…two telegrams; awaiting your reply. Our needs here are very urgent. Please instruct us quickly … on arrival we will certainly remit by wire. — Zheng [?]")
  - Codes 0–1, 8 (`zoqe` 7144; 需 is `zoda`), 15–17 and 24 are uncertain.
  - `nese tubu xixi` could be 知 將 款 (s→x, t→d, i→e).
  - The signature 正 is probably 居正 (Ju Zheng), whose Northeast Army was based at Tsingtao.

## Frames 19–20 (JACAR 460–461): Shanghai No. 0129 → Rosamonde Tokio
- Received 9.35 pm 27-3-1916. Papers 19–20, class P, Shanghai, No. 0129, 30 words, 27/3 1916, 6.21 pm.
- Cipher (read left column, then right, row by row):
  `nogemozuko fotohataje bucakavome notaxupopa conesigeso qurelukova hozajemica bomibiloge mejihayije mirecahayi jemixegaro napimexika xekepijoti dezamibuca hayijikifa nijivotopu | popavikoga yosijuhidu pokepibuba gazabameka bufakevomi nezekataco xoqobucati qakofosaku hayidigake luiifatoyi sozimikuma jebocutibi`
- Key **shanghai1916**, z 6.7 on paper 19 alone.
- Corrections:
  - noge → noqe 江.
  - `conesigeso` → `conesiqexo`, giving 可 and 支.
  - koga|yo → qayo 給.
  - `hayidigake` → `hayixigake` 全.
  - `luiifatoyi` → `lixifatoyi`: keli 須, xifa 兩 (the scrawled "ii" is "xi").
- Decode: **江浙滬暨第二艦隊等款略可支配[漆?]，無餘裕。外湘[陲?]萬餘，鄂萬餘，購械均[兣?]，贛四千，皖二萬。專處尚有款分給否？[席?]正[噶?]言直隸事頗好。請立撥二[匍?]滬，籌萬全，須兩星期始能發動。**
  ("Funds for Zhejiang, Jiangsu, Shanghai and the Second Fleet can roughly be managed, with nothing to spare. Also Hunan 10,000+, Hubei 10,000+, arms purchases …, Jiangxi 4,000, Anhui 20,000. Is there still money to allot? … says Zhili affairs go well. Please allot 2 … to Shanghai at once. Raising it safely will take two weeks before we can move.")
  Codes 14, 20, 29, 44, 46 and 57 are unexplained. There is no signature code.

## Frame 20 (JACAR 461), lower form: Manila No. 19 → Rosamonde Tokio
- Received 5.56 pm 27-3-1916. Paper 18, class P, Manila, No. 19, 15 words, date "nil". Remarks: Compac.
- Text: `Shuisoongi` (clear name), then `zexegahude cemegovoca jizogogave befedisavi gopefisave bobotadeku fiyayuhomo padetigoro boyagavude cedoyurozo demafinosa vijuzovusi`
- Key **manila1916**, z 5.8.
- Corrections: `jizo` → `juzo` 碼. `goga` → `qoga` 在 (g/q).
- Decode: **爲誰用期密碼在滬發電[休亠滃徉田亥?]萬可疑，以後請用[愴?]堂留下電碼。英**
  ("… using the codebook to send telegrams from Shanghai … highly suspicious. From now on please use … hall, leave the code … — Ying")
  Codes 0–3 are readable but awkward, and 10–15 and 23 are unexplained. 英 also signs frame 25.

## Frame 21 (JACAR 462), upper form: Sun → Manila
- Forwarded, Tokyo, class P, No. 07525(?), 6 words, 27/3, 9.35 pm. Remarks: Sh, Comm. Address **Konglipo Manila**. Signature 中山.
- Cipher: `vebesavifi yeyokoleyu fozafedilo jidelikeqe`
- Key **manila1916**, z 4.6 as read.
- Corrections: `leyu` → `leye` 智. `lo|ji…` → `loju` 勿 (the "ii" is "u"). `deli` → `deti` 疑.
- Decode: **滬電乃崇智所發，勿疑。文**
  ("The Shanghai telegram was sent by [Xu] Chongzhi. Do not doubt it. — Wen")

## Frame 21, lower form: clear text
- Forwarded, Tokyo, No. 22317, 8 words, 28/3 1916, 0.45 pm. To Ozawayoshitaro, Taiyokan, Japanese Concession, Tientsin. Signed 中山.
- Text: "2000 through Shokinginko" (Yokohama Specie Bank, 正金銀行).

## Frame 22 (JACAR 463), upper form: Shanghai No. 058 → Rosamonde Tokio
- Received 8.10 pm 26/3/1916. Paper 14, class P, Shanghai, No. 058, 11 words, 26-3-1916, 5.57 pm.
- Cipher: `rakugequca mohokijepe fijalocaxo kepumoyosa savixopilo homuvogavu savixopiho yalolajeye`. Signature in clear: **Shuichunchee** (許崇智 Xu Chongzhi).
- Key **manila1916**, z 4.4–4.7 as read.
- Corrections:
  - gequ → qequ 款.
  - `fijalocaxo` gives loca 千 (the letter I first read as b is l).
  - muvo → muvi 籌.
  - jeye → leye 智.
- Decode: **閩款[黃?]僅撥五千，尚絀。已電岷加籌；請電岷催匯。智**
  ("Of the Fujian funds, [Huang?] has allotted only 5,000; still short. I have wired Manila (岷) to raise more. Please wire Manila to hurry the remittance. — [Chong]zhi")

## Frames 22–23 (JACAR 463–464): Shanghai No. 070 → Rosamonde Tokio
- Received 11 pm 26-3-1916. Papers 15–17, class P, Shanghai, No. 070, 38 words, 26-3-1916, 8.52 pm.
- Cipher:
  - Paper 15: `mekudituzi lisifomeku vagepopaxo luzekapiki fanisexase xetemiqilu bufixahayo joxolubiru padasiyame kukopatopu pokefipidi zevopomohe xeluzihoxe vusocozini pigibufoxo gapodasiyi`
  - Paper 16: `barepabido nivimakofo zekazogafi pebufimeku pabidoniki hayecoseco tixapiyani kijihanigi bufoxidolo fodoxadori xiyaronita xubuzekofo fipemitusi kilafuleno sosivagevo becozujiva`
  - Paper 17: `xigotoyajo varonahime topuyojomo jesijunaci`
- Key **shanghai1916**, z 9.2.
- Corrections:
  - `jozolubiru` → `joxo…` 收.
  - `kukopatopu` → `kukopotopu`: kopo 滇.
  - `pokefipidi` → `…pixi`: xize 公 (d→x).
- Decode: **電悉。仲去電[穆]款收，請[嚥?]處速運軍器，並示接收手續。又電，滇有正式公文派趙伸赴東，以[嚳?]之[攙歕卯?]。託總理到滬，請招待；並電總理宜變通，勿固執。展堂之兄清瑞、現[光?]桂等云：滬待妥，即[舟?]青木。穆日當局允暗濟械，已有接洽否？美**
  ("Telegram received. … funds received. Please have … ship the munitions quickly and state the handover procedure. Also: Yunnan has an official letter sending Zhao Shen to Japan … Please receive … on arrival in Shanghai, and wire the Premier to be flexible and not obstinate. Hu Hanmin's brother Qingrui, … Gui and others say Shanghai is ready; then [see?] Aoki. The authorities have agreed to supply arms secretly. Has contact been made? — [Chen Qi]mei")
  - 穆 (`vage`) occurs twice with the same letters, so it is probably a name or cover word.
  - Codes 9, 35, 37–39 and 73 are unexplained.
  - Signature 美 = 陳其美 (Chen Qimei).

## Frame 24 (JACAR 465), upper form: Sun → Junzaburo Shanghai
- Forwarded, Tokio, class P, No. 07235, 16 words, 26/3 1916, 2.40 pm. Address **Junzaburo Shanghai**. Signature 中山.
- Cipher: `buceyirija cavigasege tahucakito qaseyozipe delizigiyi xipoyebipe qaribuhoyi jokamutibu figuviroxo cukofobufa cozubacuvo gacakiseyo bufovirebu hosigevopo`
- Key **shanghai1916**, z 5.7.
- Corrections: zigi → ziqi 代. bacu → bocu 發 (a/o). sige → siqe 可.
- Decode: **京信[矴刷遜?]策：袁暫退，使黎代；俟歐戰終，乃借英力[徹?]出。故滬事當發於袁退之前乃可。文**
  ("The Beijing letter … plan: Yuan steps down for now and Li [Yuanhong] acts in his place; after the European war ends, British power is used to push him out. So the Shanghai rising must be launched before Yuan withdraws. — Wen")
  Codes 2–4 are unexplained (`ya/ja ca`, `viga`, `sege`). Code 20 `figu` could be 從 or 復.

## Frame 24, lower form: Sun → Manila
- Forwarded, Tokio, class P, No. 07135, 8 words, 26/3 1916, noon. Remarks: Sh, Comm. Address **Konglipo Manila**. Signature 中山.
- Cipher: `hayemomufu rosagitabe fodomazujo megequrasi qetagegibu nelosukefo`
- Key **manila1916**, z 4.7.
- Correction: gequ → qequ 款.
- Decode: **譽反覆難靠，應[逼?][償?]款，阻止[挫蚓勾?]敵**
  (partial: "Yu is fickle and unreliable; the funds should …; stop … enemy")
  譽 also opens the Manila telegram No. 75 (frame 25), so it is probably a person's name. Codes 6–7 and 11–13 are unexplained.

## Frame 25 (JACAR 466), upper form: Manila No. 75 → Rozamonde Tokio
- Received 1 am 26-3-1916. Paper 13, class P, Manila, No. 75, 10 words, date nil. Remarks: Compac no.
- Cipher: `hayefigavo yigutilofi calefibume nokevozexe guzagofile hisavisoku ?otagoquma jiyujuvusi`. The first letter of w7 looks like "a" and is invalid; I used d.
- Key **manila1916**, z 5.9.
- Decode: **譽云：實着力黨事，未敢爲真。他曾電奉[慙?]何[遨蒲?]。英**
  (partial: "Yu says he is truly working hard on party affairs … he has wired … — Ying")

## Frame 25, lower form: clear text
- Manila No. 73, 15 words, received 0.15 am 26-3-1916, paper 12. Addressed Sunyatsen Tokio. Remarks: cpe no.
- Text: "Cable instruct local headquarter postpone 1200 suit against Tsyhaneng(?) myself fetter following Tomgun(?)".

## Frame 26 (JACAR 467): Seitō No. 56 → Rosamonde Tokio
- Received 0.37 pm 26/3/1916. Papers 10–11, class M, **Seitō**, No. 56, 20 words, 25/3 1916, 9.50 pm.
- Cipher: `zilehufaci norixayoqi huhohixodu mimubelavu suvobohisi kirudelehe mocenolaru pebelozecu deliqiyoso pekirezuzi dejilasiso hosopiseye bolirikobo yiduhacupe | nuzorozusu domusutobe nibamezole yusicohuho`
- Key **rot9 uieoa vow off1**: z 7.1, robust z 11.0.
- Corrections: `mimubefavu` → `…lavu` 不. `domusu` → `domuxu` 令.
- Decode: **津德漸有門徑。王少[佘?]不可靠。東北[訂→事?]請謝勿與聞。[荷旖?]速由天[莛锕?]遞送[篧?]面書。青島守備軍司令部[搵?]盼覆。[某→正?]徑**
  ("The Tianjin Germans are gradually becoming accessible. Wang Shao… is unreliable. On Northeast matters please [ask] Xie not to get involved. … send quickly via Tian[jin] … a personal letter. The Tsingtao garrison command … awaiting your reply. — Zheng?")
  - The signature `sico huho` becomes `xico` 正 with the usual s→x slip, followed by 徑.

## Frame 27 (JACAR 468): Shanghai No. 054 → Rosamonda Tokio
- Received 4.5 pm 25-3-1916. Papers 8–9, class P, Shanghai, No. 054, words "29/38", 25-3-1916, 12.42 pm.
- Cipher:
  - Paper 8: `hikuvihasi qamojujeda solitaxuco zukoyebajo todukofoco gemohetibu fisovozabi kaconesiqe fisukipezi yapacumopu temixozabo cutahuteto hayixigaho vafonodido yimesoribi diciyukofo`
  - Paper 9: `tibinepusa vafopezebe buhuzekake pufopesexa zitetoturi juzipusisa zazecuzuto jigojuzibe toqifiketi bioooooooo`. The last word is "bi" plus o-padding: its "bi" completes the final code.
- Key **shanghai1916**, z 6.7 as read.
- Corrections:
  - voza → voga 於.
  - fisu → fixu 從.
  - zite → zime 來.
  - cuzu → cozu 當.
  - goju → qoju 機.
- Decode: **帝制取消，馮、朱等當漸觀望。滬異派力弱，於我略可從容佈置。海軍[擂?]發策較萬全，然猶急備未懈。慮滬動，防[篚?]王謀，仍請飭王速來會商，便[反?]相當時機。[供?]是[徊?]動**
  ("The monarchy is cancelled. Feng [Guozhang], Zhu and the others will gradually wait and see. The opposing faction in Shanghai is weak, so we can deploy at some leisure. A plan launched by the Navy … is safer, but we are still preparing urgently without slackening. Fearing a move in Shanghai, guard against … Wang's plotting. Please still order Wang to come quickly for consultation, so as to … the right moment …")
  Codes 26, 42, 54 and 59–61 are unexplained. There is no signature.

---

### Non-condenser items
- Frame 04, lower form: English, Tokyo → Ozawa Yoshitaro, Tientsin: "Return with your friend settle mother here".
- Frame 21, lower form: English/romanised Japanese, Tokyo → Ozawa Yoshitaro, Tientsin: "2000 through Shokinginko".
- Frame 25, lower form: English, Manila → Sunyatsen Tokio: "Cable instruct local headquarter postpone 1200 suit against Tsyhaneng myself fetter following Tomgun".
- Clear words inside cipher telegrams:
  - "Aloha" (Honolulu, frame 18).
  - "Shuisoongi" (Manila No. 19, frame 20).
  - Signature "Shuichunchee" (Shanghai No. 058, frame 22).
  - "bioooooooo" filler (frame 27).
- Kana/kanji notes on the forms: 中山 on the forwarded forms, and the receipt notes 本居方…中山宛.
