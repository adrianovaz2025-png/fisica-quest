import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:70]);s=s.replace(a,b)
rep("async foraEstat(n,v){const{error}=await this.sb.rpc('admin_fora_estat',{p_nick:n,p_fora:v});if(error)throw error},",
    "async foraEstat(n,v){const{error}=await this.sb.rpc('admin_fora_estat',{p_nick:n,p_fora:v});if(error)throw error},\nasync novaSenha(n,p){const{error}=await this.sb.rpc('admin_redefinir_senha',{p_nick:n,p_senha:p});if(error)throw error},")
# formulário de nova senha no topo da ficha do aluno (aparece para todos, até quem não fez simulado)
rep("async function adAluno(r){adStatsOpen('<p class=\"sdim\">Carregando estatísticas...</p>');",
    "function senhaBox(r){return`<div class=\"codrow\" style=\"margin:8px 0 4px\"><p>🔑 <b>Esqueceu a senha?</b> Crie uma senha nova para <b>${r.nick}</b> (mínimo 6 caracteres) e passe para o aluno. O login dele continua sendo o nick <b>${r.nick}</b>.</p><input class=\"inp\" id=\"nsIn\" type=\"text\" autocomplete=\"off\" placeholder=\"Nova senha\"><button class=\"sm\" id=\"nsBt\">REDEFINIR SENHA</button><span class=\"sdim\" id=\"nsMsg\"></span></div>`}\n"
    "function senhaWire(r){const b=$('nsBt');if(!b)return;b.onclick=async()=>{const v=$('nsIn').value.trim(),m=$('nsMsg');if(v.length<6){m.textContent='A senha precisa ter pelo menos 6 caracteres.';return}b.disabled=true;m.textContent='Salvando...';try{if(!API.novaSenha)throw new Error('Disponível só no modo online.');await API.novaSenha(r.nick,v);m.innerHTML='✔ Senha redefinida. Anote e passe para o aluno.'}catch(e){m.textContent=/nao_encontrado/.test(e.message)?'Aluno não encontrado.':errPT(e)}b.disabled=false}}\n"
    "async function adAluno(r){adStatsOpen('<p class=\"sdim\">Carregando estatísticas...</p>');")
rep("  <div class=\"estats\"><span>SIMULADOS<b>${S.n}</b></span>","  ${senhaBox(r)}<div class=\"estats\"><span>SIMULADOS<b>${S.n}</b></span>")
rep(" if(!qt){adStatsOpen(h+'<p class=\"sdim\">Este aluno ainda não fez simulados na Torre ENEM.</p>');return}",
    " if(!qt){adStatsOpen(h+'<p class=\"sdim\">Este aluno ainda não fez simulados na Torre ENEM.</p>');senhaWire(r);return}")
rep(" adStatsOpen(h);$('foraBt').onclick=async()=>{"," adStatsOpen(h);senhaWire(r);$('foraBt').onclick=async()=>{")
open(f,'w',encoding='utf-8').write(s);print('senha ok',f)
