import sys,json
from PIL import Image,ImageDraw
Q='/home/claude/fisica-quest/q/'
bank=sys.argv[1];out=sys.argv[2];ids=sys.argv[3:]
B={q['id']:q for q in json.load(open(Q+bank+'.json'))}
tiles=[]
for i in ids:
    q=B[i];im=Image.open(Q+'orig/'+q['orig']).convert('RGB')
    lab=Image.new('RGB',(im.width,24),'#222');ImageDraw.Draw(lab).text((4,5),f"{i}  GAB={q.get('gab')}",fill='#ff0')
    t=Image.new('RGB',(im.width,im.height+24),'white');t.paste(lab,(0,0));t.paste(im,(0,24));tiles.append(t)
cols=[[]];h=0
for t in tiles:
    if h+t.height>1800 and cols[-1]:cols.append([]);h=0
    cols[-1].append(t);h+=t.height
W=sum(max(t.width for t in c) for c in cols)+10*len(cols);H=max(sum(t.height for t in c) for c in cols)
cv=Image.new('RGB',(W,H),'#888');x=0
for c in cols:
    y=0
    for t in c:cv.paste(t,(x,y));y+=t.height
    x+=max(t.width for t in c)+10
cv.save(out);print(cv.size)
