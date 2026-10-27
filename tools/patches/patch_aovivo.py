import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:70]);s=s.replace(a,b)
# API online
rep("async alunos(){const{data,error}=await this.sb.rpc('admin_alunos');if(error)throw error;return data||[]},",
    "async alunos(){const{data,error}=await this.sb.rpc('admin_alunos');if(error)throw error;return data||[]},\n"
    "async ping(at){try{await this.sb.rpc('ping',{p_ativo:!!at})}catch(e){}},\n"
    "async aoVivo(){const{data,error}=await this.sb.rpc('admin_ao_vivo');if(error)throw error;return data||[]},")
# presença do aluno: batimento a cada 45 s enquanto o jogo está aberto e visível
rep("async function adminLoad(){",
"""let LASTACT=Date.now();for(const ev of['pointerdown','keydown','touchstart','wheel'])addEventListener(ev,()=>{LASTACT=Date.now()},{passive:true});
function pingTick(){if(!ONLINE||!me||isAdm()||screen!=='game'||document.visibilityState!=='visible'||!API.ping)return;API.ping(Date.now()-LASTACT<180000)}
setInterval(pingTick,45000);document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='visible')pingTick()});
/* ===== AO VIVO: quem está jogando agora e quem jogou hoje ===== */
const hhmm=t=>t?new Date(t).toLocaleTimeString('pt-BR',{hour:'2-digit',minute:'2-digit'}):'—';
function agoTxt(t){if(!t)return'—';const s=(Date.now()-new Date(t))/1000;return s<90?'agora':s<3600?Math.round(s/60)+' min atrás':hhmm(t)}
async function aoVivoLoad(){try{AD.vivo=await API.aoVivo();AD.vivoT=Date.now();AD.vivoErr=''}catch(e){AD.vivoErr=errPT(e)}if(AD.view==='vivo'&&$('admin').classList.contains('on'))renderAdmin()}
setInterval(()=>{if(AD.view==='vivo'&&$('admin').classList.contains('on')&&API.aoVivo)aoVivoLoad()},30000);
function renderVivo(B){if(AD.vivoErr){B.appendChild(el('p','esub',AD.vivoErr));return}if(!AD.vivo){B.appendChild(el('p','esub','Carregando...'));if(API.aoVivo)aoVivoLoad();else B.appendChild(el('p','esub','Disponível só no jogo online.'));return}
 const hojeD=new Date().toLocaleDateString('sv-SE',{timeZone:'America/Sao_Paulo'}),isHoje=t=>t&&new Date(t).toLocaleDateString('sv-SE',{timeZone:'America/Sao_Paulo'})===hojeD;
 const L=AD.vivo.map(r=>({...r,on:r.visto_em&&Date.now()-new Date(r.visto_em)<150000,hoje:isHoje(r.visto_em)||r.simulados>0}));
 const on=L.filter(r=>r.on),hoje=L.filter(r=>r.hoje),Q=hoje.reduce((a,r)=>a+r.questoes,0),A=hoje.reduce((a,r)=>a+r.acertos,0);
 B.appendChild(el('p','sdim',`Atualiza sozinho a cada 30 s · última leitura ${hhmm(AD.vivoT)}. “Online agora” = mexeu no jogo nos últimos 2 minutos. Questões contam os simulados do ENEM entregues hoje.`));
 const sx=el('div','estats');sx.innerHTML=`<span>ONLINE AGORA<b style="color:#5ac86a">${on.length}</b></span><span>JOGARAM HOJE<b>${hoje.length}</b></span><span>QUESTÕES HOJE<b>${Q}</b></span><span>ACERTO HOJE<b>${Q?Math.round(A/Q*100):0}%</b></span>`;B.appendChild(sx);
 /* por turma */
 const wrapT=el('div','adw'),tt=el('table','adt');wrapT.style.flex='none';tt.innerHTML='<tr><th>TURMA</th><th>ONLINE AGORA</th><th>JOGARAM HOJE</th><th>QUESTÕES HOJE</th><th>ACERTO</th></tr>';
 for(const T of TURMAS){const g=L.filter(r=>r.turma===T.id);if(!g.length)continue;const gh=g.filter(r=>r.hoje),q=gh.reduce((a,r)=>a+r.questoes,0),a=gh.reduce((a,r)=>a+r.acertos,0);const t=el('tr');t.innerHTML=`<td>${T.nome}</td><td class="n">${g.filter(r=>r.on).length}</td><td class="n">${gh.length} de ${g.length}</td><td class="n">${q}</td><td class="n">${q?Math.round(a/q*100)+'%':'—'}</td>`;tt.appendChild(t)}
 wrapT.appendChild(tt);B.appendChild(wrapT);
 /* lista de alunos de hoje */
 const ft=el('div','erow');for(const[k,l]of[['all','TODAS'],...TURMAS.map(t=>[t.id,t.id])])ft.appendChild(eBtn(l,'sm'+((AD.vt||'all')===k?' on':''),()=>{AD.vt=k;renderAdmin()}));B.appendChild(ft);
 const rows=hoje.filter(r=>(AD.vt||'all')==='all'||r.turma===AD.vt).sort((a,b)=>(b.on-a.on)||(new Date(b.visto_em||b.ult_simulado||0)-new Date(a.visto_em||a.ult_simulado||0)));
 const w=el('div','adw'),tb=el('table','adt');w.style.flex='none';tb.innerHTML='<tr><th></th><th>ALUNO</th><th>TURMA</th><th>VISTO</th><th>ENTROU</th><th>TEMPO</th><th>SIMULADOS</th><th>QUESTÕES</th><th>ACERTOS</th><th>PONTOS HOJE</th></tr>';
 for(const r of rows){const t=el('tr','clk');t.title='Ver estatísticas';t.onclick=async()=>{if(!AD.rows){try{AD.rows=await API.alunos()}catch(e){}}adAluno((AD.rows||[]).find(x=>x.nick===r.nick)||r)};
  t.innerHTML=`<td>${r.on?'<span class="vivo"></span>':''}</td><td>${r.nome||r.nick}<br><small class="sdim">${r.nick}</small></td><td>${r.turma}</td><td>${r.on?'<b style="color:#5ac86a">online</b>':agoTxt(r.visto_em)}</td><td>${hhmm(r.primeiro_hoje)}</td><td class="n">${r.min_hoje?r.min_hoje+' min':'—'}</td><td class="n">${r.simulados}</td><td class="n">${r.questoes}</td><td class="n">${r.questoes?r.acertos+' ('+Math.round(r.acertos/r.questoes*100)+'%)':'—'}</td><td class="n">${r.pontos_dia}</td>`;tb.appendChild(t)}
 if(!rows.length){const t=el('tr'),d=el('td',null,'Ninguém jogou hoje ainda.');d.colSpan=10;t.appendChild(d);tb.appendChild(t)}
 w.appendChild(tb);B.appendChild(w);
 const nao=L.filter(r=>!r.hoje&&((AD.vt||'all')==='all'||r.turma===AD.vt));if(nao.length){const d=el('details');d.innerHTML=`<summary class="sdim" style="cursor:pointer;margin-top:8px">Ainda não entraram hoje (${nao.length})</summary><p class="sdim">${nao.sort((a,b)=>a.turma.localeCompare(b.turma)||String(a.nome).localeCompare(String(b.nome),'pt')).map(r=>`${r.turma} · ${r.nome||r.nick}`).join('<br>')}</p>`;B.appendChild(d)}}
async function adminLoad(){""")
# botão e rota no painel
rep("h.appendChild(el('span','etit2','PAINEL DO PROFESSOR · '+(AD.view==='turmas'?'VISÃO POR TURMA':'ALUNOS CADASTRADOS')));",
    "h.appendChild(el('span','etit2','PAINEL DO PROFESSOR · '+(AD.view==='vivo'?'AO VIVO / HOJE':AD.view==='turmas'?'VISÃO POR TURMA':'ALUNOS CADASTRADOS')));h.appendChild(eBtn('🟢 AO VIVO','sm'+(AD.view==='vivo'?' on':''),()=>{AD.view=AD.view==='vivo'?'':'vivo';if(AD.view==='vivo')aoVivoLoad();renderAdmin()}));")
rep("h.appendChild(eBtn('↻ ATUALIZAR','sm',()=>{AD.enem=null;adminLoad()}));",
    "h.appendChild(eBtn('↻ ATUALIZAR','sm',()=>{AD.enem=null;if(AD.view==='vivo')aoVivoLoad();else adminLoad()}));")
rep(" if(AD.view==='turmas'){renderTurmas(B);return}"," if(AD.view==='vivo'){renderVivo(B);return}\n if(AD.view==='turmas'){renderTurmas(B);return}")
rep(".adt tr.clk{cursor:pointer}",".vivo{display:inline-block;width:10px;height:10px;border-radius:50%;background:#5ac86a;box-shadow:0 0 6px #5ac86a;animation:vivoP 1.6s infinite}@keyframes vivoP{50%{opacity:.35}}.adt tr.clk{cursor:pointer}")
# ping logo ao entrar
rep("function enterGame(){setTimeout(pedirEmail,4000);","function enterGame(){setTimeout(pedirEmail,4000);setTimeout(pingTick,3000);")
open(f,'w',encoding='utf-8').write(s);print('aovivo ok',f)
