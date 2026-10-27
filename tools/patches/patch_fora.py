import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:70]);s=s.replace(a,b)
rep("async enemTodos(){const{data,error}=await this.sb.rpc('admin_enem');","async foraEstat(n,v){const{error}=await this.sb.rpc('admin_fora_estat',{p_nick:n,p_fora:v});if(error)throw error},\nasync enemTodos(){const{data,error}=await this.sb.rpc('admin_enem');")
rep("map(u=>({nick:u.nick,turma:u.turma,enem:(u.equip&&u.equip.enem)||{}}))},","map(u=>({nick:u.nick,turma:u.turma,enem:(u.equip&&u.equip.enem)||{},fora:!!u.fora}))},\n  async foraEstat(n,v){const u=Object.values(this.db.users).find(x=>x.nick.toLowerCase()===n.toLowerCase());if(u){u.fora=!!v;this.save()}},")
# visão por turma ignora quem foi retirado das estatísticas
rep("function turmaResumo(tid,E){const rows=(AD.rows||[]).filter(r=>tid==='all'||r.turma===tid),",
    "function turmaResumo(tid,E){const rows=(AD.rows||[]).filter(r=>(tid==='all'||r.turma===tid)&&!(E[String(r.nick).toLowerCase()]||{}).fora),")
rep(" W.innerHTML=h;B.appendChild(W);\n W.querySelectorAll('[data-t]')",
    " {const fo=(AD.rows||[]).filter(r=>(E[String(r.nick).toLowerCase()]||{}).fora&&(tid==='all'||r.turma===tid));if(fo.length)h+=`<h3>FORA DAS ESTATÍSTICAS (${fo.length})</h3><p class=\"sdim\">${fo.map(r=>r.nome||r.nick).join(', ')} — os pontos continuam valendo para a tribo, mas não entram nas médias da turma nem no painel do diretor. Para voltar a contar, abra o aluno na lista.</p>`}\n W.innerHTML=h;B.appendChild(W);\n W.querySelectorAll('[data-t]')")
# botão na ficha do aluno
rep(" adStatsOpen(h)}\nasync function adTurma(",
    " const fx=x&&x.fora;h+=`<div class=\"codrow\" style=\"margin-top:14px\"><p>${fx?'⚠ Este aluno está <b>fora das estatísticas</b> da turma e do painel do diretor (os pontos continuam valendo).':'Se este aluno distorce as médias (ex.: chute em massa), dá para retirá-lo das estatísticas sem mexer nos pontos.'}</p><button class=\"sm\" id=\"foraBt\">${fx?'↩ VOLTAR A CONTAR NAS ESTATÍSTICAS':'🚫 RETIRAR DAS ESTATÍSTICAS'}</button></div>`;\n adStatsOpen(h);$('foraBt').onclick=async()=>{try{await API.foraEstat(r.nick,!fx);if(x)x.fora=!fx;else AD.enem=null;toast(!fx?'ALUNO RETIRADO DAS ESTATÍSTICAS':'ALUNO VOLTOU A CONTAR NAS ESTATÍSTICAS',3000);adAluno(r);if(AD.view==='turmas')renderAdmin()}catch(e){toast(errPT(e))}}}\nasync function adTurma(")
open(f,'w',encoding='utf-8').write(s);print('fora ok',f)
