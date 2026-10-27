import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:70]);s=s.replace(a,b)
rep("['ifsul','IF SUL DE MINAS · TÉCNICO INTEGRADO',null]","['ifsul','IF SUL DE MINAS · PROVA COMPLETA',[]]")
rep("['ifsul','IF SUL DE MINAS','Processo seletivo dos cursos técnicos integrados',null]","['ifsul','IF SUL DE MINAS','Processo seletivo dos cursos técnicos integrados · provas de 2025 e 2026','🏫']")
rep("if(id==='espcex')loadQX(null,'espcex');renderEnem()}","if(id==='espcex'||id==='ifsul')loadQX(null,id);renderEnem()}")
rep("const QXF={geral:'*',espcex:'*',","const QXF={geral:'*',espcex:'*',ifsul:'*',")
rep(" if(m==='espcex'){const fin=()=>{QXS.espcex=QXS.geral.filter(q=>q.banca==='espcex');if(ES.mat==='espcex')QX=QXS.espcex;cb&&cb()};if(QXS.geral)fin();else loadQX(fin,'geral');return}",
    " if(m==='espcex'||m==='ifsul'){const fin=()=>{QXS[m]=QXS.geral.filter(q=>q.banca===m);if(ES.mat===m)QX=QXS[m];cb&&cb()};if(QXS.geral)fin();else loadQX(fin,'geral');return}")
rep("const PRV=X=>X&&X.banca==='espcex'?`ESPCEX ${X.ano} · ${X.dia}º DIA`:`ENEM ${X.ano}`;",
    "const PRV=X=>X&&X.banca==='espcex'?`ESPCEX ${X.ano} · ${X.dia}º DIA`:X&&X.banca==='ifsul'?`IF SUL DE MINAS ${X.ano}`:`ENEM ${X.ano}`;")
# matérias dentro da prova
rep("const MAT_ESP={","const MAT_IF={ifsul:'PROVA COMPLETA (50 QUESTÕES)',mat:'MATEMÁTICA',lin:'LÍNGUA PORTUGUESA'};\nconst MAT_ESP={")
rep("eHead(B,(P==='espcex'?'ESPCEX':'ENEM')+' · ESCOLHA A MATÉRIA','prova');",
    "const MM=P==='espcex'?MAT_ESP:P==='ifsul'?MAT_IF:null;eHead(B,({espcex:'ESPCEX',ifsul:'IF SUL DE MINAS'}[P]||'ENEM')+' · ESCOLHA A MATÉRIA','prova');")
rep("  if(P==='espcex'?!MAT_ESP[id]:(id==='espcex'||id==='ifsul'))continue;\n  const n=P==='espcex'?MAT_ESP[id]:n0;",
    "  if(MM?!MM[id]:(id==='espcex'||id==='ifsul'))continue;\n  const n=MM?MM[id]:n0;")
rep("if(id==='espcex'){ES.n=10;ES.dia=0}QX=QXS[id]||null;ES.src='enem';loadQX(()=>{if(ES.scr==='qtd')renderEnem()},id);renderEnem()});",
    "if(id==='espcex'||id==='ifsul'){ES.n=10;ES.dia=0}QX=QXS[id]||null;ES.src='enem';loadQX(()=>{if(ES.scr==='qtd')renderEnem()},id);renderEnem()});")
rep("  if(qb){const sub=P==='espcex'?",
    "  if(qb){const sub=P==='ifsul'?(id==='ifsul'?'Prova inteira · 25 de Língua Portuguesa e 25 de Matemática':id==='lin'?'Questões de Língua Portuguesa do IF Sul de Minas':'Questões de Matemática do IF Sul de Minas')+' · 2025 e 2026':P==='espcex'?")
# quantidades, estatística, cabeçalho
rep("for(const[n,l]of(ES.mat==='espcex'?","for(const[n,l]of(ES.mat==='ifsul'?[[10,'TREINO'],[25,'MEIA PROVA'],[50,'PROVA COMPLETA']]:ES.mat==='espcex'?")
rep("const mm=(ES.mat==='geral'||ES.mat==='espcex')&&q.e?","const mm=(ES.mat==='geral'||ES.mat==='espcex'||ES.mat==='ifsul')&&q.e?")
rep("`${(ES.mat==='geral'||ES.mat==='espcex')&&q.e?(ES.mat==='espcex'?'ESPCEX · ':'GERAL · ')+",
    "`${(ES.mat==='geral'||ES.mat==='espcex'||ES.mat==='ifsul')&&q.e?({espcex:'ESPCEX · ',ifsul:'IF SUL · '}[ES.mat]||'GERAL · ')+")
rep("&&ES.banca!=='espcex'){","&&ES.banca!=='espcex'&&ES.banca!=='ifsul'){")
rep("{espcex:'A ESPCEX',all:'O ENEM E ESPCEX'}","{espcex:'A ESPCEX',ifsul:'O IF SUL DE MINAS',all:'O ENEM E ESPCEX'}")
open(f,'w',encoding='utf-8').write(s);print('ifsul ok',f)
