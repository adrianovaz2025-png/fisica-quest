import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:70]);s=s.replace(a,b)
# matéria nova no topo da lista
rep("const MATERIAS=[['fis','FÍSICA',QB_FIS],","const MATERIAS=[['geral','SIMULADO GERAL (TODAS)',[]],['fis','FÍSICA',QB_FIS],")
rep("const QXF={fis:'questoes.json',","const QXF={geral:'*',fis:'questoes.json',")
# carregar o simulado geral = junta os 6 bancos, marcando a matéria de cada questão
rep("function loadQX(cb,m){m=m||ES.mat;if(!QXF[m]){cb&&cb();return}",
    "const AREA2MAT={MAT:'mat',QUI:'qui',BIO:'bio',LIN:'lin',HUM:'hum'},GERAL_M=['lin','hum','fis','qui','bio','mat'];\n"
    "function loadQX(cb,m){m=m||ES.mat;if(!QXF[m]){cb&&cb();return}\n"
    " if(m==='geral'){if(QXS.geral){if(ES.mat==='geral')QX=QXS.geral;cb&&cb();return}let k=0;const done=()=>{if(++k<GERAL_M.length)return;QXS.geral=[];for(const mm of GERAL_M)for(const q of QXS[mm]||[]){q.mt=mm;QXS.geral.push(q)}if(ES.mat==='geral')QX=QXS.geral;cb&&cb()};for(const mm of GERAL_M)loadQX(done,mm);return}")
# para cada matéria carregada, guarda de qual matéria é cada questão
rep("QXS[m]=a.filter(q=>q.gab&&!q.anulada);return QXS[m]","QXS[m]=a.filter(q=>q.gab&&!q.anulada);for(const q of QXS[m])q.mt=m;return QXS[m]")
# quantidades do simulado geral (múltiplos de 12: 4 áreas iguais, como no ENEM)
rep("for(const[n,l]of[[5,'AQUECIMENTO'],[10,'TREINO'],[20,'DESAFIO'],[45,'PROVA COMPLETA']]){",
    "for(const[n,l]of(ES.mat==='geral'?[[12,'RÁPIDO'],[24,'TREINO'],[48,'DESAFIO'],[90,'UM DIA DE ENEM'],[180,'ENEM COMPLETO']]:[[5,'AQUECIMENTO'],[10,'TREINO'],[20,'DESAFIO'],[45,'PROVA COMPLETA']])){")
rep("if(ES.mat==='lin'){B.appendChild(el('div','elab','LÍNGUA ESTRANGEIRA (QUESTÕES 1 A 5)'));",
    "if(ES.mat==='geral')B.appendChild(el('p','esub','As questões vêm das 4 áreas do ENEM em partes iguais: Linguagens, Ciências Humanas, Ciências da Natureza (Física, Química e Biologia) e Matemática.'));\n if(ES.mat==='lin'||ES.mat==='geral'){B.appendChild(el('div','elab','LÍNGUA ESTRANGEIRA (QUESTÕES 1 A 5)'));")
# sorteio equilibrado por área no simulado geral
rep("function startSim(qb){profHide();const idx=shuf(qb.map((_,i)=>i),(Date.now()&0xffff)).slice(0,Math.min(ES.n,qb.length)),",
    "function geralIdx(qb,n){const per={lin:n/4,hum:n/4,mat:n/4,fis:n/12,qui:n/12,bio:n/12},out=[],sd=Date.now()&0xffff;\n"
    " for(const mm of GERAL_M){const ids=qb.map((q,i)=>q.mt===mm?i:-1).filter(i=>i>=0);out.push(...shuf(ids,sd+mm.charCodeAt(0)*31).slice(0,Math.round(per[mm])))}\n"
    " if(out.length<n){const rest=shuf(qb.map((_,i)=>i).filter(i=>!out.includes(i)),sd+7);out.push(...rest.slice(0,n-out.length))}return out.slice(0,n)}\n"
    "function startSim(qb){profHide();const idx=ES.mat==='geral'&&ES.src==='enem'?geralIdx(qb,Math.min(ES.n,qb.length)):shuf(qb.map((_,i)=>i),(Date.now()&0xffff)).slice(0,Math.min(ES.n,qb.length)),")
# cabeçalho mostra a matéria da questão
rep("h.appendChild(el('span','etit2',`${mat} · QUESTÃO ${ES.cur+1}/${n}`));",
    "h.appendChild(el('span','etit2',`${ES.mat==='geral'&&q.e?'GERAL · '+((MATERIAS.find(m=>m[0]===q.X.mt)||[0,''])[1]):mat} · QUESTÃO ${ES.cur+1}/${n}`));")
# estatística por matéria real de cada questão
rep("{if(!st.mt){st.mt={};st.mt0=st.n}const M=st.mt[ES.mat]=st.mt[ES.mat]||{n:0,q:0,ac:0,tp:{}};M.n++;M.q+=n;M.ac+=ac;for(const q of qs){const k=q.e?(q.X.tema||q.X.area):ES.bank[q.i][0];M.tp[k]=M.tp[k]||[0,0];M.tp[k][1]++;if(isOk(q))M.tp[k][0]++}}",
    "{if(!st.mt){st.mt={};st.mt0=st.n}const G={};for(const q of qs){const mm=ES.mat==='geral'&&q.e?(q.X.mt||AREA2MAT[q.X.area]||'fis'):ES.mat;(G[mm]=G[mm]||[]).push(q)}\n"
    "  for(const mm in G){const M=st.mt[mm]=st.mt[mm]||{n:0,q:0,ac:0,tp:{}};M.n++;M.q+=G[mm].length;M.ac+=G[mm].filter(isOk).length;for(const q of G[mm]){const k=q.e?(q.X.tema||q.X.area):ES.bank[q.i][0];M.tp[k]=M.tp[k]||[0,0];M.tp[k][1]++;if(isOk(q))M.tp[k][0]++}}}")
rep("id!=='fis'&&QXF[id]?(id==='lin'||id==='hum'?'ENEM 2020–2023 e 2025':'ENEM 2020–2025')",
    "id==='geral'?'Todas as matérias do ENEM · de 12 a 180 questões':id!=='fis'&&QXF[id]?(id==='lin'||id==='hum'?'ENEM 2020–2023 e 2025':'ENEM 2020–2025')")
open(f,'w',encoding='utf-8').write(s);print('geral ok',f)
s=open(f,encoding='utf-8').read()
a="ES.mat=id;ES.scr='qtd';"
assert s.count(a)==1;s=s.replace(a,"ES.mat=id;ES.scr='qtd';if(id==='geral')ES.n=24;else if(ES.n>45||ES.n%12===0)ES.n=10;")
open(f,'w',encoding='utf-8').write(s);print('n ok')
