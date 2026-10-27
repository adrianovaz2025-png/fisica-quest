import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:70]);s=s.replace(a,b)
i=s.find("const ESTAT_DESDE=");j=s.find("function statsDe(",i);assert 0<i<j
TOT=r'''/* estatística total (todo o histórico). Desfaz o corte de 22/10 para quem chegou a passar por ele:
   volta o arquivo e soma só o que veio depois do corte (questões com tópico); a parte refeita do histórico de hoje é descartada para não contar em dobro */
const AREA_DE={mat:'MAT',qui:'QUI',bio:'BIO',lin:'LIN',hum:'HUM'};
function enemTotal(st){st=st||{};if(!st.arq)return st;const A=st.arq,R={n:Math.max(A.n||0,st.n||0),best:Math.max(A.best||0,st.best||0),hist:st.hist||[],areas:JSON.parse(JSON.stringify(A.areas||{})),mt:JSON.parse(JSON.stringify(A.mt||{}))};
 for(const k in st.areas||{}){if(k==='FIS'||k in{MAT:1,QUI:1,BIO:1,LIN:1,HUM:1})continue;R.areas[k]=R.areas[k]||[0,0];R.areas[k][0]+=st.areas[k][0];R.areas[k][1]+=st.areas[k][1]}
 for(const m in st.mt||{}){const tp=st.mt[m].tp||{};let q=0,ac=0;const M=R.mt[m]=R.mt[m]||{n:0,q:0,ac:0,tp:{}};M.tp=M.tp||{};for(const k in tp){q+=tp[k][1];ac+=tp[k][0];if(m!=='fis'){M.tp[k]=M.tp[k]||[0,0];M.tp[k][0]+=tp[k][0];M.tp[k][1]+=tp[k][1]}}M.q+=q;M.ac+=ac;if(q)M.n++;
  if(AREA_DE[m]&&q){R.areas[AREA_DE[m]]=R.areas[AREA_DE[m]]||[0,0];R.areas[AREA_DE[m]][0]+=ac;R.areas[AREA_DE[m]][1]+=q}}
 if(st.mt0!=null&&A.mt0!=null)R.mt0=A.mt0;return R}
'''
s=s[:i]+TOT+s[j:]
rep("function statsDe(st){st=enemCorte(st||{});","function statsDe(st){st=enemTotal(st||{});")
rep("function enemState(){const e=eqState();if(!e.enem)e.enem={n:0,best:0,hist:[],areas:{},ep:ESTAT_EP};if(e.enem.ep!==ESTAT_EP){e.enem=enemCorte(e.enem);saveEq()}return e.enem}",
    "function enemState(){const e=eqState();if(!e.enem)e.enem={n:0,best:0,hist:[],areas:{}};if(e.enem.arq){e.enem=enemTotal(e.enem);saveEq()}return e.enem}")
open(f,'w',encoding='utf-8').write(s);print('total ok',f)
