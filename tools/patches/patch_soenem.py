import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:70]);s=s.replace(a,b)
# estatística: desconta das contas de Física os simulados de questões rápidas que aparecem no histórico
i=s.find("function statsDe(st){st=enemTotal(st||{});")
assert i>0
j=s.find(" return{R,n:st.n||0",i)
assert j>0
s=s[:j]+" {let rq=0,ra=0,rn=0;for(const h of (st.hist||[]))if(h&&h.src==='rap'&&(!h.mat||h.mat==='fis')){rq+=h.n||0;ra+=h.ac||0;rn++}\n  const F=R.fis;if(rq&&F.q){const fq=Math.max(0,1-rq/F.q),fa=F.ac?Math.max(0,1-ra/F.ac):0;for(const k in F.tp){F.tp[k]=[Math.round(F.tp[k][0]*fa),Math.round(F.tp[k][1]*fq)]}F.q=Math.max(0,F.q-rq);F.ac=Math.max(0,Math.min(F.q,F.ac-ra))}}\n"+s[j:]
# daqui pra frente: só simulados do ENEM entram nas estatísticas
rep(" const ar={};for(const q of qs){const a=qArea(q);ar[a]=ar[a]||[0,0];ar[a][1]++;if(isOk(q))ar[a][0]++}",
    " const ar={},soEnem=ES.src==='enem';if(soEnem)for(const q of qs){const a=qArea(q);ar[a]=ar[a]||[0,0];ar[a][1]++;if(isOk(q))ar[a][0]++}")
rep(" {if(!st.mt){st.mt={};st.mt0=st.n}const G={};"," if(soEnem){if(!st.mt){st.mt={};st.mt0=st.n}const G={};")
open(f,'w',encoding='utf-8').write(s);print('soenem ok',f)
