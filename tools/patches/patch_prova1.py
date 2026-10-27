import sys,re
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:70]);s=s.replace(a,b)
i=s.index("function eMat(B){");j=s.index("function eQtd(B){")
s=s[:i]+r"""/* 1º passo do simulado: escolher a prova */
const PROVAS=[['enem','ENEM','Exame Nacional do Ensino Médio · provas de 2017 a 2025 · todas as matérias','📘'],
 ['espcex','ESPCEX','Escola Preparatória de Cadetes do Exército · provas de 2025 e 2026','🎖️'],
 ['ifsul','IF SUL DE MINAS','Processo seletivo dos cursos técnicos integrados',null]];
function ePrv(B){eHead(B,'PARA QUAL PROVA VOCÊ QUER ESTUDAR?','home');const g=el('div','elist');
 for(const[id,n,d,ic]of PROVAS){const b=eBtn(ic?`${ic} ${n}`:`🔒 ${n} — em breve`,'eopt eprova'+(ic?'':' off'),()=>{if(!ic)return;ES.prova=id;ES.banca=id;ES.scr='mat';if(id==='espcex')loadQX(null,'espcex');renderEnem()});b.appendChild(el('small',null,d));g.appendChild(b)}B.appendChild(g)}
/* 2º passo: matéria (dentro da prova escolhida) */
const MAT_ESP={espcex:'PROVA COMPLETA (1º E 2º DIA)',fis:'FÍSICA',mat:'MATEMÁTICA',qui:'QUÍMICA',lin:'PORTUGUÊS E INGLÊS',hum:'GEOGRAFIA E HISTÓRIA'};
function eMat(B){const P=ES.prova||'enem';eHead(B,(P==='espcex'?'ESPCEX':'ENEM')+' · ESCOLHA A MATÉRIA','prova');const g=el('div','elist');
 for(const[id,n0,qb]of MATERIAS){
  if(P==='espcex'?!MAT_ESP[id]:(id==='espcex'||id==='ifsul'))continue;
  const n=P==='espcex'?MAT_ESP[id]:n0;
  const b=eBtn(qb?`⚡ ${n}`:`🔒 ${n} — em breve`,'eopt'+(qb?'':' off'),()=>{if(!qb)return;ES.mat=id;ES.scr='qtd';if(id==='geral')ES.n=24;else if(ES.n>45||ES.n%12===0)ES.n=10;ES.ano='all';ES.banca=P;if(id==='espcex'){ES.n=10;ES.dia=0}QX=QXS[id]||null;ES.src='enem';loadQX(()=>{if(ES.scr==='qtd')renderEnem()},id);renderEnem()});
  if(qb){const sub=P==='espcex'?(id==='espcex'?'Prova inteira · 1º dia: Português, Física e Química · 2º dia: Matemática, Geografia, História e Inglês':id==='lin'?'Questões de Português e de Inglês da EsPCEx':id==='hum'?'Questões de Geografia e de História da EsPCEx':'EsPCEx 2025 e 2026')
    :(id==='fis'?'ENEM 2017–2025':id==='geral'?'Todas as matérias do ENEM · de 12 a 180 questões':id==='lin'||id==='hum'?'ENEM 2020–2023 e 2025':'ENEM 2020–2025');b.appendChild(el('small',null,sub))}
  g.appendChild(b)}B.appendChild(g)}
"""+s[j:]
rep("({home:eHome,mat:eMat,","({home:eHome,prova:ePrv,mat:eMat,")
rep("R2.appendChild(eBtn('▶ SIMULADO','big2 ebig',()=>{ES.scr='mat';renderEnem()}));","R2.appendChild(eBtn('▶ SIMULADO','big2 ebig',()=>{ES.scr='prova';renderEnem()}));")
rep("B.appendChild(eBtn('▶ SIMULADO','big2',()=>{ES.scr='mat';renderEnem()}));return}","B.appendChild(eBtn('▶ SIMULADO','big2',()=>{ES.scr='prova';renderEnem()}));return}")
# a prova já foi escolhida: some o filtro ENEM/ESPCEX dentro da matéria
rep(" if(ES.mat!=='espcex'&&ES.src==='enem'&&QX&&QX.some(q=>q.banca==='espcex')){"," if(!ES.prova&&ES.mat!=='espcex'&&ES.src==='enem'&&QX&&QX.some(q=>q.banca==='espcex')){")
rep(".adt tr.clk{cursor:pointer}",".eopt.eprova{padding:18px 16px}.eopt.eprova small{margin-top:6px}.adt tr.clk{cursor:pointer}")
open(f,'w',encoding='utf-8').write(s);print('prova1 ok',f)
s=open(f,encoding='utf-8').read()
a=" if(ES.mat==='lin'||ES.mat==='geral'){B.appendChild(el('div','elab','LÍNGUA ESTRANGEIRA"
assert s.count(a)==1
s=s.replace(a," if((ES.mat==='lin'||ES.mat==='geral')&&ES.banca!=='espcex'){B.appendChild(el('div','elab','LÍNGUA ESTRANGEIRA")
open(f,'w',encoding='utf-8').write(s);print('lg ok')
