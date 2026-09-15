# Hyde-Barwick cipher (THE=370), transcribed from the plate "Tabula Cryptographica" (No. VIII)
# facing p.316 of Vita Johannis Barwick (1721). archive.org bim_eighteenth-century_vita-johannis-barwick-s_barwick-peter_1721 leaves n386/n387.
LETTERS = {}
for codes, let in [((1,2,3),'a'),((4,5,6),'b'),((7,8,9),'c'),((10,11,12),'d'),((13,14,15),'e'),((16,17,18),'f'),
                   ((19,20,21),'g'),((22,23,24),'h'),((25,26,27),'i'),((28,29),'k'),((30,31,32),'l'),((33,34,35),'m'),
                   ((36,37,38),'n'),((39,40,41),'o'),((42,43,44),'p'),((45,46,47),'q'),((48,49,50),'r'),((51,52,53),'s'),
                   ((54,55,56),'t'),((57,58,59),'v'),((60,61),'w'),((62,63),'y')]:
    for c in codes: LETTERS[c]=let
WORDS = """70 ab|71 ad|72 ac|73 by|74 ba|75 be|76 ca|77 ce|78 ci|79 da|80 de|81 di|82 em|83 en|84 es|85 fa|86 fe|87 fi|88 ga|89 ge|90 gi|91 ha|92 he|93 hi|94 I|95 ja|96 je|97 ka|98 ke|99 la|100 le|101 li|102 ma|103 me|104 mi|105 na|106 ne|107 ni|108 ob|109 ol|110 oc|111 pa|112 pe|113 pi|114 qu|115 qua|116 ra|117 re|118 ri|119 sa|120 se|121 si|122 ta|123 te|124 ti|125 va|126 ve|127 wa|128 we|130 you|131 your
132 af|133 ar|134 ap|136 bi|137 bo|138 bu|139 co|140 cu|141 cr|142 du|143 do|144 dr|145 el|146 ex|147 er|148 fo|149 fu|150 fr|151 go|152 gu|153 gr|154 ho|155 his|156 had|157 ju|158 jo|159 ir|160 ki|161 ko|162 lo|163 lu|164 ly|165 mo|166 mu|167 my|168 no|169 nu|170 nt|171 of|172 or|173 os|174 po|175 pu|176 pr|177 que|178 qui|179 ro|180 ru|181 rs|182 so|183 sh|184 st|185 to|186 te|187 th|188 vi|189 vo|190 wi|191 wo|192 yet|193 young
194 all|195 as|196 at|197 bl|198 br|199 but|200 ch|201 cl|202 ct|203 dis|204 den|205 Dr|206 ed|207 est|208 ence|209 fl|210 for|211 from|212 gh|213 gl|214 get|215 have|216 here|217 him|218 is|219 it|220 in|221 kn|222 kind|223 life|224 let|225 live|226 must|227 most|228 much|229 not|230 nor|231 now|232 op|233 om|234 on|235 ph|236 pl|237 plo|238 quo|239 quick|240 ry|241 ris|242 run|243 Sr|244 sh|245 sen|246 ty|247 tra|248 tre|249 ur|250 us|251 wh|252 with|253 yield|254 yeare
255 and|256 am|257 are|258 bly|259 both|260 been|261 can|262 con|263 com|264 did|265 doth|266 done|267 ent|268 eve|269 end|270 fix|271 fit|272 fill|273 gon|274 good|275 give|276 hath|277 how|278 hold|279 im|280 ill|281 in|282 keep|283 know|284 long|285 less|286 like|287 more|288 move|289 man|290 new|291 need|292 name|293 ow|294 our|295 out|296 pra|297 pre|298 pri|299 quiet|300 quantity|301 quarter|302 rule|303 raise|304 rest|305 say|306 shall|307 sea|308 tri|309 tro|310 tru|311 up|312 un|313 um|314 which|315 where|316 York Du.|317 Yarmouth
318 an|319 act|320 age|321 best|322 better|323 believe|324 care|325 case|326 court|327 day|328 der|329 dra|330 Earl|331 enter|332 except|333 full|334 fall|335 few|336 great|337 grant|338 gain|339 hear|340 help|341 hope|342 ing|343 joy|344 ion|345 knew|346 knowledge|347 loose|348 leave|349 least|350 mean|351 might|352 men|353 neer|354 ness|355 North|356 old|357 over|358 offer|359 pro|360 put|361 part|362 quarrel|363 quality|364 right|365 resist|366 rite|367 such|368 fame|369 some|370 the|371 this|372 that|373 use|374 upon|375 unto|376 went|377 want|378 York|379 Yaughall
380 arm|381 art|382 assist|383 between|384 besiege|385 business|386 cause|387 could|388 ceive|389 dre|390 desire|391 Duke|392 expect|393 express|394 exceed|395 free|396 friend|397 first|398 gard|399 govern|400 grace|401 horse|402 house|403 high|404 just|405 judge|406 interest|407 King|408 King|409 learn|410 little|411 letter|412 may|413 make|414 made|415 nigh|416 navy|417 next|418 office|419 order|420 obey|421 passe|422 place|423 please|424 question|425 Quaker|426 receive|427 rebel|428 resolve|429 summ|430 ship|431 state|432 them|433 they|434 then|435 under|436 very|437 were|438 would|439 Yelverton Sir H.|440 X
441 any|442 able|443 advise|444 break|445 betray|446 breach|447 count|448 charge|449 chief|450 design|451 defend|452 destroy|453 excel|454 enemy|455 endeavour|456 fear|457 fight|458 find|459 general|460 garrison|461 gentle|462 hence|463 hap|464 honest|465 inform|466 instruct|467 Independant|468 King|469 King|470 Lord|471 Lady|472 Land|473 matter|474 Month|475 Master|476 Nation|477 negotiate|478 Norwich|479 ought|480 opportunity|481 occasion|482 peace|483 pound|484 press|485 Queen|486 Queen|487 Queen|488 Reason|489 Religion|490 return|491 self|492 should|493 serve|494 there|495 take|496 time|497 van|498 ven|499 who|500 when|501 X|502 X|503 X
504 abou|505 affair|506 answer|507 Bishop|508 Bruxelles|509 Bucks Duke|510 choole|511 crown|512 concern|513 Dover|514 Dartmouth|516 example|517 examine|518 enterprize|519 tail|520 foot|521 force|522 Gerard Lord|523 Germany|524 Glocester|525 honour|526 hither|527 hundred|528 Intelligence|529 jealous|530 Isle|531 Kingdom|532 Kent|533 League|534 look|535 lost|536 Mr.|537 Message|538 Majesty|539 Newcastle|540 Norfolk|541 Northumberland|542 Overture|543 Opinion|544 Overton Coll.|545 People|546 Power|547 Promise|551 restore|552 relieve|553 Resolution|554 Service|555 Supply|556 Success|557 their|558 treat|559 trouble|560 ver|561 violent|562 what|563 whether|564 Z|565 Z|566 Z
567 acquaint|568 Army|569 Ambassador|570 Bristol|571 Berkley Lord|572 Barwick|573 Council|574 correspond|575 Cromwell R.|576 Desborow|579 England|580 English|581 Essex|582 Fleet|583 France|584 French|585 Glocester Duke|586 Goff Major General|587 Greenvill Sir John|588 Hull|589 Hyde Lord Chancellor|590 Harrison Major General|591 Ireland|592 Irish|593 Jermin Lord|594 Knight Col.|596 Leveller|597 Lambert|598 Ludlow|599 Marquis|600 Monke Lieutenant Gen.|601 Mazarine Cardinal|602 Northampton|603 Nicholas Mr. Secretary|605 Ormond Lord Lieutenant|606 Oxford|607 Ostend|608 Parliament|609 Presbyter|610 Prince|614 Regiment|615 Rendezvouz|617 Scotland|618 Spain|619 Southampton|620 tempt|621 through|622 though|623 Victory|624 victual|625 write|626 winter|627 Zeal|628 Zealand
632 Bradshaw|633 Baxter Lieut. of the Tower|635 Cromwell H.|636 Clobery Coll.|637 Clarges Dr|638 Cholmeley Sir H.|639 Cholmeley Mr.|644 Fleetwood|645 Fairfax Lord|646 Fiennes Mr. Nath|650 Hartford Marq.|651 Haslerig Sir Arthur|653 Inchequin Lord|658 Lockhart|659 Lenthall Speaker|660 Lisle Lord|661 Massy Major General|662 Mountagu Admiral|663 Moyer Mr.|664 Middleton Sir Tho.|665 Mordant Lord|667 Otway Mr.|670 Portsmouth|671 Plimouth|676 Republick|677 Rombald Mr.|678 Redman Coll.|679 Saloway Major|680 St. John|682 Tinmouth|683 Tichburne|684 Thurloe|685 Vane Sir Hen.|686 Venables Coll.|688 Wales"""
KEY = dict(LETTERS)
for line in WORDS.split('\n'):
    for ent in line.split('|'):
        ent=ent.strip()
        if not ent: continue
        n, w = ent.split(' ',1); KEY[int(n)] = w
MAX = 692

SUPERSCRIPTIONS = {
 '1659-09-29 (No.XVI p.358)': [212,23,12,7,461,36,108,49,498,14,21,410],
 '1659-10-17 (No.XVII p.360)': [729,549,705,99,856,250,245,831,100,859,609,858,101,24],
 '1660-01-14 (No.XXIII p.389)': [729,549,856,21,245,831,99],
 '1660-01-16 (No.XXVI p.396)': [729,549,856,8,245,831],
}
if __name__ == '__main__':
    print('key entries:', len(KEY), 'max code', MAX)
    for name, nums in SUPERSCRIPTIONS.items():
        out=[]
        for n in nums:
            out.append('%d=%s' % (n, KEY.get(n, '??' if n<=MAX else '>692')))
        print(name); print('   ', ' '.join(out))
    # sanity: known plaintext from the letters? print a few
    for w in ['for','the','Mr.','Barwick','these','London','Sir','Dr']:
        print(w, [k for k,v in KEY.items() if v.lower()==w.lower()])
