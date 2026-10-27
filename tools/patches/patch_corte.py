import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:70]);s=s.replace(a,b)
CORTE=r'''const ESTAT_DESDE='2026-10-22',ESTAT_EP=Date.parse(ESTAT_DESDE+'T00:00:00-03:00'),M2AREA={mat:'MAT',qui:'QUI',bio:'BIO',lin:'LIN',hum:'HUM',fis:'FIS'};
/* estatísticas contam só a partir de ESTAT_DESDE: o que veio antes fica guardado em "arq", fora das contas */
function enemCorte(st){st=st||{};if(st.ep===ESTAT_EP)return st;const h=(st.hist||[]).filter(x=>x&&x.d>=ESTAT_DESDE),N={n:h.length,best:0,hist:h,areas:{},mt:{},ep:ESTAT_EP,arq:{n:st.n||0,best:st.best||0,areas:st.areas||{},mt:st.mt||{},ate:ESTAT_DESDE}};
 for(const x of h){if(!x.parc&&x.n)N.best=Math.max(N.best,Math.round(x.ac/x.n*100));const m=x.mat;if(!M2AREA[m])continue;const k=M2AREA[m];N.areas[k]=N.areas[k]||[0,0];N.areas[k][0]+=x.ac||0;N.areas[k][1]+=x.n||0;const M=N.mt[m]=N.mt[m]||{n:0,q:0,ac:0,tp:{}};M.n++;M.q+=x.n||0;M.ac+=x.ac||0}
 N.mt0=0;return N}
'''
rep("/* junta o histórico antigo (só totais) com o novo (matéria + tópico) */\nfunction statsDe(st){st=st||{};",
    "/* junta o histórico antigo (só totais) com o novo (matéria + tópico) */\n"+CORTE+"function statsDe(st){st=enemCorte(st||{});")
rep("function enemState(){const e=eqState();if(!e.enem)e.enem={n:0,best:0,hist:[],areas:{}};return e.enem}",
    "function enemState(){const e=eqState();if(!e.enem)e.enem={n:0,best:0,hist:[],areas:{},ep:ESTAT_EP};if(e.enem.ep!==ESTAT_EP){e.enem=enemCorte(e.enem);saveEq()}return e.enem}")
# tópico genérico para física reconstruída do histórico
import re
i=s.find("const TEMAS={");j=s.find('"fis": {',i)
assert j>0 and j-i<3000
s=s[:j]+'"fis": {"FIS": "Física (sem tópico registrado)", '+s[j+len('"fis": {'):]
open(f,'w',encoding='utf-8').write(s);print('corte ok',f)
