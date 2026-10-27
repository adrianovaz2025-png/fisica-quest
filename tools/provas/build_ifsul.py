import json,re,shutil,unicodedata
Q='/home/claude/fisica-quest/q/'
G={2025:'BDAADCCDBCBBCADCADDNBBBCNNCCDADCBADCDCBBCADBACDABA',2026:'CBADCACBDADBCBCADADABCBDACBDCDBCBCBBAACADADCAABADD'}
src=open('/home/claude/work/tema/cls.py',encoding='utf-8').read().split('FN={')[0];ns={};exec(src,ns);R=ns['R']
def norm(s):return unicodedata.normalize('NFD',s.lower()).encode('ascii','ignore').decode()
out={'linguagens':[],'matematica':[]}
for ano,gab in G.items():
    assert len(gab)==50
    for r in json.load(open(f'out/rel_{ano}_1.json')):
        n=r['num'];g=gab[n-1]
        if n<=25: fn,tema,area='linguagens','POR','LIN'
        else:
            t=norm(r['txt']);sc=sorted(((len(re.findall(rx,t)),c) for c,_,rx in R['mat'][:-1]),reverse=True)
            fn,tema,area='matematica',(sc[0][1] if sc[0][0]>0 else 'ARI'),'MAT'
        q=dict(id=r['id'],ano=ano,num=n,dia=1,banca='ifsul',area=area,lg='',parts=[],alts=[{'l':l,'h':''} for l in 'ABCD'],orig=r['id']+'.webp',osz=r['osz'],modo='img',gab=None if g=='N' else g,gsrc='oficial',tema=tema)
        if g=='N':q['anulada']=True
        out[fn].append(q);shutil.copy(f"out/{r['id']}.webp",Q+'orig/'+r['id']+'.webp')
for fn,add in out.items():
    raw=open(Q+fn+'.json',encoding='utf-8').read();a=json.loads(raw)
    a=[x for x in a if x.get('banca')!='ifsul']+add
    compact='": ' not in raw[:800]
    open(Q+fn+'.json','w',encoding='utf-8').write(json.dumps(a,ensure_ascii=False,separators=(',',':')) if compact else json.dumps(a,ensure_ascii=False))
    print(fn,len(add),sum(1 for x in add if x.get('anulada')))
