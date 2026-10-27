import sys,json
from PIL import Image,ImageDraw
Q='/home/claude/fisica-quest/q/'
B={q['id']:q for q in json.load(open(Q+'questoes.json'))}
out=sys.argv[1];ids=sys.argv[2:]
tiles=[]
for i in ids:
    q=B[i];fs=[]
    if q.get('modo')=='img':fs=[Q+'orig/'+q['orig']]
    else:
        fs=[Q+'img/'+p['img'] for p in q['parts'] if p.get('img')]
        for a in q['alts']:
            for im in a.get('imgs') or []:fs.append(Q+'img/'+im['img'])
    for f in fs:
        im=Image.open(f).convert('RGB')
        if im.width>900: im=im.resize((900,int(im.height*900/im.width)))
        lab=Image.new('RGB',(im.width,22),'#222');ImageDraw.Draw(lab).text((4,4),i+' '+f.split('/')[-1],fill='#ff0')
        t=Image.new('RGB',(im.width,im.height+22),'white');t.paste(lab,(0,0));t.paste(im,(0,22));tiles.append(t)
# empacota em colunas de até 1400 px de altura
cols=[[]];h=0
for t in tiles:
    if h+t.height>1400 and cols[-1]:cols.append([]);h=0
    cols[-1].append(t);h+=t.height
W=sum(max(t.width for t in c) for c in cols)+10*len(cols);H=max(sum(t.height for t in c) for c in cols)
cv=Image.new('RGB',(W,H),'#888');x=0
for c in cols:
    y=0
    for t in c:cv.paste(t,(x,y));y+=t.height
    x+=max(t.width for t in c)+10
cv.save(out);print(cv.size)
