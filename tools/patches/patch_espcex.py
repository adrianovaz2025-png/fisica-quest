import sys,re
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:70]);s=s.replace(a,b)
s=s.replace("ENEM ${X.ano}","${PRV(X)}").replace("ENEM ${q.X.ano}","${PRV(q.X)}")
# rótulo da prova (ENEM x EsPCEx)
rep("function qAnos(){","const PRV=X=>X&&X.banca==='espcex'?`ESPCEX ${X.ano} · ${X.dia}º DIA`:`ENEM ${X.ano}`;\nconst bancaOk=q=>!ES.banca||ES.banca==='all'||(q.banca||'enem')===ES.banca;\nfunction qAnos(){")
rep("function qAnos(){const s={};for(const q of QX||[])s[q.ano]=(s[q.ano]||0)+1;return s}",
    "function qAnos(){const s={};for(const q of QX||[])if(bancaOk(q))s[q.ano]=(s[q.ano]||0)+1;return s}")
rep("return (QX||[]).filter(q=>(ES.ano==='all'||q.ano===ES.ano)&&(!q.lg||q.lg===lg))}",
    "return (QX||[]).filter(q=>bancaOk(q)&&(ES.ano==='all'||q.ano===ES.ano)&&(!q.lg||q.lg===lg))}")
# escolha da prova na tela de quantidade
rep(" if(ES.src==='enem'&&QX){B.appendChild(el('div','elab','ANO DA PROVA'",
    " if(ES.src==='enem'&&QX&&QX.some(q=>q.banca==='espcex')){B.appendChild(el('div','elab','PROVA'));const bc=el('div','echips');for(const[k,l]of[['enem','ENEM'],['espcex','ESPCEX'],['all','TODAS']])bc.appendChild(eBtn(l,'echip'+((ES.banca||'enem')===k?' on':''),()=>{ES.banca=k;ES.ano='all';renderEnem()}));B.appendChild(bc)}\n"
    " if(ES.src==='enem'&&QX){B.appendChild(el('div','elab','ANO DA PROVA'")
rep("ES.ano='all';QX=QXS[id]||null;ES.src='enem';","ES.ano='all';ES.banca=ES.banca||'enem';QX=QXS[id]||null;ES.src='enem';")
rep("id==='fis'?'ENEM 2017–2025':id==='geral'?'Todas as matérias do ENEM · de 12 a 180 questões':id!=='fis'&&QXF[id]?(id==='lin'||id==='hum'?'ENEM 2020–2023 e 2025':'ENEM 2020–2025')",
    "id==='fis'?'ENEM 2017–2025 · EsPCEx 2025–2026':id==='geral'?'Todas as matérias · ENEM e EsPCEx · de 12 a 180 questões':id==='bio'?'ENEM 2020–2025':id!=='fis'&&QXF[id]?(id==='lin'||id==='hum'?'ENEM 2020–2023 e 2025 · EsPCEx 2025–2026':'ENEM 2020–2025 · EsPCEx 2025–2026')")
open(f,'w',encoding='utf-8').write(s);print('espcex ok',f,s.count('PRV('))
s=open(f,encoding='utf-8').read()
a="ES.src==='enem'?' DO ENEM'+(ES.ano==='all'?'':' '+ES.ano):''"
assert s.count(a)==1
s=s.replace(a,"ES.src==='enem'?' D'+({espcex:'A ESPCEX',all:'O ENEM E ESPCEX'}[ES.banca]||'O ENEM')+(ES.ano==='all'?'':' '+ES.ano):''")
open(f,'w',encoding='utf-8').write(s);print('botao ok')
