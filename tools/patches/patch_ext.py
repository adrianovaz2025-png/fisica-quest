import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(f,a[:60]);s=s.replace(a,b)
rep("const TURMA=id=>TURMAS.find(t=>t.id===id)||(id==='PROF'?PROF_T:TURMAS[0]);",
    "/* aluno externo: não pertence a nenhuma tribo, fica na Cidadela das Provas */\nconst EXT_T={id:'EXT',nome:'VESTIBULANDO',tribo:'CIDADELA DAS PROVAS',serie:3,cor:{r:['#a8b8f0','#6a7ad0','#3a4688'],f:'#7a8ae0'}};\nconst isExt=()=>!!(me&&me.turma==='EXT');\nconst TURMA=id=>TURMAS.find(t=>t.id===id)||(id==='PROF'?PROF_T:id==='EXT'?EXT_T:TURMAS[0]);")
rep("`+${r.ganho} PONTOS PARA A TRIBO ${TURMA(me.turma).tribo}!`","(isExt()?`+${r.ganho} PONTOS!`:`+${r.ganho} PONTOS PARA A TRIBO ${TURMA(me.turma).tribo}!`)")
rep("screen='game';tab='jornada';jView='mundo';","screen='game';tab=isExt()?'enem':'jornada';jView='mundo';")
open(f,'w',encoding='utf-8').write(s);print('ext ok',f)
