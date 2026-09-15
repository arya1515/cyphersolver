"""The five Koehler cryptograms (Kahn, Cryptologia 5(2), April 1981), text as corrected against the Cryptologia
printing (Norbert's corrections, Schmeh 2017 comment #7; Schmeh's 2021 repost)."""
MSGS = {
 237: """ybtat mqfvo dvbis prito kecqg kokik kyiwm zuarj alyia qtxvi vxzya szgou skiqn rbqjq mogex ezdnf
 vusda zurop ixklo cmnbl grdhz swmch kupef pzlej hbord wkkhu vthjk sfwda jepmu izvig kzlau rdrxx
 mdecs spozv eeeod dlmdz nqmia pidwg xdcyy mvkso hmmii impwq nkipa mljvm sqsbb glevn sktlq tn""",
 178: """eekao parwo xiavy pejux lhnjh pbqdd vdvxb mdiia gwwmn zbivm abuws dwoug djozl ylaug loaea ilihj
 swjft oetad tjisn avaqn sodwb wzaxe zvoxg xpgzv adurm shvxx xfmuq pdpvq dqwtu fryok xfvcp ydzwm
 ofwfl uzfne qsslo evl""",
 137: """tziqb lqqxs kinod mbvil sukms syarh mhzvp tvswm ayddq rixyy omfzm ugfzz aznqe ljuyi ygwuo qmdbi
 vcxgz rmzno pessh gpoyx qqlei xmaoj buugz czfdl yzmkp gsmfm dteze oxmos""",
 140: """dmxkb kqnvh zzeek beoop ygcca yvepv tykmt iykfl zkacv uxiyd kruwy vnjvp xyeqp jpmfo abzpt mjtdy
 zvzky bjgze vdtyd zeejw zumjp ivsna gsmzq dltxb qjqqj fnpta mqted skijj""",
 229: """fpoxa tijyp qrerq znqst zasnk zarvq hhsmw vlhfg pyhqc yuirf fsgoi twgdg sbphc fkfza bpegh jzujn
 wtsxp ijamg tzdto hxzdn uivww tizoc axkye lhmdn sfzjo omrhb zpith hklsf anvdr ynhqk syrgi ltxos
 wabom dzwlb byava sjomn qqszs adddu greao alhon lxzgi iwpnf uzgui jgmya ksqfw zsjl""",
}
CT = {k: ''.join(v.split()) for k, v in MSGS.items()}
