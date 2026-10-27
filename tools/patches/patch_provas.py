import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:70]);s=s.replace(a,b)
# entradas próprias na escolha de matéria
rep("const MATERIAS=[['geral','SIMULADO GERAL (TODAS)',[]],",
    "const MATERIAS=[['geral','SIMULADO GERAL (TODAS)',[]],['espcex','ESPCEX · PROVA COMPLETA',[]],['ifsul','IF SUL DE MINAS · TÉCNICO INTEGRADO',null],")
rep("const QXF={geral:'*',","const QXF={geral:'*',espcex:'*',")
rep(" if(m==='geral'){if(QXS.geral)",
    " if(m==='espcex'){const fin=()=>{QXS.espcex=QXS.geral.filter(q=>q.banca==='espcex');if(ES.mat==='espcex')QX=QXS.espcex;cb&&cb()};if(QXS.geral)fin();else loadQX(fin,'geral');return}\n if(m==='geral'){if(QXS.geral)")
# ao escolher: prova fixa
rep("ES.ano='all';ES.banca=ES.banca||'enem';QX=QXS[id]||null;ES.src='enem';",
    "ES.ano='all';ES.banca=id==='espcex'?'espcex':(ES.fromEsp?'enem':ES.banca||'enem');ES.fromEsp=id==='espcex';if(id==='espcex'){ES.n=10;ES.dia=0}QX=QXS[id]||null;ES.src='enem';")
rep("id==='geral'?'Todas as matérias · ENEM e EsPCEx · de 12 a 180 questões':",
    "id==='geral'?'Todas as matérias · ENEM e EsPCEx · de 12 a 180 questões':id==='espcex'?'Escola de Cadetes do Exército · provas de 2025 e 2026 · 1º e 2º dia':")
rep("const s=el('small',null,id==='fis'?","const s=el('small',null,id==='ifsul'?'em breve':id==='fis'?")
# filtro de dia e chips só para a EsPCEx
rep(" if(ES.src==='enem'&&QX&&QX.some(q=>q.banca==='espcex')){",
    " if(ES.mat==='espcex'){B.appendChild(el('p','esub','1º dia: Português, Física e Química (44 questões). 2º dia: Matemática, Geografia, História e Inglês (56 questões).'));B.appendChild(el('div','elab','DIA DA PROVA'));const dc=el('div','echips');for(const[k,l]of[[0,'OS DOIS'],[1,'1º DIA'],[2,'2º DIA']])dc.appendChild(eBtn(l,'echip'+((ES.dia||0)===k?' on':''),()=>{ES.dia=k;renderEnem()}));B.appendChild(dc)}\n"
    " if(ES.mat!=='espcex'&&ES.src==='enem'&&QX&&QX.some(q=>q.banca==='espcex')){")
rep("return (QX||[]).filter(q=>bancaOk(q)&&","return (QX||[]).filter(q=>bancaOk(q)&&(ES.mat!=='espcex'||!ES.dia||q.dia===ES.dia)&&")
rep("for(const[n,l]of(ES.mat==='geral'?","for(const[n,l]of(ES.mat==='espcex'?[[10,'TREINO'],[22,'MEIA PROVA'],[44,'1º DIA COMPLETO'],[56,'2º DIA COMPLETO']]:ES.mat==='geral'?")
# estatística e cabeçalho pela matéria real da questão
rep("const mm=ES.mat==='geral'&&q.e?","const mm=(ES.mat==='geral'||ES.mat==='espcex')&&q.e?")
rep("`${ES.mat==='geral'&&q.e?'GERAL · '+","`${(ES.mat==='geral'||ES.mat==='espcex')&&q.e?(ES.mat==='espcex'?'ESPCEX · ':'GERAL · ')+")
open(f,'w',encoding='utf-8').write(s);print('provas ok',f)
