import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:70]);s=s.replace(a,b)
rep("if(id!=='fis')ES.src='enem';loadQX(","ES.src='enem';loadQX(")
rep("id==='fis'?`ENEM 2017–2025 + ${qb.length} rápidas`:","id==='fis'?'ENEM 2017–2025':")
rep("if(ES.mat==='fis'){B.appendChild(el('div','elab','FONTE'));","ES.src='enem';if(false){B.appendChild(el('div','elab','FONTE'));")
open(f,'w',encoding='utf-8').write(s);print('norap ok',f)
