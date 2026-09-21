"""Synthetic French positive control; NOT plaintext of the Egmond cipher."""
import pathlib,random,json,subprocess,sys
root=pathlib.Path(__file__).resolve().parent
plain=('monsieurmonboncousinieVouspriedeVouloircontinuerauBienetaduancement'
       'demesaffairesetdonnerVotrebonnefaueuretassistanceauporteurdeceslettres'
       'afinquilpuisseauoirbonneetbriefueexpedition').lower().replace('v','u')
alpha='abcdefghiklmnopqrstuvxyz'
labels=list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'[:len(alpha)])
random.Random(20260920).shuffle(labels)
enc=dict(zip(alpha,labels))
ct=''.join(enc[c] for c in plain)
(root/'synthetic_control.txt').write_text(ct)
(root/'synthetic_control_truth.json').write_text(json.dumps({'plaintext':plain,'encryption':enc,'caution':'Constructed positive control; not an Egmond decipherment.'},indent=2))
subprocess.run([sys.executable,str(root/'probe.py'),'separate','synthetic_control.txt'],check=True)
r=json.loads((root/'probe_result_synthetic_control_separate.json').read_text())
accuracy=sum(x==y for x,y in zip(r['reading'],plain))/len(plain)
print('Positive control letter accuracy:',accuracy)
(root/'synthetic_control_validation.json').write_text(json.dumps({'letters':len(plain),'letter_accuracy':accuracy,'exact_match':r['reading']==plain},indent=2))
