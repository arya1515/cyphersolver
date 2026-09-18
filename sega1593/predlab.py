# CNN predictions -> label file for montage_lab and class strings. usage: predlab.py model prefix k0 k1 out_prefix
import json, sys, numpy as np, torch, cnn
model, pre, k0, k1, outp = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
net = cnn.Net(); net.load_state_dict(torch.load(model)); boxes = json.load(open(f'{pre}_g2.json'))
pred = {}; probs = {}; strings = {}
for k in range(k0, k1 + 1):
    bx = boxes[str(k)]
    p = cnn.predict(net, cnn.crops_for(pre, k, bx)); probs[str(k)] = p.tolist()
    s = []
    for j, (b, pj) in enumerate(zip(bx, p)):
        top = int(pj.argmax()); name = cnn.CLASSES[top]
        if b[4] < 130: name = '.'
        elif pj[top] < 0.5: name = name + '?'
        pred[f'{k}:{j}'] = name; s.append(name)
    strings[str(k)] = ' '.join(s)
json.dump({'pred': pred}, open(outp + '_pred.json', 'w'))
json.dump(probs, open(outp + '_probs.json', 'w'))
with open(outp + '_strings.txt', 'w') as f:
    for k in range(k0, k1 + 1): f.write(f'L{k}: {strings[str(k)]}\n')
print('wrote', outp)
