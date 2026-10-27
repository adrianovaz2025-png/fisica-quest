import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:70]);s=s.replace(a,b)
# ---------- telas ----------
rep('''    <button class="lnk" id="toSign">Não tenho conta: criar agora</button>
  </div>''','''    <button class="lnk" id="toSign">Não tenho conta: criar agora</button>
    <button class="lnk" id="toRec">Esqueci minha senha</button>
  </div>
  <div id="aRec" style="display:none">
    <p class="note" style="margin:0 0 8px">Digite seu nick. Se você cadastrou um e-mail de recuperação, enviamos um link para criar uma senha nova.</p>
    <label>NICK</label><input class="inp" id="rNick" maxlength="16" autocomplete="username" autocapitalize="off">
    <button class="big" id="rGo">ENVIAR LINK</button>
    <button class="lnk" id="rBack">Voltar para entrar</button>
  </div>
  <div id="aNew" style="display:none">
    <label>NOVA SENHA (mínimo 6 caracteres)</label><input class="inp" id="nPass" type="password" autocomplete="new-password">
    <label>REPITA A NOVA SENHA</label><input class="inp" id="nPass2" type="password" autocomplete="new-password">
    <button class="big" id="nGo">SALVAR SENHA E ENTRAR</button>
  </div>''')
rep('''    <label>CÓDIGO DA TURMA (peça ao professor)</label>''','''    <label>E-MAIL PARA RECUPERAR A SENHA (opcional, só usado se você esquecer a senha)</label><input class="inp" id="sEmail" type="email" maxlength="120" autocomplete="email" autocapitalize="off">
    <label>CÓDIGO DA TURMA (peça ao professor)</label>''')
rep('<div class="ov" id="trib"><div class="box">','''<div class="ov" id="emq"><div class="box">
  <button class="x" id="emx">X</button>
  <h2>PROTEJA SUA CONTA</h2><h3>E-MAIL DE RECUPERAÇÃO</h3>
  <p class="note" style="font-size:13px;line-height:1.5">Se um dia você esquecer a senha, mandamos um link para este e-mail criar uma nova. Ele não aparece para ninguém no jogo.</p>
  <label>SEU E-MAIL</label><input class="inp" id="emIn" type="email" maxlength="120" autocomplete="email" autocapitalize="off">
  <button class="big" id="emGo">SALVAR E-MAIL</button>
  <button class="lnk" id="emNo">Agora não</button>
  <div class="fb" id="emMsg"></div>
</div></div>

<div class="ov" id="trib"><div class="box">''')
# ---------- API ----------
rep("async foraEstat(n,v){const{error}=await this.sb.rpc('admin_fora_estat',",
    "async recupPedir(n){const r=await fetch(CONFIG.SUPABASE_URL+'/functions/v1/recuperar-senha',{method:'POST',headers:{'Content-Type':'application/json',apikey:CONFIG.SUPABASE_KEY,Authorization:'Bearer '+CONFIG.SUPABASE_KEY},body:JSON.stringify({nick:n})});let j={};try{j=await r.json()}catch(e){}if(!r.ok&&!j.ok)throw new Error(j.erro||('Erro '+r.status));return j},\n"
    "async recupNova(th,p){const v=await this.sb.auth.verifyOtp({token_hash:th,type:'recovery'});if(v.error)throw v.error;this.uid=v.data.user.id;const u=await this.sb.auth.updateUser({password:p});if(u.error)throw u.error;return this.profile()},\n"
    "async salvarEmail(e){const{error}=await this.sb.rpc('salvar_email_recup',{p_email:e});if(error)throw error},\n"
    "async meuEmail(){const{data,error}=await this.sb.rpc('meu_email_recup');if(error)throw error;return data},\n"
    "async foraEstat(n,v){const{error}=await this.sb.rpc('admin_fora_estat',")
# ---------- abrir os modos ----------
rep("function openAuth(m){$('aLog').style.display=m==='login'?'block':'none';$('aSign').style.display=m==='signup'?'block':'none';$('aT').textContent=m==='login'?'ENTRAR':'CRIAR CONTA';",
    "function openAuth(m){$('aLog').style.display=m==='login'?'block':'none';$('aSign').style.display=m==='signup'?'block':'none';$('aRec').style.display=m==='rec'?'block':'none';$('aNew').style.display=m==='new'?'block':'none';$('aT').textContent={login:'ENTRAR',signup:'CRIAR CONTA',rec:'RECUPERAR SENHA',new:'CRIAR SENHA NOVA'}[m];")
rep("$('ax').onclick=()=>$('auth').classList.remove('on');",
    "$('ax').onclick=()=>$('auth').classList.remove('on');$('toRec').onclick=()=>{openAuth('rec');$('rNick').value=$('lNick').value};$('rBack').onclick=()=>openAuth('login');\n"
    "$('rGo').onclick=async()=>{const n=$('rNick').value.trim();if(!/^[A-Za-z0-9_]{3,16}$/.test(n)){$('aMsg').textContent='Digite o seu nick.';return}if(!ONLINE||!API.recupPedir){$('aMsg').textContent='Recuperação disponível só no jogo online.';return}$('rGo').disabled=true;$('aMsg').textContent='Enviando...';\n"
    " try{const j=await API.recupPedir(n);$('aMsg').textContent=j.limite?'Muitos pedidos para este nick. Tente de novo em 1 hora.':j.semEmail?'Este nick não tem e-mail de recuperação cadastrado. Peça ao professor para redefinir sua senha.':'Pronto! Se o nick existir e tiver e-mail cadastrado, o link chega em alguns minutos (olhe também o spam).'}catch(e){$('aMsg').textContent='Não foi possível enviar agora. Peça ao professor para redefinir sua senha.'}$('rGo').disabled=false};\n"
    "$('nGo').onclick=async()=>{const a=$('nPass').value,b=$('nPass2').value;if(a.length<6){$('aMsg').textContent='A senha precisa ter pelo menos 6 caracteres.';return}if(a!==b){$('aMsg').textContent='As duas senhas não são iguais.';return}$('nGo').disabled=true;$('aMsg').textContent='Salvando...';\n"
    " try{me=await API.recupNova(RECUP,a);RECUP=null;history.replaceState(null,'',location.pathname);$('auth').classList.remove('on');toast('SENHA NOVA SALVA! BEM-VINDO DE VOLTA',4000);enterGame()}catch(e){$('aMsg').textContent=/expired|invalid|otp/i.test(e.message||'')?'Este link expirou ou já foi usado. Peça um link novo em \"Esqueci minha senha\".':errPT(e)}$('nGo').disabled=false};\n"
    "$('emx').onclick=$('emNo').onclick=()=>$('emq').classList.remove('on');\n"
    "$('emGo').onclick=async()=>{const v=$('emIn').value.trim();if(!/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(v)){$('emMsg').textContent='Digite um e-mail válido.';return}$('emGo').disabled=true;try{await API.salvarEmail(v);$('emq').classList.remove('on');toast('E-MAIL DE RECUPERAÇÃO SALVO',3000)}catch(e){$('emMsg').textContent=errPT(e)}$('emGo').disabled=false};\n"
    "let RECUP=new URLSearchParams(location.search).get('recup');\n"
    "async function pedirEmail(){if(!ONLINE||!me||isAdm()||!API.meuEmail)return;const k='fq_emq_'+String(me.nick).toLowerCase();let n=0;try{n=+localStorage.getItem(k)||0}catch(e){}if(n>=3)return;try{if(await API.meuEmail())return}catch(e){return}try{localStorage.setItem(k,n+1)}catch(e){}setTimeout(()=>{if(screen==='game'&&!document.querySelector('.ov.on'))$('emq').classList.add('on')},2500)}")
# e-mail do cadastro
rep("nome=$('sNome').value.trim().replace(/\\s+/g,' ');","nome=$('sNome').value.trim().replace(/\\s+/g,' '),em=$('sEmail').value.trim();")
rep(" if(p.length<6){$('aMsg').textContent='A senha precisa ter pelo menos 6 caracteres.';return}\n if(!cd){",
    " if(p.length<6){$('aMsg').textContent='A senha precisa ter pelo menos 6 caracteres.';return}\n if(em&&!/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(em)){$('aMsg').textContent='E-mail inválido (ou deixe em branco).';return}\n if(!cd){")
rep("pending={nick:n,senha:p,turma:t,codigo:cd,nome};","pending={nick:n,senha:p,turma:t,codigo:cd,nome,email:em};")
rep("try{me=await API.signup({...pending,personagem:selIdx});pending=null;enterGame()}",
    "try{const em=pending.email;me=await API.signup({...pending,personagem:selIdx});pending=null;if(em&&API.salvarEmail)API.salvarEmail(em).catch(()=>{});enterGame()}")
# depois de entrar: link de recuperação ou pedido de e-mail
rep("function enterGame(){screen='game';","function enterGame(){setTimeout(pedirEmail,4000);screen='game';")
rep("setTimeout(()=>{tribeWorld=buildTribeWorld(levelsOf(tribeData));tribeDirty=false;busy(false);if(me)enterGame();else screen='title'},30)}",
    "setTimeout(()=>{tribeWorld=buildTribeWorld(levelsOf(tribeData));tribeDirty=false;busy(false);if(RECUP&&ONLINE){screen='title';openAuth('new')}else if(me)enterGame();else screen='title'},30)}")
open(f,'w',encoding='utf-8').write(s);print('recup ok',f)
