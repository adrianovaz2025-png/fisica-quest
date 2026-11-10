"""Adiciona IF Sul de Minas 2020, 2023 e 2024 (recortes em out/ e out2/). Rode da raiz do repo."""
import json,re,shutil,unicodedata,sys
Q='q/'
G={}
for r in open('/mnt/user-data/uploads/provas/gabaritos.txt',encoding='utf-8'):
    p=r.strip().split(';')
    if len(p)>=5 and p[0].lower().startswith('if') and p[1] in('2020','2023','2024'):G.setdefault(int(p[1]),{})[int(p[3])]=p[4]
src=open('/home/claude/work/tema/cls.py',encoding='utf-8').read().split('FN={')[0];ns={};exec(src,ns);R=ns['R']
def norm(s):return unicodedata.normalize('NFD',s.lower()).encode('ascii','ignore').decode()
# onde está cada faixa de questões: (arquivo, area, tema fixo ou None)
def dest(ano,n,txt):
    if ano==2020:
        if n<=15:return 'linguagens','LIN','POR'
        if n<=30:return 'matematica','MAT',None
        if n<=38:return ('quimica','QUI','GER') if n==37 else ('biologia','BIO','GER')
        return 'humanas','HUM','GEO' if n<=44 else 'HIS'
    return ('linguagens','LIN','POR') if n<=25 else ('matematica','MAT',None)
out={k:[] for k in['linguagens','matematica','biologia','quimica','humanas']}
for ano,dr in((2020,'out'),(2023,'out2'),(2024,'out2')):
    for r in json.load(open(f'{dr}/rel_{ano}_1.json')):
        n=r['num'];g=G[ano][n];fn,area,tema=dest(ano,n,r['txt'])
        if fn=='matematica':
            t=norm(r['txt']);sc=sorted(((len(re.findall(rx,t)),c) for c,_,rx in R['mat'][:-1]),reverse=True);tema=sc[0][1] if sc[0][0]>0 else 'ARI'
        anul=g.upper().startswith('ANUL')
        q=dict(id=r['id'],ano=ano,num=n,dia=1,banca='ifsul',area=area,lg='',parts=[],alts=[{'l':l,'h':''} for l in 'ABCD'],orig=r['id']+'.webp',osz=r['osz'],modo='img',gab=None if anul else g[0],gsrc='oficial',tema=tema)
        if anul:q['anulada']=True
        out[fn].append(q);shutil.copy(f"{dr}/{r['id']}.webp",Q+'orig/'+r['id']+'.webp')
for fn,add in out.items():
    if not add:continue
    raw=open(Q+fn+'.json',encoding='utf-8').read();a=json.loads(raw)
    ids={q['id'] for q in add};a=[x for x in a if x['id'] not in ids]+add
    compact='": ' not in raw[:800]
    open(Q+fn+'.json','w',encoding='utf-8').write(json.dumps(a,ensure_ascii=False,separators=(',',':')) if compact else json.dumps(a,ensure_ascii=False))
    print(fn,len(add),'anuladas',sum(1 for x in add if x.get('anulada')))
