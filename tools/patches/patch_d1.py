import sys,json
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:70]);s=s.replace(a,b)
NM=json.load(open('/home/claude/work/d1/temas_d1.json',encoding='utf-8'))
rep("const MATERIAS=[['fis','FÍSICA',QB_FIS],['mat','MATEMÁTICA',[]],['qui','QUÍMICA',[]],['bio','BIOLOGIA',[]]];",
    "const MATERIAS=[['fis','FÍSICA',QB_FIS],['mat','MATEMÁTICA',[]],['qui','QUÍMICA',[]],['bio','BIOLOGIA',[]],['lin','LINGUAGENS',[]],['hum','CIÊNCIAS HUMANAS',[]]];")
rep("const QXF={fis:'questoes.json',mat:'matematica.json',qui:'quimica.json',bio:'biologia.json'}","const QXF={fis:'questoes.json',mat:'matematica.json',qui:'quimica.json',bio:'biologia.json',lin:'linguagens.json',hum:'humanas.json'}")
rep("const AREAS={MAT:'MATEMÁTICA',","const AREAS={LIN:'LINGUAGENS',HUM:'CIÊNCIAS HUMANAS',MAT:'MATEMÁTICA',")
# língua estrangeira (questões 1 a 5): inglês ou espanhol, como na inscrição do ENEM
rep("function qPool(){if(ES.src!=='enem')return MATERIAS.find(m=>m[0]===ES.mat)[2];return (QX||[]).filter(q=>ES.ano==='all'||q.ano===ES.ano)}",
    "function qPool(){if(ES.src!=='enem')return MATERIAS.find(m=>m[0]===ES.mat)[2];const lg=ES.lg||'i';return (QX||[]).filter(q=>(ES.ano==='all'||q.ano===ES.ano)&&(!q.lg||q.lg===lg))}")
rep("else if(QXF[ES.mat])ES.src='enem';else ES.src='rap';",
    "else if(QXF[ES.mat])ES.src='enem';else ES.src='rap';\n if(ES.mat==='lin'){B.appendChild(el('div','elab','LÍNGUA ESTRANGEIRA (QUESTÕES 1 A 5)'));const lc=el('div','echips');for(const[k,l]of[['i','INGLÊS'],['e','ESPANHOL']])lc.appendChild(eBtn(l,'echip'+((ES.lg||'i')===k?' on':''),()=>{ES.lg=k;renderEnem()}));B.appendChild(lc)}")
# estatísticas do professor
rep("MATN={fis:'FÍSICA',mat:'MATEMÁTICA',qui:'QUÍMICA',bio:'BIOLOGIA'},LEGA={MAT:'mat',QUI:'qui',BIO:'bio'}",
    "MATN={fis:'FÍSICA',mat:'MATEMÁTICA',qui:'QUÍMICA',bio:'BIOLOGIA',lin:'LINGUAGENS',hum:'CIÊNCIAS HUMANAS'},LEGA={MAT:'mat',QUI:'qui',BIO:'bio',LIN:'lin',HUM:'hum'}")
rep("const TEMAS={","const TEMAS={lin:"+json.dumps(NM['lin'],ensure_ascii=False)+",hum:"+json.dumps(NM['hum'],ensure_ascii=False)+",")
rep("if(['mat','qui','bio'].some(","if(['mat','qui','bio','lin','hum'].some(")
open(f,'w',encoding='utf-8').write(s);print('d1 ok',f)
s=open(f,encoding='utf-8').read()
a="id!=='fis'&&QXF[id]?'ENEM 2020–2025'"
assert s.count(a)==1;s=s.replace(a,"id!=='fis'&&QXF[id]?(id==='lin'||id==='hum'?'ENEM 2020–2023 e 2025':'ENEM 2020–2025')")
open(f,'w',encoding='utf-8').write(s);print('lbl ok')
