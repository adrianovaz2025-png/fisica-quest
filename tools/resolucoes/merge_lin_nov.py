import json,sys,re
sys.path.insert(0,'/tmp/w')
R={}
from b1 import R as a; R.update(a)
from b2 import R2020 as b; R.update(b)
from b3 import R2021 as c; R.update(c)
from b4 import R26 as d; R.update(d)
from b5 import RX as e; R.update(e)
try:
    from b6 import R25 as g; R.update(g)
except ImportError: pass
bank={}
for f in ['linguagens']:
    for q in json.load(open(f'q/{f}.json')): bank[q['id']]=q
res=json.load(open('q/res/lin.json'))
add=0
for k,v in R.items():
    assert k in bank,k
    assert bank[k].get('gab'),(k,'anulada')
    assert v.count('<b>')==v.count('</b>')>=1,k
    assert k not in res or not res[k].get('t'),(k,'já existe')
    res[k]={'t':v,'aula':''};add+=1
open('q/res/lin.json','w',encoding='utf-8').write(json.dumps(res,ensure_ascii=False,separators=(',',':')))
print('adicionadas',add,'total',len(res))
